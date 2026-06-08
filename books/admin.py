from django.contrib import admin
from .models import Book, BookFile

class BookFileInline(admin.TabularInline):
    model = BookFile
    extra = 1
    fields = ['file_format', 'file', 'file_url', 'file_size_mb']
    verbose_name = "Book File"
    verbose_name_plural = "Downloadable Files"

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'rating', 'is_recommended', 'created_at')
    list_filter = ('category', 'is_recommended')
    search_fields = ('title', 'author', 'category')
    list_editable = ('is_recommended',)
    ordering = ('-created_at',)

    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'author', 'category', 'description')
        }),
        ('Cover Image', {
            'fields': ('cover_image', 'cover_url'),
            'description': 'Upload a cover image directly OR paste an external URL as fallback'
        }),
        ('Stats', {
            'fields': ('rating', 'pages', 'ratings_count', 'reviews_count')
        }),
        ('Display Settings', {
            'fields': ('is_recommended', 'color_gradient')
        }),
    )

    inlines = [BookFileInline]
