from rest_framework import serializers
from .models import Delivery

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['id', 'order', 'tracking_number', 'status', 'carrier', 'estimated_delivery', 'actual_delivery', 'notes', 'created_at']