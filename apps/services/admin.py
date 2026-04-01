from django.contrib import admin
from .models import Service, ServiceFAQ


class ServiceFAQInline(admin.StackedInline):
    model = ServiceFAQ
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'order')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ServiceFAQInline]


@admin.register(ServiceFAQ)
class ServiceFAQAdmin(admin.ModelAdmin):
    list_display = ('service', 'question', 'order')
    list_filter = ('service',)
    search_fields = ('question', 'answer')
