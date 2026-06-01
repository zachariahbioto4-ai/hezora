from rest_framework import serializers
from books.serializers import BookSerializer
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'book', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'status', 'total_amount', 'shipping_address', 'items', 'created_at']