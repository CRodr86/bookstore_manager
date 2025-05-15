from django.db import models

class Book(models.Model):
    """
    Model representing a book in the inventory.
    """
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author}"


class RestockEvent(models.Model):
    """
    Model representing a restock event for a book.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='restock_events')
    scheduled_for = models.DateTimeField()
    quantity = models.PositiveIntegerField(default=1)
    executed = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, blank=True)
    executed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Restock {self.quantity}x {self.book.title} scheduled for {self.scheduled_for}"
    