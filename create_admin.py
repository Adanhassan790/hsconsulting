import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Create superuser with credentials
username = 'admin'
email = 'admin@hsconsulting.co.ke'
password = 'Admin@123'

# Check if user already exists
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'✓ Superuser created successfully!')
    print(f'  Username: {username}')
    print(f'  Email: {email}')
    print(f'  Password: {password}')
else:
    print(f'✓ Superuser "{username}" already exists')
