"""
Signals for admin dashboard app
Automatically create DashboardAccessControl for staff users
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import DashboardAccessControl


@receiver(post_save, sender=User)
def create_dashboard_access(sender, instance, created, **kwargs):
    """
    Create DashboardAccessControl for new staff/admin users
    """
    if created and (instance.is_staff or instance.is_superuser):
        access, _ = DashboardAccessControl.objects.get_or_create(user=instance)
        
        # Grant full access to superusers and staff
        if instance.is_superuser:
            access.can_access_dashboard = True
            access.can_manage_inquiries = True
            access.can_manage_appointments = True
            access.can_manage_clients = True
            access.can_manage_services = True
            access.can_manage_blog = True
            access.can_view_reports = True
        elif instance.is_staff:
            # Staff members get dashboard access but can customize permissions
            access.can_access_dashboard = True
        
        access.save()


@receiver(post_save, sender=User)
def update_dashboard_access_on_user_update(sender, instance, created, **kwargs):
    """
    Update DashboardAccessControl when user is promoted to superuser/staff
    """
    if not created:  # Only for updates
        try:
            access = DashboardAccessControl.objects.get(user=instance)
            
            # Grant full access to superusers
            if instance.is_superuser:
                access.can_access_dashboard = True
                access.can_manage_inquiries = True
                access.can_manage_appointments = True
                access.can_manage_clients = True
                access.can_manage_services = True
                access.can_manage_blog = True
                access.can_view_reports = True
                access.save()
            # Grant basic dashboard access to staff
            elif instance.is_staff and not access.can_access_dashboard:
                access.can_access_dashboard = True
                access.save()
        except DashboardAccessControl.DoesNotExist:
            # Create if it doesn't exist
            if instance.is_staff or instance.is_superuser:
                access = DashboardAccessControl.objects.create(user=instance)
                if instance.is_superuser:
                    access.can_access_dashboard = True
                    access.can_manage_inquiries = True
                    access.can_manage_appointments = True
                    access.can_manage_clients = True
                    access.can_manage_services = True
                    access.can_manage_blog = True
                    access.can_view_reports = True
                    access.save()
