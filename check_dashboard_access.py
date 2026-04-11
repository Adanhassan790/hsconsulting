#!/usr/bin/env python
"""Check dashboard access for superusers"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.admin_dashboard.models import DashboardAccessControl

users = User.objects.filter(is_superuser=True)
print(f'Found {users.count()} superusers\n')

for u in users:
    print(f'User: {u.username}')
    print(f'  - is_superuser: {u.is_superuser}')
    print(f'  - is_staff: {u.is_staff}')
    
    try:
        access = u.dashboard_access
        print(f'  - dashboard_access exists: Yes')
        print(f'    - can_access_dashboard: {access.can_access_dashboard}')
    except DashboardAccessControl.DoesNotExist:
        print(f'  - dashboard_access exists: NO ❌ (This is the problem!)')
    print()

print("\n" + "="*60)
print("SOLUTION: The DashboardAccessControl objects don't exist!")
print("="*60)
