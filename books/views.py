from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book, Category

def dashboard_view(request):
    """Discovery / Home page"""
    books = Book.objects.filter(is_available=True)[:12]
    categories = Category.objects.all()
    
    context = {
        'books': books,
        'categories': categories,
        'title': 'Discover Books - Hezora'
    }
    return render(request, 'books/dashboard.html', context)

def book_detail_view(request, slug):
    """Single book detail page"""
    book = get_object_or_404(Book, slug=slug)
    context = {
        'book': book,
        'title': book.title
    }
    return render(request, 'books/book_detail.html', context)

@login_required
def library_view(request):
    """User's personal library (purchased books)"""
    # This will work once delivery app is fully wired
    try:
        from delivery.models import PurchasedBook
        purchased = PurchasedBook.objects.filter(user=request.user).select_related('book')
        books = [p.book for p in purchased]
    except:
        books = []
    
    context = {
        'books': books,
        'title': 'My Library'
    }
    return render(request, 'books/library.html', context)
