from django.contrib import admin
from .models import Job, JobApplication


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'employment_type', 'status', 'posted_date', 'featured', 'is_active')
    list_filter = ('status', 'employment_type', 'featured', 'is_active', 'posted_date')
    search_fields = ('title', 'department', 'description')
    readonly_fields = ('posted_date', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Job Information', {
            'fields': ('title', 'department', 'employment_type', 'location')
        }),
        ('Description', {
            'fields': ('description', 'requirements', 'responsibilities')
        }),
        ('Details', {
            'fields': ('salary_range', 'status', 'deadline')
        }),
        ('Visibility', {
            'fields': ('featured', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('posted_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'job', 'email', 'phone', 'status', 'applied_date')
    list_filter = ('status', 'applied_date', 'job')
    search_fields = ('full_name', 'email', 'job__title')
    readonly_fields = ('applied_date', 'created_at', 'updated_at', 'resume', 'cover_letter')
    
    fieldsets = (
        ('Applicant Information', {
            'fields': ('full_name', 'email', 'phone', 'job')
        }),
        ('Application', {
            'fields': ('resume', 'cover_letter')
        }),
        ('Status', {
            'fields': ('status', 'notes')
        }),
        ('Timestamps', {
            'fields': ('applied_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_shortlisted', 'mark_rejected']
    
    def mark_shortlisted(self, request, queryset):
        queryset.update(status='shortlisted')
    mark_shortlisted.short_description = "Mark selected as shortlisted"
    
    def mark_rejected(self, request, queryset):
        queryset.update(status='rejected')
    mark_rejected.short_description = "Mark selected as rejected"
