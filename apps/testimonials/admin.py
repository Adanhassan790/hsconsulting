from django.contrib import admin
from .models import Testimonial, CaseStudy


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_company', 'rating', 'is_featured', 'is_published')
    list_filter = ('rating', 'is_featured', 'is_published')
    search_fields = ('client_name', 'client_company', 'content')


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ('title', 'client_company', 'is_published')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'client_name', 'client_company')
    prepopulated_fields = {'slug': ('title',)}
