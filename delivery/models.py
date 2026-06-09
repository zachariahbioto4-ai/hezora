from django.db import models
from django.conf import settings
from books.models import Book, BookFile
from orders.models import Order
import uuid
from datetime import timedelta
from django.utils import timezone

def default_expiry():
    return timezone.now() + timedelta(hours=48)

class DownloadToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book_file = models.ForeignKey(BookFile, on_delete=models.CASCADE)
    expires_at = models.DateTimeField(default=default_expiry)
    max_downloads = models.PositiveIntegerField(default=5)
    download_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_valid(self):
        return self.download_count < self.max_downloads and self.expires_at > timezone.now()

    def __str__(self):
        return f"Token for {self.book_file.book.title}"

class PurchasedBook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')

class DownloadLog(models.Model):
    token = models.ForeignKey(DownloadToken, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    downloaded_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
