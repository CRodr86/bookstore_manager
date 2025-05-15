from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Book, RestockEvent

# Create your views here.
@method_decorator(login_required, name='dispatch')
class BookListView(LoginRequiredMixin, ListView):
    """
    View to list all books in the inventory.
    """
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    
@method_decorator(login_required, name='dispatch')
class BookDetailView(DetailView):
    """
    View to display details of a single book.
    """
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['delay'] = settings.RESTOCK_DELAY_DAYS
        ctx['events'] = self.object.restock_events.filter(executed=False)
        return ctx
    
@method_decorator(login_required, name='dispatch')
class BookCreateView(CreateView):
    """
    View to create a new book in the inventory.
    """
    model = Book
    template_name = 'books/book_form.html'
    fields = ['title', 'author', 'description', 'price', 'stock']
    success_url = reverse_lazy('books:list')
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['view'] = self
        self.action = 'create'
        return ctx
    
@method_decorator(login_required, name='dispatch')
class BookUpdateView(UpdateView):
    """
    View to update an existing book in the inventory.
    """
    model = Book
    template_name = 'books/book_form.html'
    fields = ['title', 'author', 'description', 'price', 'stock']
    success_url = reverse_lazy('books:list')
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['view'] = self
        self.action = 'update'
        return ctx

@method_decorator(login_required, name='dispatch')
class BookDeleteView(DeleteView):
    """
    View to delete a book from the inventory.
    """
    model = Book
    template_name = 'books/book_confirm_delete.html'
    context_object_name = 'book'
    success_url = reverse_lazy('books:list')
    
@method_decorator(login_required, name='dispatch')
class RestockEventListView(ListView):
    """
    View to list all restock events.
    """
    model = RestockEvent
    template_name = 'books/event_list.html'
    context_object_name = 'events'
    paginate_by = 50
    
    def get_queryset(self):
        return RestockEvent.objects.filter(executed=False).order_by('scheduled_for')
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['pending_events'] = RestockEvent.objects.filter(executed=False).order_by('scheduled_for')
        ctx['executed_events'] = RestockEvent.objects.filter(executed=True).order_by('-executed_at')
        return ctx
    
@login_required
def buy_stock(request, pk):
    """
    If there is stock available, subtract 1 from the stock and schedule a restock event.
    If there is no stock available, and there isn't a scheduled event: schedule a restock event.
    If there is no stock available, and there is a scheduled event: show a message that it's already scheduled.
    """
    book = get_object_or_404(Book, pk=pk)
    
    # Read POST quantity or default to 1
    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1
        
    # Read delay days from settings
    delay_days = int(settings.RESTOCK_DELAY_DAYS)
    scheduled = timezone.now() + timezone.timedelta(days=delay_days)

    # Always create a new event
    RestockEvent.objects.create(
        book=book,
        scheduled_for=scheduled,
        quantity=quantity
    )
    messages.success(
        request,
        f"Order placed for {quantity}x “{book.title}”. Delivery on {scheduled:%Y-%m-%d}."
    )
    return redirect('books:detail', pk=pk)
