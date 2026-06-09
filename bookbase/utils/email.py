from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_purchase_confirmation(user, order, tokens=None):
    """Send purchase confirmation email with download links"""
    subject = f'Your Book Purchase Confirmation - Order #{getattr(order, "order_number", order.id)}'
    
    context = {
        'user': user,
        'order': order,
        'tokens': tokens or [],
        'site_name': 'Hezora BookStore',
        'frontend_url': getattr(settings, 'FRONTEND_URL', 'http://localhost:8000'),
    }

    html_message = render_to_string('emails/purchase_confirmation.html', context)
    plain_message = strip_tags(html_message)

    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@hezora.com'),
        to=[user.email]
    )
    email.attach_alternative(html_message, "text/html")
    email.send()
