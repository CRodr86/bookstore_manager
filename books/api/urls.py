from django.urls import path
from .views import (
    BookListCreateAPIView,
    BookDetailAPIView,
    PurchaseBookAPIView,
    RestockEventListAPIView,
    BookRetrieveUpdateDestroyAPIView,
    BookListAPIView,
)

app_name = 'books_api'

urlpatterns = [
    path('books/', BookListCreateAPIView.as_view(), name='books-list-create'),    path('books/<int:pk>/', BookDetailAPIView.as_view(), name='books-detail'),
    path('books/', BookListAPIView.as_view(), name='books-list'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyAPIView.as_view(), name='books-detail-update-delete'),
    path('books/<int:pk>/', BookDetailAPIView.as_view(), name='books-detail'),
    path('book/buy/<int:pk>/', PurchaseBookAPIView.as_view(), name='book-buy-api'),
    path('events/', RestockEventListAPIView.as_view(), name='events-list'),
]
