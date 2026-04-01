from django.contrib import admin
from .models import DashboardAccessControl, ReminderLog


@admin.register(DashboardAccessControl)
class DashboardAccessControlAdmin(admin.ModelAdmin):
    list_display = ('user', 'can_access_dashboard', 'can_manage_inquiries', 'can_manage_appointments')
    list_filter = ('can_access_dashboard', 'can_manage_inquiries', 'can_manage_appointments')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')


@admin.register(ReminderLog)
class ReminderLogAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'reminder_type', 'sent_at', 'status')
    list_filter = ('reminder_type', 'status', 'sent_at')
    readonly_fields = ('sent_at',)
