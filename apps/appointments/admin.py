from django.contrib import admin
from .models import AppointmentSlot, Appointment, TaxDeadline


@admin.register(AppointmentSlot)
class AppointmentSlotAdmin(admin.ModelAdmin):
    list_display = ('date', 'start_time', 'end_time', 'is_available')
    list_filter = ('date', 'is_available')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'service', 'appointment_date', 'status', 'assigned_staff')
    list_filter = ('status', 'appointment_date', 'created_at')
    search_fields = ('client_name', 'client_email', 'client_phone')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Client Information', {
            'fields': ('client_name', 'client_email', 'client_phone')
        }),
        ('Appointment Details', {
            'fields': ('service', 'appointment_date', 'duration_minutes', 'status')
        }),
        ('Notes', {
            'fields': ('message', 'internal_notes')
        }),
        ('Reminders', {
            'fields': ('reminder_sent_email', 'reminder_sent_sms')
        }),
        ('Staff Assignment', {
            'fields': ('assigned_staff',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TaxDeadline)
class TaxDeadlineAdmin(admin.ModelAdmin):
    list_display = ('name', 'deadline_date', 'deadline_type', 'recurring', 'created_at')
    list_filter = ('deadline_type', 'recurring', 'deadline_date')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'deadline_date'
    
    fieldsets = (
        ('Deadline Information', {
            'fields': ('name', 'description')
        }),
        ('Date & Type', {
            'fields': ('deadline_date', 'deadline_type', 'recurring')
        }),
        ('Next Occurrence', {
            'fields': ('next_deadline',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_changeform_initial_data(self, request):
        """Pre-populate with current date on creation"""
        initial = super().get_changeform_initial_data(request)
        from datetime import date
        if not initial:
            initial = {}
        initial['deadline_date'] = date.today()
        return initial
