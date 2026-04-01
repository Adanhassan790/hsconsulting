from django.contrib import admin
from .models import Client, ClientDocument, ServiceHistory


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'client_type', 'phone', 'is_active', 'vip')
    list_filter = ('client_type', 'is_active', 'vip', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'company_name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ClientDocument)
class ClientDocumentAdmin(admin.ModelAdmin):
    list_display = ('client', 'document_type', 'title', 'is_verified', 'created_at')
    list_filter = ('document_type', 'is_verified', 'created_at')
    search_fields = ('client__full_name', 'title')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ServiceHistory)
class ServiceHistoryAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'start_date')
    search_fields = ('client__full_name', 'service__name')
