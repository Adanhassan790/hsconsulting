from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from apps.services.models import Service


class AppointmentSlot(models.Model):
    """Available appointment slots"""
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _("Appointment Slot")
        verbose_name_plural = _("Appointment Slots")
        unique_together = ['date', 'start_time']
    
    def __str__(self):
        return f"{self.date} - {self.start_time}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', _('Scheduled')),
        ('confirmed', _('Confirmed')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
        ('no-show', _('No Show')),
    ]
    
    # Client info
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=20)
    
    # Appointment details
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    appointment_date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60)
    
    # Notes
    message = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True, help_text='Staff notes only')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    
    # Reminders
    reminder_sent_email = models.BooleanField(default=False)
    reminder_sent_sms = models.BooleanField(default=False)
    
    # Assignment
    assigned_staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Appointment")
        verbose_name_plural = _("Appointments")
        ordering = ['-appointment_date']
    
    def __str__(self):
        return f"{self.client_name} - {self.appointment_date}"
    
    def send_confirmation_email(self):
        """Send appointment confirmation email"""
        subject = f"Appointment Confirmation - {self.service.name if self.service else 'HS Consulting'}"
        html_message = render_to_string('emails/appointment_confirmation.html', {
            'appointment': self,
        })
        plain_message = strip_tags(html_message)
        send_mail(
            subject,
            plain_message,
            'noreply@hsconsulting.co.ke',
            [self.client_email],
            html_message=html_message,
            fail_silently=False,
        )
    
    def send_reminder_email(self):
        """Send appointment reminder email 24 hours before"""
        subject = f"Reminder: Your appointment on {self.appointment_date.strftime('%B %d, %Y')}"
        html_message = render_to_string('emails/appointment_reminder.html', {
            'appointment': self,
        })
        plain_message = strip_tags(html_message)
        send_mail(
            subject,
            plain_message,
            'noreply@hsconsulting.co.ke',
            [self.client_email],
            html_message=html_message,
            fail_silently=False,
        )
        self.reminder_sent_email = True
        self.save()


class TaxDeadline(models.Model):
    """Kenyan tax calendar deadlines"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    deadline_date = models.DateField()
    deadline_type = models.CharField(max_length=50, choices=[
        ('vat', 'VAT'),
        ('income_tax', 'Income Tax'),
        ('paye', 'PAYE'),
        ('excise_duty', 'Excise Duty'),
        ('other', 'Other'),
    ])
    recurring = models.BooleanField(default=False, help_text='Does this repeat every year?')
    next_deadline = models.DateField(null=True, blank=True, help_text='For recurring deadlines')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Tax Deadline")
        verbose_name_plural = _("Tax Deadlines")
        ordering = ['deadline_date']
    
    def __str__(self):
        return f"{self.name} - {self.deadline_date}"
