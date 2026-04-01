"""
Celery tasks for HS Consulting
"""
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from twilio.rest import Client as TwilioClient

from apps.appointments.models import Appointment, ReminderLog
from django.conf import settings


@shared_task
def send_appointment_reminders():
    """Send appointment reminders 24 hours before"""
    now = timezone.now()
    tomorrow = now + timedelta(hours=24)
    
    # Find appointments that need reminders
    appointments = Appointment.objects.filter(
        appointment_date__gte=now,
        appointment_date__lte=tomorrow,
        reminder_sent_email=False,
        status__in=['scheduled', 'confirmed']
    )
    
    for appointment in appointments:
        # Send email reminder
        try:
            appointment.send_reminder_email()
            ReminderLog.objects.create(
                appointment=appointment,
                reminder_type='email',
                status='sent'
            )
        except Exception as e:
            ReminderLog.objects.create(
                appointment=appointment,
                reminder_type='email',
                status='failed',
                error_message=str(e)
            )
        
        # Send SMS reminder if Twilio is configured
        if settings.TWILIO_ACCOUNT_SID:
            try:
                send_sms_reminder(appointment)
                ReminderLog.objects.create(
                    appointment=appointment,
                    reminder_type='sms',
                    status='sent'
                )
                appointment.reminder_sent_sms = True
                appointment.save()
            except Exception as e:
                ReminderLog.objects.create(
                    appointment=appointment,
                    reminder_type='sms',
                    status='failed',
                    error_message=str(e)
                )


def send_sms_reminder(appointment):
    """Send SMS reminder using Twilio"""
    client = TwilioClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    message_text = f"Hello {appointment.client_name}, this is a reminder about your appointment on {appointment.appointment_date.strftime('%B %d, %Y at %I:%M %p')}. Reply STOP to opt out."
    
    client.messages.create(
        body=message_text,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=appointment.client_phone
    )


@shared_task
def send_inquiry_follow_up_reminders():
    """Send follow-up reminders for inquiries"""
    from apps.inquiries.models import Inquiry
    
    today = timezone.now().date()
    inquiries = Inquiry.objects.filter(follow_up_date=today)
    
    for inquiry in inquiries:
        # Send internal reminder to staff
        # This would typically be logged or sent to staff emails
        pass


@shared_task
def check_upcoming_tax_deadlines():
    """Alert staff about upcoming tax deadlines"""
    from apps.appointments.models import TaxDeadline
    
    now = timezone.now().date()
    upcoming = TaxDeadline.objects.filter(
        deadline_date__gte=now,
        deadline_date__lt=now + timedelta(days=7)
    )
    
    # Could send alerts to admin dashboard or staff emails
    return f"Found {upcoming.count()} upcoming tax deadlines"
