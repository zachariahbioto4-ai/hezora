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
    return render(request, 'dashboard.html', context)

def book_detail_view(request, slug):
    """Single book detail page"""
    book = get_object_or_404(Book, slug=slug)
    context = {
        'book': book,
        'title': book.title
    }
    return render(request, 'book_detail.html', context)

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
    return render(request, 'library.html', context)


# ---- stubs added by fix_hezora.sh ----
from rest_framework.decorators import api_view
from rest_framework.response import Response as DRFResponse
from .serializers import BookSerializer

def orders_view(request):
    """Renders the orders page (template-based)."""
    return render(request, 'orders.html', {'title': 'My Orders'})

@login_required
def download_book(request, file_id):
    """Redirects to the delivery download endpoint via token lookup."""
    from delivery.models import DownloadToken
    token_obj = DownloadToken.objects.filter(
        user=request.user, book_file_id=file_id
    ).order_by('-created_at').first()
    if token_obj and token_obj.is_valid:
        from django.shortcuts import redirect
        return redirect(f'/api/delivery/download/{token_obj.token}/')
    from django.http import HttpResponseForbidden
    return HttpResponseForbidden('No valid download token found.')

@api_view(['GET'])
def api_books(request):
    """Public JSON list of all available books."""
    books = Book.objects.filter(is_available=True)
    serializer = BookSerializer(books, many=True, context={'request': request})
    return DRFResponse(serializer.data)
