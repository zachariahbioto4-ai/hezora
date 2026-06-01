"""
WSGI config for bookbase project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookbase.settings')

application = get_wsgi_application()
