#!/bin/bash
set -o errexit

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating admin superuser if needed..."
python manage.py shell << END
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@hsconsulting.co.ke', 'Admin@123')
    print("✓ Superuser admin created")
else:
    print("✓ Superuser admin already exists")
END

echo "Build complete!"
