import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Inquiry
from .forms import InquiryForm

logger = logging.getLogger(__name__)


def contact_us(request):
    """Contact form view"""
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()

            # Send confirmation email to client
            try:
                inquiry.send_confirmation_email()
                logger.info("Inquiry confirmation email sent to %s", inquiry.email)
            except Exception as e:
                logger.error("Failed to send inquiry confirmation to %s: %s", inquiry.email, e, exc_info=True)

            # Send notification email to owner
            try:
                inquiry.send_owner_notification()
                logger.info("Inquiry owner notification sent")
            except Exception as e:
                logger.error("Failed to send inquiry owner notification: %s", e, exc_info=True)
            
            messages.success(request, 'Thank you for your inquiry! We will get back to you shortly.')
            return redirect('inquiries:contact_success')
    else:
        form = InquiryForm()
    
    context = {
        'form': form,
    }
    return render(request, 'inquiries/contact_us.html', context)


def contact_success(request):
    """Success page after inquiry"""
    return render(request, 'inquiries/contact_success.html')
