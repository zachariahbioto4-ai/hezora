from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'library'
router = DefaultRouter()
router.register(r'api', views.LibraryViewSet, basename='library')

urlpatterns = [
    path('', include(router.urls)),
    path('add_book/', views.add_book_view, name='add_book'),
    path('remove_book/', views.remove_book_view, name='remove_book'),
]
