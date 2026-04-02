#!/usr/bin/env python
"""
Render initialization script - runs on startup to prepare the application
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth.models import User
from django.core.management import call_command
from apps.core.models import CoreSettings

print("=" * 70)
print("RENDER STARTUP: Initializing application...")
print("=" * 70)

# 1. Ensure migrations are ran
print("\n[1] Running migrations...")
try:
    call_command('migrate', '--noinput', verbosity=1)
    print("✓ Migrations completed")
except Exception as e:
    print(f"⚠ Migration issue: {e}")

# 2. Create superuser if needed
print("\n[2] Checking admin user...")
try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@hsconsulting.co.ke', 'Admin@123')
        print("✓ Admin user created")
    else:
        print("✓ Admin user already exists")
except Exception as e:
    print(f"⚠ Admin user issue: {e}")

# 3. Initialize CoreSettings with both partners
print("\n[3] Initializing core settings...")
try:
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
        print("✓ CoreSettings created with both partners")
    else:
        print("✓ CoreSettings already exists")
except Exception as e:
    print(f"⚠ CoreSettings issue: {e}")

# 4. Populate initial data
print("\n[4] Populating initial data...")
try:
    call_command('populate_tax_deadlines', verbosity=0)
    print("✓ Tax deadlines populated")
except:
    pass

try:
    call_command('populate_services', verbosity=0)
    print("✓ Services populated")
except:
    pass

try:
    call_command('populate_testimonials', verbosity=0)
    print("✓ Testimonials populated")
except:
    pass

print("\n" + "=" * 70)
print("RENDER STARTUP: Initialization complete!")
print("=" * 70)
