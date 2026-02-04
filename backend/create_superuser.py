import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from test_config import get_test_password, get_test_email

username = 'admin'
email = get_test_email('admin', 'example.com')
password = get_test_password('admin')

if User.objects.filter(username=username).exists():
    print(f'Superuser "{username}" already exists!')
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser created successfully!')
    print(f'Username: {username}')
    print(f'Password: {password}')
    print(f'Email: {email}')
