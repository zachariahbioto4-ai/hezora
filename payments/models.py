from django.db import models
from accounts.models import User
from orders.models import Order

class Payment(models.Model):
    STATUS_CHOICES = [('pending','Pending'),('completed','Completed'),('failed','Failed'),('refunded','Refunded')]
    PAYMENT_METHOD_CHOICES = [('stripe','Stripe'),('paypal','PayPal'),('bank_transfer','Bank Transfer')]
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Payment for {self.order.order_number}'