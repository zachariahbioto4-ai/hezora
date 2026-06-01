from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [

      # Post-purchase delivery page
    # /delivery/order/<uuid>/
    path(
        'order/<uuid:order_id>/',
        views.delivery_page,
        name='delivery_page'
    ),

    # Secure file download via email token
    # /delivery/download/<uuid>/
    path(
        'download/<uuid:token_uuid>/',
        views.download_file,
        name='download'
    ),

    # Re-download from My Library
    # /delivery/library/<int>/pdf/
    path(
        'library/<int:purchased_id>/<str:fmt>/',
        views.library_redownload,
        name='library_redownload'
    ),

    # Add your URL patterns here
]
