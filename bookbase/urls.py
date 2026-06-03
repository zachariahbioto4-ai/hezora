"""
URL configuration for bookbase project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls', namespace='accounts')),
    path('api/books/', include('books.urls', namespace='books')),
    path('api/library/', include('library.urls', namespace='library')),
    path('api/orders/', include('orders.urls', namespace='orders')),
    path('api/payments/', include('payments.urls', namespace='payments')),
    path('api/delivery/', include('delivery.urls', namespace='delivery')),
    path('accounts/', include('allauth.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.http import JsonResponse

def home(request):
    return JsonResponse({
        'message': 'Welcome to BookBase API',
        'endpoints': {
            'admin': '/admin/',
            'books': '/api/books/',
            'accounts': '/api/accounts/',
            'orders': '/api/orders/',
            'payments': '/api/payments/',
            'delivery': '/api/delivery/',
            'library': '/api/library/',
        }
    })

urlpatterns = [path('', home)] + urlpatterns

from django.shortcuts import render
urlpatterns = [path('auth/', lambda req: render(req, 'auth.html'))] + urlpatterns

from django.shortcuts import render
urlpatterns = [path('auth/', lambda req: render(req, 'auth.html'))] + urlpatterns
urlpatterns = [path('book/', lambda req: render(req, 'book_detail.html'))] + urlpatterns
urlpatterns = [path('library/', lambda req: render(req, 'library.html'))] + urlpatterns
