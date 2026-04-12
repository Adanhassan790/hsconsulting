#!/usr/bin/env python
"""Initialize database after fresh migration"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Set up Django
try:
    django.setup()
except Exception as e:
    print(f"[ERROR] Django setup failed: {e}")
    sys.exit(1)

from django.contrib.auth.models import User
from django.db import connection

print("=" * 70)
print("DATABASE INITIALIZATION")
print("=" * 70)

# First, verify tables exist
print("\n[CHECK] Verifying database tables...")
with connection.cursor() as cursor:
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_coresettings'")
        if not cursor.fetchone():
            print("[ERROR] core_coresettings table does not exist!")
            print("[ERROR] Migrations may not have run properly")
            print("[ACTION] Attempting to run migrations...")
            try:
                from django.core.management import call_command
                call_command('migrate', verbosity=1, interactive=False)
                print("[OK] Migrations completed")
            except Exception as e:
                print(f"[ERROR] Migration attempt failed: {e}")
                sys.exit(1)
    except Exception as e:
        print(f"[WARNING] Table check failed: {e}")

# Now try to import models
try:
    from apps.core.models import CoreSettings
    from apps.admin_dashboard.models import DashboardAccessControl
except ImportError as e:
    print(f"[ERROR] Failed to import models: {e}")
    sys.exit(1)

print("\n1. Setting up CoreSettings...")
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
            'whatsapp_2': '+254746645534',
            'address': 'Nairobi, Kenya',
            'city': 'Nairobi',
            'country': 'Kenya',
            'twitter_url': 'https://twitter.com/hsconsulting',
            'instagram_url': 'https://instagram.com/hsconsulting_tax',
            'facebook_url': 'https://www.facebook.com/profile.php?id=61578462577692',
            'linkedin_url': 'https://www.linkedin.com/company/hsconsultingkenya/'
        }
    )
    if created:
        print("[OK] CoreSettings created")
    else:
        print("[OK] CoreSettings already exists")
        # Ensure social media URLs are set
        if not settings.twitter_url:
            settings.twitter_url = 'https://twitter.com/hsconsulting'
        if not settings.instagram_url:
            settings.instagram_url = 'https://instagram.com/hsconsulting_tax'
        if not settings.facebook_url:
            settings.facebook_url = 'https://www.facebook.com/profile.php?id=61578462577692'
        if not settings.linkedin_url:
            settings.linkedin_url = 'https://www.linkedin.com/company/hsconsultingkenya/'
        settings.save()
except Exception as e:
    print(f"[ERROR] CoreSettings initialization failed: {e}")
    print(f"[ERROR] This usually means the table doesn't exist or database is inaccessible")
    sys.exit(1)

print("\n2. Creating superuser...")
try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@hsconsulting.co.ke', 'Admin@123')
        print("[OK] Superuser 'admin' created")
        print("  Username: admin")
        print("  Password: Admin@123")
    else:
        print("[OK] Superuser 'admin' already exists")
except Exception as e:
    print(f"[ERROR] Superuser creation failed: {e}")
    # Don't exit - this is non-critical

print("\n3. Setting up dashboard access...")
try:
    superusers = User.objects.filter(is_superuser=True)
    for user in superusers:
        access, created = DashboardAccessControl.objects.get_or_create(user=user)
        access.can_access_dashboard = True
        access.can_manage_inquiries = True
        access.can_manage_appointments = True
        access.can_manage_clients = True
        access.can_manage_services = True
        access.can_manage_blog = True
        access.can_view_reports = True
        access.save()
        if created:
            print(f"[OK] Dashboard access created for {user.username}")
        else:
            print(f"[OK] Dashboard access updated for {user.username}")
except Exception as e:
    print(f"[ERROR] Dashboard access setup failed: {e}")
    # Don't exit - this is non-critical

print("\n" + "=" * 70)
print("[OK] DATABASE INITIALIZATION COMPLETE!")
print("=" * 70)
print("\nYou can now access:")
print("  - Admin Panel: http://localhost:8000/admin/")
print("  - Dashboard: http://localhost:8000/admin-dashboard/")
print("\nCredentials:")
print("  - Username: admin")
print("  - Password: Admin@123")
print("=" * 70 + "\n")
