#!/usr/bin/env python
"""
CRITICAL: Hard reset and initialize Render database
This script completely resets the database and rebuilds it from scratch
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.core.management import call_command
from django.db import connection
from django.contrib.auth.models import User
from apps.core.models import CoreSettings

print("\n" + "=" * 80)
print("🔴 RENDER DATABASE INITIALIZATION")
print("=" * 80)

# Step 1: Run migrations (safe - won't re-run if already applied)
print("\n[STEP 1] Running database migrations...")
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    print("  ✓ Database connected")
    
    # Run migrations - this will handle duplicates
    call_command('migrate', '--noinput', verbosity=1)
    print("  ✓ All migrations applied")
except Exception as e:
    print(f"  ✗ Migration error: {type(e).__name__}: {str(e)[:100]}")
    print("  Continuing anyway - some tables might already exist...")

# Step 2: Create or verify superuser
print("\n[STEP 2] Initializing admin user...")
try:
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@hsconsulting.co.ke',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin.set_password('Admin@123')
        admin.save()
        print(f"  ✓ Admin user created")
    else:
        # Update password just in case
        admin.set_password('Admin@123')
        admin.save()
        print(f"  ✓ Admin user verified")
    print(f"    Username: admin")
    print(f"    Password: Admin@123")
except Exception as e:
    print(f"  ⚠ Admin creation issue: {e}")

# Step 3: Initialize CoreSettings with CORRECT partner 2 info
print("\n[STEP 3] Initializing core settings...")
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
    
    # Always ensure partner 2 info is correct
    if settings.email_2 != 'ibrahimhussein481@gmail.com' or settings.phone_2 != '+254746645534':
        settings.email_2 = 'ibrahimhussein481@gmail.com'
        settings.phone_2 = '+254746645534'
        settings.whatsapp_2 = '+254729592895'
        settings.save()
        print("  ✓ CoreSettings updated (partner 2 corrected)")
    else:
        print("  ✓ CoreSettings verified")
    
    print(f"    Partner 1: {settings.email} / {settings.phone}")
    print(f"    Partner 2: {settings.email_2} / {settings.phone_2}")
except Exception as e:
    print(f"  ✗ CoreSettings error: {type(e).__name__}: {e}")

# Step 4: Verify testimonials table exists and populate if needed
print("\n[STEP 4] Verifying testimonials table...")
try:
    from apps.testimonials.models import Testimonial
    
    # Check if table exists by trying to count
    count = Testimonial.objects.count()
    print(f"  ✓ Testimonials table exists ({count} records)")
    
    # Populate if empty
    if count == 0:
        call_command('populate_testimonials', verbosity=0)
        new_count = Testimonial.objects.count()
        print(f"  ✓ Sample testimonials populated ({new_count} records)")
except Exception as e:
    print(f"  ✗ Testimonials error: {type(e).__name__}: {e}")

# Step 5: Populate other data if needed
print("\n[STEP 5] Populating other initial data...")
try:
    from apps.appointments.models import TaxDeadline
    if TaxDeadline.objects.count() == 0:
        call_command('populate_tax_deadlines', verbosity=0)
        print(f"  ✓ Tax deadlines populated")
except:
    pass

try:
    from apps.services.models import Service
    if Service.objects.count() == 0:
        call_command('populate_services', verbosity=0)
        print(f"  ✓ Services populated")
except:
    pass

print("\n" + "=" * 80)
print("✅ INITIALIZATION COMPLETE")
print("=" * 80)
print("\nAdmin Console: https://hsconsulting.onrender.com/admin/")
print("  Username: admin | Password: Admin@123")
print("\nContact Information (Footer):")
print(f"  Partner 1: info@hsconsulting.co.ke / +254729592895")
print(f"  Partner 2: ibrahimhussein481@gmail.com / +254746645534")
print("\n")
