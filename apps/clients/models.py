from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    CLIENT_TYPE_CHOICES = [
        ('individual', _('Individual')),
        ('corporate', _('Corporate')),
        ('sme', _('SME')),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    
    # Basic info
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    client_type = models.CharField(max_length=20, choices=CLIENT_TYPE_CHOICES)
    company_name = models.CharField(max_length=200, blank=True)
    
    # Address
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Tax info
    id_number = models.CharField(max_length=50, blank=True)  # KRA PIN or ID
    vat_number = models.CharField(max_length=50, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    vip = models.BooleanField(default=False)
    
    # Documents
    profile_picture = models.ImageField(upload_to='clients/', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")
    
    def __str__(self):
        return f"{self.full_name} ({self.client_type})"


class ClientDocument(models.Model):
    """Documents uploaded by clients"""
    DOCUMENT_TYPE_CHOICES = [
        ('tax_return', _('Tax Return')),
        ('financial_statement', _('Financial Statement')),
        ('invoice', _('Invoice')),
        ('receipt', _('Receipt')),
        ('identification', _('Identification')),
        ('other', _('Other')),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    file = models.FileField(upload_to='client_documents/%Y/%m/')
    is_verified = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Client Document")
        verbose_name_plural = _("Client Documents")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.client.full_name} - {self.title}"


class ServiceHistory(models.Model):
    """Track services provided to clients"""
    STATUS_CHOICES = [
        ('ongoing', _('Ongoing')),
        ('completed', _('Completed')),
        ('on_hold', _('On Hold')),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='service_history')
    service = models.ForeignKey('services.Service', on_delete=models.SET_NULL, null=True)
    
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Service History")
        verbose_name_plural = _("Service Histories")
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.client.full_name} - {self.service.name if self.service else 'Custom Service'}"
