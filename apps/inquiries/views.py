from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Inquiry
from .forms import InquiryForm


def contact_us(request):
    """Contact form view"""
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            
            # Send confirmation email to client
            try:
                inquiry.send_confirmation_email()
            except Exception as e:
                print(f"Error sending confirmation email: {e}")
            
            # Send notification email to owner
            try:
                inquiry.send_owner_notification()
            except Exception as e:
                print(f"Error sending owner notification: {e}")
            
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
