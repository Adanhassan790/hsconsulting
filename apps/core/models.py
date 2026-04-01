from django.db import models
from django.utils.translation import gettext_lazy as _


class CoreSettings(models.Model):
    """Global settings for the website"""
    site_name = models.CharField(max_length=200, default='HS Consulting')
    tagline = models.CharField(max_length=255, default='Tax Consulting & Financial Solutions')
    about_us = models.TextField()
    mission = models.TextField()
    
    # Contact info - Primary Partner
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20, blank=True)
    
    # Contact info - Secondary Partner
    email_2 = models.EmailField(blank=True, help_text="Second partner's email")
    phone_2 = models.CharField(max_length=20, blank=True, help_text="Second partner's phone")
    whatsapp_2 = models.CharField(max_length=20, blank=True, help_text="Second partner's WhatsApp")
    
    # Social media
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    
    # Address
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Kenya')
    
    logo = models.ImageField(upload_to='branding/')
    favicon = models.ImageField(upload_to='branding/', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Core Settings")
        verbose_name_plural = _("Core Settings")
    
    def __str__(self):
        return self.site_name


class Page(models.Model):
    """Static pages like About, Terms, Privacy"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    meta_description = models.CharField(max_length=160, blank=True)
    is_published = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/page/{self.slug}/'
