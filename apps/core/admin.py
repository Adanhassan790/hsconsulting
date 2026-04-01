from django.contrib import admin
from .models import CoreSettings, Page


@admin.register(CoreSettings)
class CoreSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'email', 'email_2', 'phone', 'phone_2')
    fieldsets = (
        ('Site Information', {
            'fields': ('site_name', 'tagline', 'about_us', 'mission')
        }),
        ('Primary Partner Contact', {
            'fields': ('email', 'phone', 'whatsapp')
        }),
        ('Secondary Partner Contact', {
            'fields': ('email_2', 'phone_2', 'whatsapp_2')
        }),
        ('Social Media', {
            'fields': ('linkedin_url', 'twitter_url', 'instagram_url')
        }),
        ('Address', {
            'fields': ('address', 'city', 'country')
        }),
        ('Branding', {
            'fields': ('logo', 'favicon')
        }),
    )


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
