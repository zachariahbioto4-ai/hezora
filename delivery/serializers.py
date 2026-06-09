from rest_framework import serializers
from .models import PurchasedBook, DownloadToken, DownloadLog

class PurchasedBookSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_cover = serializers.CharField(source='book.cover_url', read_only=True)

    class Meta:
        model = PurchasedBook
        fields = ['id', 'book', 'book_title', 'book_cover', 'order', 'purchased_at']
        read_only_fields = ['id', 'purchased_at']

class DownloadTokenSerializer(serializers.ModelSerializer):
    is_valid = serializers.BooleanField(read_only=True)
    file_format = serializers.CharField(source='book_file.file_format', read_only=True)

    class Meta:
        model = DownloadToken
        fields = ['id', 'token', 'book_file', 'file_format', 'expires_at', 'max_downloads', 'download_count', 'is_valid', 'created_at']
        read_only_fields = ['id', 'token', 'download_count', 'created_at']

class DownloadLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownloadLog
        fields = ['id', 'user', 'token', 'ip_address', 'success', 'downloaded_at']
        read_only_fields = ['id', 'downloaded_at']
