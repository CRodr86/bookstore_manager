from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


from books.models import Book, RestockEvent
from .serializers import BookSerializer, RestockEventSerializer


class BookListAPIView(generics.ListAPIView):
    """
    GET /api/books/  -> list all books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    

class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/books/{pk}/    Retrieve
    PUT    /api/books/{pk}/    Update
    PATCH  /api/books/{pk}/    Partial update
    DELETE /api/books/{pk}/    Delete
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    

class PurchaseBookAPIView(APIView):
    """
    POST /api/book/buy/<id>/ -> purchase a book (reduces stock, schedules restock)
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        try:
            quantity = max(1, int(request.data.get('quantity', 1)))
        except (TypeError, ValueError):
            return Response({'detail': 'Quantity must be a positive integer.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate stock
        if book.stock < quantity:
            return Response({'detail': 'Insufficient stock available.'}, status=status.HTTP_400_BAD_REQUEST)

        # Reduce stock
        book.stock -= quantity
        book.save()

        # Schedule restock
        delay = int(settings.RESTOCK_DELAY_DAYS)
        scheduled = timezone.now() + timezone.timedelta(days=delay)
        ev = RestockEvent.objects.create(book=book, scheduled_for=scheduled, quantity=quantity)

        return Response({
            'book_id': book.pk,
            'purchased': quantity,
            'remaining_stock': book.stock,
            'restock_event': RestockEventSerializer(ev).data
        }, status=status.HTTP_201_CREATED)


class RestockEventListAPIView(APIView):
    """
    GET /api/events/ -> returns both pending and executed restock events
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        pending = RestockEvent.objects.filter(executed=False).order_by('scheduled_for')
        executed = RestockEvent.objects.filter(executed=True).order_by('-executed_at')
        return Response({
            'pending_events': RestockEventSerializer(pending, many=True).data,
            'executed_events': RestockEventSerializer(executed, many=True).data,
        })

class BookListCreateAPIView(generics.ListCreateAPIView):
    """
    GET  /api/books/      List all books
    POST /api/books/      Create a new book
    """
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'author']


class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/books/{pk}/    Retrieve a book
    PUT    /api/books/{pk}/    Update a book
    DELETE /api/books/{pk}/    Delete a book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer