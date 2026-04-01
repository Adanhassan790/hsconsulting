from django.contrib import admin
from .models import Inquiry


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'service_interested', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'service_interested')
    search_fields = ('name', 'email', 'phone', 'company_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'company_name')
        }),
        ('Inquiry Details', {
            'fields': ('service_interested', 'message', 'status')
        }),
        ('Follow-up', {
            'fields': ('follow_up_date', 'internal_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
