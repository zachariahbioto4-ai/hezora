from django.contrib import admin
from .models import LibraryEntry

@admin.register(LibraryEntry)
class LibraryEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'added_at']
    search_fields = ['user__username', 'book__title']
