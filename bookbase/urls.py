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
