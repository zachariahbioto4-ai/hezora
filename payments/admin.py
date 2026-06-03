from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'user', 'amount', 'status', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method']
    search_fields = ['user__username', 'transaction_id']
