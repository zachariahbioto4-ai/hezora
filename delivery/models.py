from django.db import models
from orders.models import Order

class Delivery(models.Model):
    STATUS_CHOICES = [('pending','Pending'),('in_transit','In Transit'),('out_for_delivery','Out for Delivery'),('delivered','Delivered'),('failed','Failed')]
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery')
    tracking_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    carrier = models.CharField(max_length=100)
    estimated_delivery = models.DateField()
    actual_delivery = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Delivery for {self.order.order_number}'