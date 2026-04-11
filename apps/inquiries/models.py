from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from apps.services.models import Service


class Inquiry(models.Model):
    STATUS_CHOICES = [
        ('new', _('New')),
        ('contacted', _('Contacted')),
        ('in_progress', _('In Progress')),
        ('converted', _('Converted')),
        ('lost', _('Lost')),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company_name = models.CharField(max_length=200, blank=True)
    
    service_interested = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    follow_up_date = models.DateField(null=True, blank=True)
    internal_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Inquiry")
        verbose_name_plural = _("Inquiries")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.email}"
    
    def send_confirmation_email(self):
        """Send inquiry confirmation email to client"""
        subject = "Thank you for contacting HS Consulting"
        html_message = render_to_string('emails/inquiry_confirmation.html', {
            'inquiry': self,
        })
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,
            'noreply@hsconsulting.co.ke',
            [self.email],
            html_message=html_message,
            fail_silently=True,
        )
    
    def send_owner_notification(self):
        """Send inquiry notification email to owner"""
        from django.conf import settings
        
        owner_emails = []
        if hasattr(settings, 'OWNER_EMAIL') and settings.OWNER_EMAIL:
            owner_emails.append(settings.OWNER_EMAIL)
        
        if owner_emails:
            subject = f"New Inquiry from {self.name}"
            html_message = render_to_string('emails/inquiry_notification_owner.html', {
                'inquiry': self,
            })
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject,
                plain_message,
                'noreply@hsconsulting.co.ke',
                owner_emails,
                html_message=html_message,
                fail_silently=True,
            )
