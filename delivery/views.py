from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from .models import DownloadToken, PurchasedBook, DownloadLog
from books.models import BookFile
from books.serializers import BookSerializer
from datetime import timedelta
from django.utils import timezone

class DownloadViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def generate_tokens(self, request):
        order_id = request.data.get('order_id')
        try:
            from orders.models import Order
            order = Order.objects.get(id=order_id, user=request.user)
            
            if order.status != 'confirmed':
                return Response({'error': 'Order not confirmed'}, status=status.HTTP_400_BAD_REQUEST)

            tokens = []
            for item in order.items.all():
                book_file = BookFile.objects.filter(book=item.book).first()
                if book_file:
                    token = DownloadToken.objects.create(
                        user=request.user,
                        order=order,
                        book_file=book_file,
                        expires_at=timezone.now() + timedelta(hours=48),
                        max_downloads=5
                    )
                    tokens.append({
                        'token': str(token.token),
                        'book_title': item.book.title,
                        'download_url': f'/api/delivery/download/{token.token}/'
                    })
                    PurchasedBook.objects.get_or_create(user=request.user, book=item.book, order=order)

            return Response({'tokens': tokens}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def download(self, request, token=None):
        token_obj = get_object_or_404(DownloadToken, token=token)
        
        if not token_obj.is_valid or token_obj.user != request.user:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_403_FORBIDDEN)

        try:
            file_path = token_obj.book_file.file.path
            token_obj.download_count += 1
            token_obj.save()

            DownloadLog.objects.create(
                token=token_obj,
                user=request.user,
                ip_address=request.META.get('REMOTE_ADDR', ''),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

            response = FileResponse(open(file_path, 'rb'), as_attachment=True)
            response['Content-Disposition'] = f'attachment; filename="{token_obj.book_file.book.title}.pdf"'
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PurchasedBookViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookSerializer

    def get_queryset(self):
        return PurchasedBook.objects.filter(user=self.request.user)
