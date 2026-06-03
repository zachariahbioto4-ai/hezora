from rest_framework import serializers
from .models import Book, Genre, Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug']

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    class Meta:
        model = Book
        fields = ['id', 'title', 'slug', 'isbn', 'authors', 'genres', 'synopsis', 'cover_image', 'pages', 'language', 'published_date', 'price', 'is_free', 'is_published', 'is_featured', 'created_at']
