from django.contrib import admin
from .models import Book, BookFile

class BookFileInline(admin.TabularInline):
    model = BookFile
    extra = 1
    verbose_name = "Downloadable File Format"
    verbose_name_plural = "Downloadable File Formats"

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # What you see in the overview list table
    list_display = ('title', 'author', 'category', 'rating', 'pages', 'is_recommended')
    list_filter = ('category', 'is_recommended', 'created_at')
    search_fields = ('title', 'author', 'category', 'description')
    list_editable = ('is_recommended',)
    ordering = ('-created_at',)
    
    # Organize fields inside the detailed editor page into intuitive sections
    fieldsets = (
        ('Basic Book Details', {
            'fields': ('title', 'author', 'category', 'description')
        }),
        ('Book Coverage & Assets', {
            'fields': ('cover_url',),
            'description': 'Provide a high-quality online URL for the book cover image'
        }),
        ('Statistics & Metadata', {
            'fields': ('rating', 'pages', 'ratings_count', 'reviews_count')
        }),
        ('Promotion & Styling', {
            'fields': ('is_recommended', 'color_gradient'),
            'description': 'Tailwind CSS classes (e.g., "from-emerald-800 to-teal-900") and homepage recommendation toggle'
        }),
    )
    
    inlines = [BookFileInline]
