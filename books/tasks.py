from celery import shared_task
from django.utils import timezone
from .models import RestockEvent

@shared_task
def process_restock_events():
    """
    Look for all pending RestockEvent whose date has arrived,
    increases the stock of the book, and marks the event as executed.
    """
    now = timezone.now()
    events = RestockEvent.objects.filter(executed=False, scheduled_for__lte=now)
    for ev in events:
        # Restock
        book = ev.book
        book.stock += ev.quantity
        book.save()
        # Mark event as executed
        ev.executed = True
        ev.executed_at = now
        ev.save(update_fields=['executed', 'executed_at'])
    return f"Processed {events.count()} restock events."
