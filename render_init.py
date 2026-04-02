#!/usr/bin/env python
"""
Render initialization script - runs on startup to prepare the application
Must be run BEFORE gunicorn starts
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth.models import User
from django.core.management import call_command
from django.db import connection
from apps.core.models import CoreSettings

print("\n" + "=" * 70)
print("RENDER STARTUP: Initializing application...")
print("=" * 70)

# CRITICAL: 1. Run migrations FIRST - must complete before any table access
print("\n[STEP 1/4] Running database migrations...")
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    print("  ✓ Database connected")
    
    # Run migrations
    call_command('migrate', '--noinput', verbosity=1)
    print("  ✓ Migrations completed successfully")
    print("  ✓ All tables (including testimonials_testimonial) created")
except Exception as e:
    print(f"  ✗ CRITICAL ERROR: {type(e).__name__}: {e}")
    print("  ✗ ABORTING: Cannot proceed without migrations")
    sys.exit(1)

# 2. Create superuser if needed
print("\n[STEP 2/4] Checking admin user...")
try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@hsconsulting.co.ke', 'Admin@123')
        print("  ✓ Admin user created (username: admin, password: Admin@123)")
    else:
        print("  ✓ Admin user already exists")
except Exception as e:
    print(f"  ⚠ Admin user issue: {e}")

# 3. Initialize CoreSettings with both partners
print("\n[STEP 3/4] Initializing core settings...")
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
        print("  ✓ CoreSettings created")
        print(f"    Partner 1: {settings.email} / {settings.phone}")
        print(f"    Partner 2: {settings.email_2} / {settings.phone_2}")
    else:
        print("  ✓ CoreSettings already exists")
        # Ensure partner 2 info is correct
        if settings.email_2 != 'ibrahimhussein481@gmail.com':
            settings.email_2 = 'ibrahimhussein481@gmail.com'
            settings.phone_2 = '+254746645534'
            settings.whatsapp_2 = '+254729592895'
            settings.save()
            print("  ✓ Partner 2 info updated")
except Exception as e:
    print(f"  ⚠ CoreSettings issue: {type(e).__name__}: {e}")

# 4. Populate initial data (if empty)
print("\n[STEP 4/4] Populating initial data...")
try:
    from apps.appointments.models import TaxDeadline
    if TaxDeadline.objects.count() == 0:
        call_command('populate_tax_deadlines', verbosity=0)
        print("  ✓ Tax deadlines populated (5 records)")
    else:
        print("  ✓ Tax deadlines already exist")
except Exception as e:
    print(f"  ⚠ Tax deadlines: {type(e).__name__}")

try:
    from apps.services.models import Service
    if Service.objects.count() == 0:
        call_command('populate_services', verbosity=0)
        print("  ✓ Services populated (13 records)")
    else:
        print("  ✓ Services already exist")
except Exception as e:
    print(f"  ⚠ Services: {type(e).__name__}")

try:
    from apps.testimonials.models import Testimonial
    count = Testimonial.objects.count()
    if count == 0:
        call_command('populate_testimonials', verbosity=0)
        print(f"  ✓ Initial testimonials populated (6 records)")
        print("  NOTE: Admins can add/edit testimonials from Django admin")
    else:
        print(f"  ✓ Testimonials already exist ({count} records)")
except Exception as e:
    print(f"  ⚠ Testimonials: {type(e).__name__}: {e}")

print("\n" + "=" * 70)
print("RENDER STARTUP: Initialization complete - App ready to serve requests!")
print("=" * 70)
print("\nAdmin URL: https://hsconsulting.onrender.com/admin/")
print("Username: admin")
print("Password: Admin@123")
print("\n")
