from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Appointment, TaxDeadline
from .forms import AppointmentForm


def book_appointment(request):
    """Book an appointment"""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.status = 'scheduled'
            appointment.save()
            
            # Send confirmation email
            try:
                appointment.send_confirmation_email()
            except Exception as e:
                print(f"Error sending email: {e}")
            
            messages.success(request, 'Appointment booked successfully! You will receive a confirmation email shortly.')
            return redirect('appointments:booking_success', pk=appointment.pk)
    else:
        form = AppointmentForm()
    
    context = {
        'form': form,
    }
    return render(request, 'appointments/book_appointment.html', context)


def booking_success(request, pk):
    """Success page after booking"""
    appointment = Appointment.objects.get(pk=pk)
    context = {
        'appointment': appointment,
    }
    return render(request, 'appointments/booking_success.html', context)


def tax_calendar(request):
    """Display Kenyan tax calendar"""
    from datetime import date
    today = date.today()
    all_deadlines = TaxDeadline.objects.filter(deadline_date__isnull=False).order_by('deadline_date')
    upcoming_deadlines = all_deadlines.filter(deadline_date__gte=today)
    past_deadlines = all_deadlines.filter(deadline_date__lt=today)
    context = {
        'deadlines': all_deadlines,
        'upcoming_deadlines': upcoming_deadlines,
        'past_deadlines': past_deadlines,
        'today': today,
    }
    return render(request, 'appointments/tax_calendar.html', context)
