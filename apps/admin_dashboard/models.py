from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class DashboardAccessControl(models.Model):
    """Granular access control for admin dashboard"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dashboard_access')
    can_access_dashboard = models.BooleanField(default=False, help_text="Can access the admin dashboard")
    can_manage_inquiries = models.BooleanField(default=False, help_text="Can view and manage inquiries")
    can_manage_appointments = models.BooleanField(default=False, help_text="Can view and manage appointments")
    can_manage_clients = models.BooleanField(default=False, help_text="Can view and manage clients")
    can_manage_services = models.BooleanField(default=False, help_text="Can manage services")
    can_manage_blog = models.BooleanField(default=False, help_text="Can manage blog posts")
    can_view_reports = models.BooleanField(default=False, help_text="Can view analytics and reports")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Dashboard Access Control")
        verbose_name_plural = _("Dashboard Access Controls")
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - Dashboard Access"


class ReminderLog(models.Model):
    """Log of sent appointment reminders"""
    REMINDER_TYPE_CHOICES = [
        ('email', _('Email')),
        ('sms', _('SMS')),
    ]
    
    STATUS_CHOICES = [
        ('sent', _('Sent')),
        ('failed', _('Failed')),
        ('pending', _('Pending')),
    ]
    
    appointment = models.ForeignKey('appointments.Appointment', on_delete=models.CASCADE, related_name='reminders')
    reminder_type = models.CharField(max_length=10, choices=REMINDER_TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = _("Reminder Log")
        verbose_name_plural = _("Reminder Logs")
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.get_reminder_type_display()} to {self.appointment.client_name} - {self.status}"


class AdminActivityLog(models.Model):
    """Log of staff activities"""
    ACTION_CHOICES = [
        ('created', _('Created')),
        ('updated', _('Updated')),
        ('deleted', _('Deleted')),
        ('viewed', _('Viewed')),
        ('login', _('Login')),
        ('logout', _('Logout')),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.IntegerField()
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("Activity Log")
        verbose_name_plural = _("Activity Logs")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.action} on {self.model_name}"
