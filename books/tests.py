from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Book, RestockEvent
from .tasks import process_restock_events


@override_settings(RESTOCK_DELAY_DAYS="0")
class RestockLogicTests(TestCase):
    def setUp(self):
        # Create and log in a user for panel actions
        self.user = User.objects.create_user("testuser", password="pass")
        self.client.force_login(self.user)
        # Create a test book
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            description="Test description",
            price=10.00,
            stock=5,
        )

    def test_buy_stock_creates_event_without_reducing_stock(self):
        """
        POST to buy_stock should create a RestockEvent with the quantity and
        not modify the current stock.
        """
        url = reverse("books:buy", args=[self.book.pk])
        self.client.post(url, {"quantity": "3"})

        # Refresh book and check
        self.book.refresh_from_db()
        self.assertEqual(self.book.stock, 5)

        # Check event
        evs = RestockEvent.objects.filter(book=self.book)
        self.assertEqual(evs.count(), 1)
        ev = evs.first()
        self.assertEqual(ev.quantity, 3)
        self.assertFalse(ev.executed)

    def test_multiple_buy_requests(self):
        """
        Multiple requests create multiple RestockEvents.
        """
        url = reverse("books:buy", args=[self.book.pk])
        self.client.post(url, {"quantity": "2"})
        self.client.post(url, {"quantity": "4"})

        evs = RestockEvent.objects.filter(book=self.book).order_by("quantity")
        self.assertEqual(evs.count(), 2)
        self.assertEqual(evs[0].quantity, 2)
        self.assertEqual(evs[1].quantity, 4)

    def test_process_restock_events_increments_stock_and_marks_executed(self):
        """
        The Celery task should increment the stock according to quantity,
        and mark executed and executed_at.
        """
        # Create a pending event scheduled for now
        now = timezone.now()
        ev = RestockEvent.objects.create(book=self.book, scheduled_for=now, quantity=7)
        # Initial stock
        self.assertEqual(self.book.stock, 5)

        # Execute task
        result = process_restock_events()
        # Refresh from db
        self.book.refresh_from_db()
        ev.refresh_from_db()

        # Check stock increment
        self.assertEqual(self.book.stock, 12)
        # Check marked event
        self.assertTrue(ev.executed)
        self.assertIsNotNone(ev.executed_at)
        self.assertIn("Processed 1 restock events.", result)


class EventListViewTests(TestCase):
    def setUp(self):
        # Create and log in a user for viewing events
        self.user = User.objects.create_user("testuser2", password="pass2")
        self.client.force_login(self.user)

        # Create book and events
        self.book = Book.objects.create(
            title="List Test", author="Author", description="", price=5.00, stock=0
        )
        now = timezone.now()
        # Pending event
        RestockEvent.objects.create(
            book=self.book, scheduled_for=now + timezone.timedelta(days=1), quantity=1
        )
        # Executed event
        RestockEvent.objects.create(
            book=self.book,
            scheduled_for=now - timezone.timedelta(days=2),
            executed=True,
            executed_at=now - timezone.timedelta(days=1),
            quantity=2,
        )

    def test_event_list_view_contains_both(self):
        url = reverse("books:events")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Check context
        pending = response.context["pending_events"]
        executed = response.context["executed_events"]
        self.assertEqual(len(pending), 1)
        self.assertEqual(len(executed), 1)

    def test_event_list_template_renders_tables(self):
        url = reverse("books:events")
        response = self.client.get(url)
        content = response.content.decode()
        self.assertIn("Pending Restock Events", content)
        self.assertIn("Executed Restock Events", content)


class PurchaseBookAPITests(TestCase):
    def setUp(self):
        # API purchase does not require authentication by default
        self.book = Book.objects.create(
            title="API Test Book",
            author="API Author",
            description="API test",
            price=20.00,
            stock=5,
        )
        self.url = reverse("book-buy-api", args=[self.book.pk])

    def test_purchase_book_success(self):
        """
        Test the purchase book API endpoint for successful purchase.
        """
        response = self.client.post(
            self.url, {"quantity": 2}, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        # Ensure numeric comparison, not string literal
        self.assertEqual(data["book_id"], self.book.pk)
        self.assertEqual(data["purchased"], 2)

        self.book.refresh_from_db()
        self.assertEqual(self.book.stock, 3)

        ev = RestockEvent.objects.get(pk=data["restock_event"]["id"])
        self.assertFalse(ev.executed)
        self.assertEqual(ev.quantity, 2)

    def test_purchase_book_insufficient_stock(self):
        """
        Test the purchase book API endpoint with insufficient stock.
        """
        response = self.client.post(
            self.url, {"quantity": 10}, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["detail"], "Insufficient stock available.")
        self.assertFalse(RestockEvent.objects.filter(book=self.book).exists())
