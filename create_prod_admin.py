import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookbase.settings') # <-- Make sure to replace 'your_project_name' with your actual Django project directory name
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = 'Hezorabookstore'  # Choose your production username
email = 'admin@example.com'
password = '4070Zach'  # Choose a strong password

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser {username}...")
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created successfully!")
else:
    print(f"Superuser {username} already exists.")
