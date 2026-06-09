from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'delivery'
router = DefaultRouter()
router.register(r'deliveries', views.PurchasedBookViewSet, basename='delivery')

urlpatterns = [
    path('', include(router.urls)),
    path('download/<uuid:token>/', views.DownloadViewSet.as_view({'get': 'download'}), name='download'),
    path('generate-tokens/', views.DownloadViewSet.as_view({'post': 'generate_tokens'}), name='generate_tokens'),
]
