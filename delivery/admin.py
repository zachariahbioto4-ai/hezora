from django.contrib import admin
from .models import Delivery

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['order', 'tracking_number', 'status', 'carrier', 'estimated_delivery', 'actual_delivery']
    list_filter = ['status', 'carrier', 'created_at']
    search_fields = ['tracking_number', 'order__order_number']
    readonly_fields = ['created_at', 'updated_at']