from django.contrib import admin
from .models import Book, Genre, Author, BookFile

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'is_published', 'is_featured', 'created_at']
    list_filter = ['is_published', 'is_featured', 'created_at']
    search_fields = ['title', 'isbn']

@admin.register(BookFile)
class BookFileAdmin(admin.ModelAdmin):
    list_display = ['book', 'format', 'file_size_mb', 'created_at']
    list_filter = ['format']
