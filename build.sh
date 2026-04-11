#!/bin/bash
set -o errexit

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Creating admin superuser if needed..."
python manage.py shell << END
from django.contrib.auth.models import User

# Create superuser with default password
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@hsconsulting.co.ke', 'Admin@123')
    print("✓ Superuser admin created with temporary password: Admin@123")
    print("  Please change this password in Django admin panel!")
else:
    print("✓ Superuser admin already exists")
END

echo "Initializing CoreSettings..."
python manage.py shell << END
import sys
from apps.core.models import CoreSettings

try:
    # Initialize CoreSettings with both partners
    settings, created = CoreSettings.objects.get_or_create(
        pk=1,
        defaults={
            'site_name': 'HS Consulting',
            'tagline': 'Your trusted tax consultation partner',
            'about_us': 'Leading tax consultation firm in Kenya',
            'mission': 'To provide comprehensive tax solutions',
            'email': 'info@hsconsulting.co.ke',
            'phone': '+254729592895',
            'whatsapp': '+254729592895',
            'email_2': 'ibrahimhussein481@gmail.com',
            'phone_2': '+254746645534',
            'whatsapp_2': '+254729592895',
            'address': 'Nairobi, Kenya',
            'city': 'Nairobi',
            'country': 'Kenya'
        }
    )
    if created:
        print("✓ CoreSettings initialized successfully")
    else:
        print("✓ CoreSettings already exists")
except Exception as e:
    print(f"ERROR creating CoreSettings: {e}")
    sys.exit(1)
END

echo "Populating initial data..."
python manage.py populate_tax_deadlines 2>/dev/null || echo "Tax deadlines already populated"
python manage.py populate_services 2>/dev/null || echo "Services already populated"
python manage.py populate_testimonials 2>/dev/null || echo "Testimonials already populated"

echo "Build complete!"
