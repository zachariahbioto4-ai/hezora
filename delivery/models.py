from django.db import models
from django.utils import timezone
from datetime import timedelta
import uuid
from books.models import Book, BookFile
from orders.models import Order
from accounts.models import User

def default_expiry():
    return timezone.now() + timedelta(hours=48)

class PurchasedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchased_books')
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'book']

    def __str__(self):
        return f'{self.user} - {self.book}'

class DownloadToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book_file = models.ForeignKey(BookFile, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    expires_at = models.DateTimeField(default=default_expiry)
    max_downloads = models.PositiveIntegerField(default=3)
    download_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_valid(self):
        return timezone.now() < self.expires_at and self.download_count < self.max_downloads

    def __str__(self):
        return f'Token {self.token}'

class DownloadLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    token = models.ForeignKey(DownloadToken, on_delete=models.SET_NULL, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    success = models.BooleanField(default=True)
    downloaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-downloaded_at']
