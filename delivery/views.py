from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PurchasedBook, DownloadToken, DownloadLog
from books.serializers import BookSerializer

class PurchasedBookViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookSerializer

    def get_queryset(self):
        return PurchasedBook.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def track(self, request):
        purchases = PurchasedBook.objects.filter(user=request.user)
        books = [p.book for p in purchases]
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
