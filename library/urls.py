from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'library'
router = DefaultRouter()
router.register(r'', views.LibraryViewSet, basename='library')
urlpatterns = [path('', include(router.urls))]
