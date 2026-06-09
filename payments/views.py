from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
import stripe
from django.conf import settings
from .models import Payment
from orders.models import Order
from bookbase.utils.email import send_purchase_confirmation

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = 'payments.serializers.PaymentSerializer'
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def webhook(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except Exception:
            return Response(status=400)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            order_id = session.metadata.get('order_id')
            
            try:
                order = Order.objects.get(id=order_id)
                payment = Payment.objects.get(transaction_id=session.id)
                payment.status = 'completed'
                payment.save()

                order.status = 'confirmed'
                order.save()

                # Generate download tokens
                from delivery.views import DownloadViewSet
                download_view = DownloadViewSet()
                # Call as function to avoid issues
                tokens_response = download_view.generate_tokens(request)
                tokens = tokens_response.data.get('tokens', []) if hasattr(tokens_response, 'data') else []

                # Send confirmation email
                send_purchase_confirmation(order.user, order, tokens)

            except Exception as e:
                print(f"Error processing successful payment: {e}")

        return Response(status=200)
