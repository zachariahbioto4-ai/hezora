from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
    path('auth/', lambda req: render(req, 'auth.html')),
    path('book/', lambda req: render(req, 'book_detail.html')),
    path('library/', lambda req: render(req, 'library.html')),
    path('orders/', lambda req: render(req, 'orders.html')),
    path('checkout/', lambda req: render(req, 'checkout.html')),
    path('categories/', lambda req: render(req, 'categories.html')),
    path('profile/', lambda req: render(req, 'profile.html')),
    path('accounts/', include('allauth.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/accounts/', include('accounts.urls', namespace='accounts')),
    path('api/library/', include('library.urls', namespace='library')),
    path('api/orders/', include('orders.urls', namespace='orders')),
    path('api/payments/', include('payments.urls', namespace='payments')),
    path('api/delivery/', include('delivery.urls', namespace='delivery')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
