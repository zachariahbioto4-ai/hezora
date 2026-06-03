from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'delivery'
router = DefaultRouter()
router.register(r'deliveries', views.PurchasedBookViewSet, basename='delivery')
urlpatterns = [path('', include(router.urls))]
