from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.BookListView.as_view(), name='list'),
    path('create/', views.BookCreateView.as_view(), name='create'),
    path('<int:pk>/', views.BookDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.BookUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.BookDeleteView.as_view(), name='delete'),
    path('<int:pk>/buy/', views.buy_stock, name='buy'),
    path('events/', views.RestockEventListView.as_view(), name='events'),
]