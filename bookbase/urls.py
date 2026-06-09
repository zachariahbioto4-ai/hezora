from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.conf import settings
from django.conf.urls.static import static
from accounts import profile_views

def logout_view(request):
    logout(request)
    return redirect('/auth/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
    path('library/', include('library.urls', namespace='library')),
    path('auth/', lambda req: render(req, 'auth.html')),
    path('checkout/', lambda req: render(req, 'checkout.html')),
    path('categories/', lambda req: render(req, 'categories.html')),
    path('profile/', lambda req: render(req, 'profile.html')),
    path('profile/update_personal/', profile_views.update_personal, name='update_personal'),
    path('profile/update_security/', profile_views.update_security, name='update_security'),
    path('profile/update_address/',  profile_views.update_address,  name='update_address'),
    path('logout/', logout_view, name='logout'),
    path('accounts/', include('allauth.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/accounts/', include('accounts.urls', namespace='accounts')),
    path('api/orders/', include('orders.urls', namespace='orders')),
    path('api/payments/', include('payments.urls', namespace='payments')),
    path('api/delivery/', include('delivery.urls', namespace='delivery')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
