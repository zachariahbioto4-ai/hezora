from django.db import models
from django.conf import settings
from books.models import Book
import uuid


class Order(models.Model):
    """
    Represents a purchase order for books.
    Used to track purchases and payment status.
    """
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('stripe', 'Stripe'),
        ('mpesa', 'M-Pesa'),
        ('paypal', 'PayPal'),
    ]
    
    # ── identifiers ───────────────────────────────
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # ── relationships ─────────────────────────────
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    books = models.ManyToManyField(
        Book,
        related_name='orders',
        help_text='Books in this order'
    )
    
    # ── payment info ──────────────────────────────
    payment_status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default='pending'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        blank=True,
        null=True
    )
    transaction_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        help_text='External payment gateway transaction ID'
    )
    
    # ── pricing ───────────────────────────────────
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    
    # ── timestamps ────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text='When payment was completed'
    )
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Order {self.id} - {self.user} ({self.payment_status})"
    
    def mark_completed(self):
        """Mark order as completed"""
        from django.utils import timezone
        self.payment_status = 'completed'
        self.completed_at = timezone.now()
        self.save()


# Create your models here.
