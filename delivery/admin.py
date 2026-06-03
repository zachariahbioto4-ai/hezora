from django.contrib import admin
from .models import PurchasedBook, DownloadToken, DownloadLog

@admin.register(PurchasedBook)
class PurchasedBookAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'order', 'purchased_at']
    search_fields = ['user__username', 'book__title']

@admin.register(DownloadToken)
class DownloadTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'book_file', 'token', 'expires_at', 'download_count', 'max_downloads']
    search_fields = ['user__username']

@admin.register(DownloadLog)
class DownloadLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'success', 'downloaded_at']
    list_filter = ['success']
