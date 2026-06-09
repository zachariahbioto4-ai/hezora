from django.contrib import admin
from .models import Book, Category

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'price', 'stock', 'is_available']
    list_filter = ['category', 'is_available']
    search_fields = ['title', 'author']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category)
