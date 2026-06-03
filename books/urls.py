from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'books'
router = DefaultRouter()
router.register(r'books', views.BookViewSet, basename='book')
router.register(r'genres', views.GenreViewSet, basename='genre')
urlpatterns = [path('', include(router.urls))]
