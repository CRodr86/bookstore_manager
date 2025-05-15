from rest_framework import serializers
from books.models import Book, RestockEvent


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model: exposes basic fields.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'price', 'stock']


class RestockEventSerializer(serializers.ModelSerializer):
    """
    Serializer for RestockEvent model: includes all relevant fields.
    """
    book_title = serializers.CharField(source='book.title', read_only=True)
    class Meta:
        model = RestockEvent
        fields = ['id', 'book', 'book_title', 'quantity', 'scheduled_for', 'executed', 'executed_at']