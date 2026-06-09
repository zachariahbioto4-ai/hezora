import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookbase.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get('ADMIN_USERNAME')
email = os.environ.get('ADMIN_EMAIL')
password = os.environ.get('ADMIN_PASSWORD')

if not all([username, email, password]):
    raise EnvironmentError(
        "Missing required environment variables: ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD"
    )

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser {username}...")
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created successfully!")
else:
    print(f"Superuser {username} already exists.")
