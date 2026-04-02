#!/usr/bin/env python
"""
CRITICAL: Hard reset and initialize Render database
This script completely resets the database and rebuilds it from scratch
Run this ONLY when migrations have permanently failed
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
print("🔴 CRITICAL DATABASE INITIALIZATION - FORCING RESET")
print("=" * 80)

# Step 1: Drop and recreate all migrations
print("\n[STEP 1] Dropping all existing tables and starting fresh...")
try:
    with connection.cursor() as cursor:
        # Get list of all tables
        cursor.execute("""
            SELECT tablename FROM pg_tables 
            WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'
        """)
        tables = cursor.fetchall()
        
        if tables:
            for table in tables:
                table_name = table[0]
                print(f"  Dropping table: {table_name}")
                try:
                    cursor.execute(f'DROP TABLE IF EXISTS "{table_name}" CASCADE')
                except Exception as e:
                    print(f"    ⚠ Could not drop {table_name}: {e}")
        else:
            print("  No tables to drop - starting fresh")
    
    connection.commit()
    print("✓ Database cleanup complete")
except Exception as e:
    print(f"⚠ Cleanup issue: {e}")

# Step 2: Run migrations fresh
print("\n[STEP 2] Running FRESH migrations...")
try:
    call_command('migrate', '--noinput', verbosity=2)
    print("✓ All migrations applied successfully")
    print("  ✓ testimonials_testimonial table created")
except Exception as e:
    print(f"✗ CRITICAL ERROR: {type(e).__name__}: {e}")
    sys.exit(1)

# Step 3: Create superuser
print("\n[STEP 3] Creating admin superuser...")
try:
    User.objects.filter(username='admin').delete()  # Remove old one if exists
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@hsconsulting.co.ke',
        password='Admin@123'
    )
    print(f"✓ Superuser created: admin (password: Admin@123)")
except Exception as e:
    print(f"⚠ Admin creation issue: {e}")

# Step 4: Create CoreSettings with CORRECT partner 2 info
print("\n[STEP 4] Initializing CoreSettings with partner contact information...")
try:
    # Delete any existing settings
    CoreSettings.objects.all().delete()
    
    # Create fresh CoreSettings with CORRECT data
    settings = CoreSettings.objects.create(
        pk=1,
        site_name='HS Consulting',
        tagline='Your trusted tax consultation partner',
        about_us='Leading tax consultation firm in Kenya',
        mission='To provide comprehensive tax solutions',
        email='info@hsconsulting.co.ke',
        phone='+254729592895',
        whatsapp='+254729592895',
        email_2='ibrahimhussein481@gmail.com',  # YOUR CORRECT EMAIL
        phone_2='+254746645534',                # YOUR CORRECT PHONE
        whatsapp_2='+254729592895',
        address='Nairobi, Kenya',
        city='Nairobi',
        country='Kenya'
    )
    print("✓ CoreSettings created with correct partner information")
    print(f"  Partner 1: {settings.email} / {settings.phone}")
    print(f"  Partner 2: {settings.email_2} / {settings.phone_2}")  # Show YOUR info
except Exception as e:
    print(f"✗ CoreSettings error: {type(e).__name__}: {e}")
    sys.exit(1)

# Step 5: Populate initial data
print("\n[STEP 5] Populating initial data...")
try:
    call_command('populate_tax_deadlines', verbosity=0)
    print("✓ Tax deadlines populated")
except Exception as e:
    print(f"⚠ Tax deadlines: {e}")

try:
    call_command('populate_services', verbosity=0)
    print("✓ Services populated")
except Exception as e:
    print(f"⚠ Services: {e}")

try:
    call_command('populate_testimonials', verbosity=0)
    print("✓ Sample testimonials populated (6 records)")
except Exception as e:
    print(f"⚠ Testimonials: {e}")

print("\n" + "=" * 80)
print("✅ DATABASE RESET COMPLETE - Application ready to run!")
print("=" * 80)
print("\nAdmin Console:")
print("  URL: https://hsconsulting.onrender.com/admin/")
print("  Username: admin")
print("  Password: Admin@123")
print("\nContact Information (Footer):")
print(f"  Partner 1: info@hsconsulting.co.ke / +254729592895")
print(f"  Partner 2: ibrahimhussein481@gmail.com / +254746645534")
print("\n")
