from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Delivery
from .serializers import DeliverySerializer

class DeliveryViewSet(viewsets.ModelViewSet):
    serializer_class = DeliverySerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Delivery.objects.filter(order__user=self.request.user)
    @action(detail=False, methods=['get'])
    def track(self, request):
        tracking_number = request.query_params.get('tracking_number')
        if tracking_number:
            delivery = Delivery.objects.filter(tracking_number=tracking_number).first()
            if delivery and delivery.order.user == request.user:
                serializer = self.get_serializer(delivery)
                return Response(serializer.data)
        return Response({'error':'Delivery not found'}, status=404)