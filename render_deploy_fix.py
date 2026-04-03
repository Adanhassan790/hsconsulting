#!/usr/bin/env python
"""
Fix all issues for Render production deployment.
This script should be run after deployment via the Render build command.
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, str(BASE_DIR))

django.setup()

from django.core.management import call_command
from django.db import connection
from apps.core.models import CoreSettings
from apps.services.models import Service

print("\n" + "="*70)
print("RENDER DEPLOYMENT FIX - Running corrections")
print("="*70)

# Step 1: Collect static files
print("\n[1/5] Collecting static files...")
try:
    call_command('collectstatic', '--noinput', '--clear', verbosity=1)
    print("✓ Static files collected successfully")
except Exception as e:
    print(f"✗ Error collecting static files: {e}")

# Step 2: Run migrations
print("\n[2/5] Running migrations...")
try:
    call_command('migrate', '--run-syncdb', verbosity=1)
    print("✓ Migrations completed successfully")
except Exception as e:
    print(f"✗ Error running migrations: {e}")

# Step 3: Initialize/Update CoreSettings with Partner 2
print("\n[3/5] Initializing CoreSettings (Partner 2 data)...")
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
            'email_2': 'admin@hsconsulting.co.ke',
            'phone_2': '+254746645534',
            'whatsapp_2': '+254729592895',
            'address': 'Nairobi, Kenya',
            'city': 'Nairobi',
            'country': 'Kenya'
        }
    )
    
    # Always update Partner 2 to correct values
    settings.email_2 = 'admin@hsconsulting.co.ke'
    settings.phone_2 = '+254746645534'
    settings.whatsapp_2 = '+254729592895'
    settings.save()
    
    print(f"✓ CoreSettings {'created' if created else 'updated'}")
    print(f"  - Partner 1: {settings.email} / {settings.phone}")
    print(f"  - Partner 2: {settings.email_2} / {settings.phone_2}")
except Exception as e:
    print(f"✗ Error initializing CoreSettings: {e}")

# Step 4: Populate services (remove any old ones with emojis)
print("\n[4/5] Populating services...")
try:
    # Clear and repopulate services
    Service.objects.all().delete()
    
    services_data = [
        ('Tax Return Filing', 'Complete tax return preparation and filing'),
        ('VAT & ETIMS Compliance', 'Comprehensive VAT management and ETIMS compliance'),
        ('Payroll Processing', 'Monthly payroll processing and statutory deductions'),
        ('Audit Services', 'Professional external and internal audit services'),
        ('Tax Advisory', 'Strategic tax planning to optimize your tax position'),
        ('Financial Consulting', 'Expert guidance on financial management and forecasting'),
    ]
    
    for i, (name, desc) in enumerate(services_data, 1):
        Service.objects.create(
            name=name,
            slug=name.lower().replace(' ', '-').replace('&', 'and'),
            description=desc,
            long_description=desc,
            price_label='Contact for Pricing',
            order=i,
            is_active=True
        )
    
    print(f"✓ Services populated: {Service.objects.count()} services created")
    for service in Service.objects.all():
        print(f"  - {service.name}")
except Exception as e:
    print(f"✗ Error populating services: {e}")

# Step 5: Run startup initialization
print("\n[5/5] Running startup initialization...")
try:
    call_command('startup', verbosity=1)
    print("✓ Startup initialization completed")
except Exception as e:
    print(f"Note: Startup command may not exist or failed: {e}")

print("\n" + "="*70)
print("RENDER DEPLOYMENT FIX COMPLETED")
print("="*70)
print("\nNext steps:")
print("1. Verify logo displays at: https://hsconsulting.onrender.com/")
print("2. Check services are emoji-free")
print("3. Verify Partner 2 contact info in footer")
print("4. Check CSS loads (dark backgrounds visible)")
print("="*70 + "\n")
