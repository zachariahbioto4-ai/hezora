from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book, Genre, Author
from .serializers import BookSerializer, GenreSerializer, AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.filter(is_published=True)
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def featured(self, request):
        books = Book.objects.filter(is_featured=True, is_published=True)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
