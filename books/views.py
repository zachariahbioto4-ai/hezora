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
            "cover_url": b.get_cover(),
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
    from django.db.models import Sum

    orders = []
    total_count = delivered_count = processing_count = 0
    total_spent = '0.00'

    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).prefetch_related('items__book').order_by('-created_at')
        total_count      = orders.count()
        delivered_count  = orders.filter(status='delivered').count()
        processing_count = orders.filter(status__in=['pending','confirmed','shipped']).count()
        spent = orders.exclude(status='cancelled').aggregate(t=Sum('total_amount'))['t']
        total_spent = f"{spent:.2f}" if spent else '0.00'

    return render(request, 'orders.html', {
        'orders': orders,
        'total_count': total_count,
        'delivered_count': delivered_count,
        'processing_count': processing_count,
        'total_spent': total_spent,
    })


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


from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
import uuid

@require_POST
@login_required
def place_order(request):
    from orders.models import Order, OrderItem
    from library.models import LibraryEntry

    book_id = request.POST.get('book_id')
    if not book_id:
        messages.error(request, 'No book selected.')
        return redirect('/checkout/')

    book = get_object_or_404(Book, id=book_id)

    first_name = request.POST.get('first_name', '').strip()
    last_name  = request.POST.get('last_name', '').strip()
    address    = request.POST.get('address', '').strip()
    city       = request.POST.get('city', '').strip()
    state      = request.POST.get('state', '').strip()
    zip_code   = request.POST.get('zip', '').strip()

    if not all([first_name, last_name, address, city, state, zip_code]):
        messages.error(request, 'Please fill in all shipping fields.')
        return redirect(f'/checkout/?book_id={book_id}')

    shipping_address = f"{first_name} {last_name}, {address}, {city}, {state} {zip_code}"

    order = Order.objects.create(
        user=request.user,
        order_number=f"BB-{uuid.uuid4().hex[:8].upper()}",
        status='confirmed',
        total_amount=14.99,
        shipping_address=shipping_address,
    )

    OrderItem.objects.create(
        order=order,
        book=book,
        quantity=1,
        price=14.99,
    )

    LibraryEntry.objects.get_or_create(user=request.user, book=book)

    messages.success(request, f'Order {order.order_number} placed! Your book has been added to your library.')
    return redirect('/library/')
