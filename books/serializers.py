from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'slug', 'author', 'category', 'description', 
                 'price', 'stock', 'image', 'is_available']
