#!/usr/bin/env python
"""
Comprehensive setup script to ensure all admin/dashboard features work correctly
Run this after deployment or when new staff users are created
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.admin_dashboard.models import DashboardAccessControl

def setup_admin_dashboard():
    """Ensure all admin users have proper dashboard access"""
    print("=" * 70)
    print("SETTING UP ADMIN DASHBOARD ACCESS")
    print("=" * 70)
    
    # Get all superusers and staff members
    staff_users = User.objects.filter(is_superuser=True) | User.objects.filter(is_staff=True)
    staff_users = staff_users.distinct()
    
    print(f"\nFound {staff_users.count()} staff/superuser accounts\n")
    
    created_count = 0
    updated_count = 0
    
    for user in staff_users:
        access, created = DashboardAccessControl.objects.get_or_create(user=user)
        
        if created:
            print(f"[OK] Created dashboard access for: {user.username}")
            created_count += 1
        else:
            print(f"[INFO] Found existing dashboard access for: {user.username}")
        
        # Ensure superusers have full access
        if user.is_superuser:
            needs_update = False
            if not access.can_access_dashboard:
                access.can_access_dashboard = True
                needs_update = True
            if not access.can_manage_inquiries:
                access.can_manage_inquiries = True
                needs_update = True
            if not access.can_manage_appointments:
                access.can_manage_appointments = True
                needs_update = True
            if not access.can_manage_clients:
                access.can_manage_clients = True
                needs_update = True
            if not access.can_manage_services:
                access.can_manage_services = True
                needs_update = True
            if not access.can_manage_blog:
                access.can_manage_blog = True
                needs_update = True
            if not access.can_view_reports:
                access.can_view_reports = True
                needs_update = True
            
            if needs_update:
                access.save()
                print(f"   → Updated permissions for superuser")
                updated_count += 1
        
        # Ensure staff have at least basic access
        elif user.is_staff and not access.can_access_dashboard:
            access.can_access_dashboard = True
            access.save()
            updated_count += 1
            print(f"   → Updated permissions for staff member")
    
    print("\n" + "=" * 70)
    print(f"SUMMARY")
    print("=" * 70)
    print(f"  Created: {created_count} new access records")
    print(f"  Updated: {updated_count} existing access records")
    print("[OK] Admin dashboard is now properly configured!")
    print("\nYou can now access:")
    print("  - Admin panel: /admin/")
    print("  - Dashboard: /admin-dashboard/")
    print("=" * 70 + "\n")

if __name__ == '__main__':
    setup_admin_dashboard()
