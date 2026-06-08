from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Book

def dashboard_view(request):
    books_qs = Book.objects.all()
    books = []
    for b in books_qs:
        books.append({
            "id": b.id,
            "title": b.title,
            "author": b.author or "Unknown Author",
            "cover_url": b.cover_url or "https://via.placeholder.com/150",
            "category": b.category or "General",
            "rating": str(b.rating),
            "pages": b.pages,
            "ratings_count": b.ratings_count,
            "reviews_count": b.reviews_count,
            "recommended": b.is_recommended,
            "color": b.color_gradient or 'from-slate-700 to-slate-900',
            "description": b.description or ""
        })

    categories = sorted(list(set(b["category"] for b in books))) if books else []
    active_category = request.GET.get('category', 'All')
    search_query = request.GET.get('q', '')

    filtered_books = books
    if active_category != 'All':
        filtered_books = [b for b in filtered_books if b["category"].lower() == active_category.lower()]
    if search_query:
        filtered_books = [b for b in filtered_books if search_query.lower() in b["title"].lower() or search_query.lower() in b["author"].lower()]

    recommended_books = [b for b in books if b["recommended"]]

    selected_book = filtered_books[0] if filtered_books else (books[0] if books else None)
    selected_id = request.GET.get('details_id')
    if selected_id:
        try:
            matched = [b for b in books if b["id"] == int(selected_id)]
            if matched:
                selected_book = matched[0]
        except ValueError:
            pass

    context = {
        "books": filtered_books,
        "recommended": recommended_books,
        "categories": categories,
        "active_category": active_category,
        "search_query": search_query,
        "selected_book": selected_book,
    }
    return render(request, "dashboard.html", context)


def book_detail_view(request, book_id=None):
    if book_id:
        book = get_object_or_404(Book, id=book_id)
    else:
        book = Book.objects.first()
    return render(request, 'book_detail.html', {'book': book})


def library_view(request):
    from library.models import LibraryEntry
    entries = []
    if request.user.is_authenticated:
        entries = LibraryEntry.objects.filter(user=request.user).select_related('book')
    return render(request, 'library.html', {'entries': entries})


def orders_view(request):
    from orders.models import Order
    orders = []
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).prefetch_related('items__book')
    return render(request, 'orders.html', {'orders': orders})


def api_books(request):
    books_qs = Book.objects.all().values()
    return JsonResponse({"books": list(books_qs)})


from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required

@login_required
def download_book(request, file_id):
    """Secure download — only logged in users can download"""
    from .models import BookFile
    book_file = BookFile.objects.filter(id=file_id).first()
    if not book_file:
        return HttpResponseForbidden("File not found.")
    url = book_file.get_download_url()
    if not url:
        return HttpResponseForbidden("No file available.")
    return HttpResponseRedirect(url)
