from rest_framework import serializers
from .models import Book, BookFile

class BookFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookFile
        fields = ['id', 'file_format', 'file_url', 'file_size_mb'] if hasattr(BookFile, 'file_size_mb') else ['id', 'file_format', 'file_url']

class BookSerializer(serializers.ModelSerializer):
    files = BookFileSerializer(many=True, read_only=True)
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'cover_url', 'category', 'rating', 'pages', 'ratings_count', 'reviews_count', 'is_recommended', 'description', 'created_at']
