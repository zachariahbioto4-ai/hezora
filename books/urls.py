from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('book/<int:book_id>/', views.book_detail_view, name='book_detail'),
    path('library/', views.library_view, name='library'),
    path('orders/', views.orders_view, name='orders'),
    path('download/<int:file_id>/', views.download_book, name='download_book'),
    path('api/books/', views.api_books, name='api_books'),
]
