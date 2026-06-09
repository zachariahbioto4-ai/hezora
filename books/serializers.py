from rest_framework import serializers
from .models import Book, BookFile

class BookFileSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()

    def get_download_url(self, obj):
        return obj.get_download_url()

    class Meta:
        model = BookFile
        fields = ['id', 'file_format', 'file_url', 'file_size_mb', 'download_url']

class BookSerializer(serializers.ModelSerializer):
    cover = serializers.SerializerMethodField()
    files = BookFileSerializer(many=True, read_only=True)

    def get_cover(self, obj):
        return obj.get_cover()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'cover', 'category',
            'rating', 'pages', 'ratings_count', 'reviews_count',
            'is_recommended', 'description', 'files', 'created_at',
        ]
