from django.contrib import admin
from .models import DownloadToken, PurchasedBook, DownloadLog

@admin.register(DownloadToken)
class DownloadTokenAdmin(admin.ModelAdmin):
    list_display = ['token', 'user', 'book_file', 'expires_at', 'download_count']
    list_filter = ['expires_at']

@admin.register(PurchasedBook)
class PurchasedBookAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'order', 'purchased_at']

@admin.register(DownloadLog)
class DownloadLogAdmin(admin.ModelAdmin):
    list_display = ['token', 'user', 'downloaded_at', 'success']
    list_filter = ['success', 'downloaded_at']
