#!/usr/bin/env python
"""Initialize database after fresh migration"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.core.models import CoreSettings
from apps.admin_dashboard.models import DashboardAccessControl

print("=" * 70)
print("DATABASE INITIALIZATION")
print("=" * 70)

print("\n1. Setting up CoreSettings...")
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
    print("✓ CoreSettings created")
else:
    print("✓ CoreSettings already exists")

print("\n2. Creating superuser...")
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@hsconsulting.co.ke', 'Admin@123')
    print("✓ Superuser 'admin' created")
    print("  Username: admin")
    print("  Password: Admin@123")
else:
    print("✓ Superuser 'admin' already exists")

print("\n3. Setting up dashboard access...")
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
        print(f"✓ Dashboard access created for {user.username}")
    else:
        print(f"✓ Dashboard access updated for {user.username}")

print("\n" + "=" * 70)
print("✅ DATABASE INITIALIZATION COMPLETE!")
print("=" * 70)
print("\nYou can now access:")
print("  - Admin Panel: http://localhost:8000/admin/")
print("  - Dashboard: http://localhost:8000/admin-dashboard/")
print("\nCredentials:")
print("  - Username: admin")
print("  - Password: Admin@123")
print("=" * 70 + "\n")
