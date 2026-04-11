#!/usr/bin/env python
"""Create DashboardAccessControl for all superusers"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.admin_dashboard.models import DashboardAccessControl

users = User.objects.filter(is_superuser=True)
print(f'Found {users.count()} superusers\n')

for u in users:
    access, created = DashboardAccessControl.objects.get_or_create(user=u)
    
    if created:
        # Grant full access to superusers
        access.can_access_dashboard = True
        access.can_manage_inquiries = True
        access.can_manage_appointments = True
        access.can_manage_clients = True
        access.can_manage_services = True
        access.can_manage_blog = True
        access.can_view_reports = True
        access.save()
        print(f'✅ Created dashboard access for: {u.username}')
    else:
        # Update existing
        access.can_access_dashboard = True
        access.save()
        print(f'✅ Updated dashboard access for: {u.username}')

print('\n✅ Dashboard access configured for all superusers!')
print('\nYou should now be able to access /admin-dashboard/')
