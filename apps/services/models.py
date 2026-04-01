from django.db import models
from django.utils.translation import gettext_lazy as _


class Service(models.Model):
    """Tax consulting services"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=500)  # Short description
    long_description = models.TextField(blank=True, default='')
    
    icon = models.ImageField(upload_to='services/', null=True, blank=True)
    image = models.ImageField(upload_to='services/', null=True, blank=True)
    
    base_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_label = models.CharField(max_length=100, default='Contact for Pricing')
    
    order = models.IntegerField(default=0, help_text='Order of appearance on the website')
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/services/{self.slug}/'


class ServiceFAQ(models.Model):
    """FAQ for each service"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = _("Service FAQ")
        verbose_name_plural = _("Service FAQs")
        ordering = ['order']
    
    def __str__(self):
        return f"{self.service.name} - {self.question[:50]}"
