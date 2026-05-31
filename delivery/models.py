from django.db import models
from django.conf import settings
from django.utils import timezone
from books.models import Book, BookFile
from orders.models import Order
import uuid
from datetime import timedelta


def default_expiry():
    # download link valid for 7 days
    return timezone.now() + timedelta(days=7)


class PurchasedBook(models.Model):
    """
    Permanent record — never expires.
    Created when order.payment_status = 'completed'.
    Powers the My Library page.
    """
    user       = models.ForeignKey(
                   settings.AUTH_USER_MODEL,
                   on_delete=models.CASCADE,
                   related_name='purchased_books')
    book       = models.ForeignKey(
                   Book, on_delete=models.PROTECT)
    order      = models.ForeignKey(
                   Order, on_delete=models.SET_NULL,
                   null=True)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} owns {self.book.title}"

    class Meta:
        unique_together = ['user', 'book']
        # can't buy same book twice


class DownloadToken(models.Model):
    """
    One token per format per purchase.
    Expires after 7 days OR 3 downloads.
    Users can always re-download from
    PurchasedBook (no token needed there).
    """
    token      = models.UUIDField(
                   default=uuid.uuid4,
                   unique=True, editable=False)
    user       = models.ForeignKey(
                   settings.AUTH_USER_MODEL,
                   on_delete=models.CASCADE)
    book_file  = models.ForeignKey(
                   BookFile, on_delete=models.CASCADE)
    order      = models.ForeignKey(
                   Order, on_delete=models.CASCADE)

    # ── limits ────────────────────────────────────
    expires_at      = models.DateTimeField(
                        default=default_expiry)
    max_downloads   = models.PositiveIntegerField(default=3)
    download_count  = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    # ── helpers ───────────────────────────────────
    @property
    def is_valid(self):
        """Token is usable if not expired & downloads left"""
        return (
            timezone.now() < self.expires_at
            and
            self.download_count < self.max_downloads
        )

    def use(self):
        """Call this on every successful download"""
        self.download_count += 1
        self.save(update_fields=['download_count'])

    def __str__(self):
        return (
            f"Token {str(self.token)[:8]}… | "
            f"{self.book_file} | valid={self.is_valid}"
        )


class DownloadLog(models.Model):
    """Audit trail of every download attempt"""
    token       = models.ForeignKey(
                    DownloadToken,
                    on_delete=models.SET_NULL,
                    null=True)
    user        = models.ForeignKey(
                    settings.AUTH_USER_MODEL,
                    on_delete=models.SET_NULL,
                    null=True)
    ip_address  = models.GenericIPAddressField(
                    blank=True, null=True)
    user_agent  = models.TextField(blank=True)
    success     = models.BooleanField(default=True)
    downloaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-downloaded_at']

# Create your models here.
