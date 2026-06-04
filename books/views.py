from django.shortcuts import render
from django.http import JsonResponse
from .models import Book

def dashboard_view(request):
    """
    Renders the live BookBase Dashboard UI populated solely by your Django Admin inputs.
    """
    # 1. Fetch your real database records
    books_qs = Book.objects.all()
    books = []
    
    for b in books_qs:
        books.append({
            "id": b.id,
            "title": b.title,
            "author": b.author or "Unknown Author",
            "cover_url": b.cover_url or "[https://via.placeholder.com/150](https://via.placeholder.com/150)",
            "category": b.category or "General",
            "rating": str(b.rating),
            "pages": b.pages,
            "ratings_count": b.ratings_count,
            "reviews_count": b.reviews_count,
            "recommended": b.is_recommended,
            "color": b.color_gradient or 'from-slate-700 to-slate-900',
            "description": b.description or ""
        })

    # 2. Extract unique categories for your filter bar
    categories = sorted(list(set(b["category"] for b in books))) if books else []
    
    # 3. Handle dashboard filtering options
    active_category = request.GET.get('category', 'All')
    search_query = request.GET.get('q', '')

    filtered_books = books
    if active_category != 'All':
        filtered_books = [b for b in filtered_books if b["category"].lower() == active_category.lower()]
    
    if search_query:
        filtered_books = [b for b in filtered_books if search_query.lower() in b["title"].lower() or search_query.lower() in b["author"].lower()]

    recommended_books = [b for b in books if b["recommended"]]
    
    # Select book detail highlight
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

def api_books(request):
    """
    Serves dynamic database book items as JSON.
    """
    books_qs = Book.objects.all().values()
    return JsonResponse({"books": list(books_qs)})
