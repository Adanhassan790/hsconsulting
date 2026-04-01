from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta

from apps.inquiries.models import Inquiry
from apps.appointments.models import Appointment, TaxDeadline
from apps.clients.models import Client, ClientDocument
from apps.services.models import Service
from apps.blog.models import BlogPost
from .models import DashboardAccessControl


def dashboard_access_required(view_func):
    """Decorator to check dashboard access"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        try:
            access = DashboardAccessControl.objects.get(user=request.user)
            if not access.can_access_dashboard:
                messages.error(request, 'You do not have permission to access the dashboard.')
                return redirect('core:home')
        except DashboardAccessControl.DoesNotExist:
            messages.error(request, 'You do not have dashboard access.')
            return redirect('core:home')
        
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@dashboard_access_required
def dashboard(request):
    """Main admin dashboard"""
    access = DashboardAccessControl.objects.get(user=request.user)
    
    # Count metrics
    new_inquiries = Inquiry.objects.filter(status='new').count()
    scheduled_appointments = Appointment.objects.filter(status='scheduled').count()
    total_clients = Client.objects.count()
    pending_documents = ClientDocument.objects.filter(is_verified=False).count()
    
    # Recent inquiries
    recent_inquiries = Inquiry.objects.filter(status='new')[:5]
    
    # Upcoming appointments
    now = timezone.now()
    upcoming_appointments = Appointment.objects.filter(
        appointment_date__gte=now,
        appointment_date__lt=now + timedelta(days=7),
        status__in=['scheduled', 'confirmed']
    ).order_by('appointment_date')[:5]
    
    # Upcoming tax deadlines
    upcoming_deadlines = TaxDeadline.objects.filter(
        deadline_date__gte=timezone.now().date(),
        deadline_date__lt=timezone.now().date() + timedelta(days=30)
    ).order_by('deadline_date')[:5]
    
    context = {
        'access': access,
        'new_inquiries': new_inquiries,
        'scheduled_appointments': scheduled_appointments,
        'total_clients': total_clients,
        'pending_documents': pending_documents,
        'recent_inquiries': recent_inquiries,
        'upcoming_appointments': upcoming_appointments,
        'upcoming_deadlines': upcoming_deadlines,
    }
    return render(request, 'admin_dashboard/dashboard.html', context)


@login_required
@dashboard_access_required
def inquiries_list(request):
    """Manage inquiries"""
    access = DashboardAccessControl.objects.get(user=request.user)
    if not access.can_manage_inquiries:
        messages.error(request, 'You do not have permission to manage inquiries.')
        return redirect('admin_dashboard:dashboard')
    
    status_filter = request.GET.get('status', 'new')
    inquiries = Inquiry.objects.filter(status=status_filter).order_by('-created_at')
    
    all_statuses = ['new', 'contacted', 'in_progress', 'converted', 'lost']
    
    context = {
        'inquiries': inquiries,
        'current_status': status_filter,
        'all_statuses': all_statuses,
    }
    return render(request, 'admin_dashboard/inquiries_list.html', context)


@login_required
@dashboard_access_required
def inquiry_detail(request, pk):
    """View and update inquiry"""
    access = DashboardAccessControl.objects.get(user=request.user)
    if not access.can_manage_inquiries:
        messages.error(request, 'You do not have permission to manage inquiries.')
        return redirect('admin_dashboard:dashboard')
    
    inquiry = get_object_or_404(Inquiry, pk=pk)
    
    if request.method == 'POST':
        inquiry.status = request.POST.get('status', inquiry.status)
        inquiry.internal_notes = request.POST.get('internal_notes', inquiry.internal_notes)
        inquiry.save()
        messages.success(request, 'Inquiry updated successfully!')
    
    context = {
        'inquiry': inquiry,
        'statuses': Inquiry.STATUS_CHOICES,
    }
    return render(request, 'admin_dashboard/inquiry_detail.html', context)


@login_required
@dashboard_access_required
def appointments_calendar(request):
    """View appointments in calendar"""
    access = DashboardAccessControl.objects.get(user=request.user)
    if not access.can_manage_appointments:
        messages.error(request, 'You do not have permission to manage appointments.')
        return redirect('admin_dashboard:dashboard')
    
    month = request.GET.get('month')
    year = request.GET.get('year')
    
    if not month or not year:
        now = timezone.now()
        month = now.month
        year = now.year
    else:
        month = int(month)
        year = int(year)
    
    appointments = Appointment.objects.filter(
        appointment_date__month=month,
        appointment_date__year=year
    ).order_by('appointment_date')
    
    context = {
        'appointments': appointments,
        'month': month,
        'year': year,
    }
    return render(request, 'admin_dashboard/appointments_calendar.html', context)


@login_required
@dashboard_access_required
def clients_list(request):
    """Manage clients"""
    access = DashboardAccessControl.objects.get(user=request.user)
    if not access.can_manage_clients:
        messages.error(request, 'You do not have permission to manage clients.')
        return redirect('admin_dashboard:dashboard')
    
    client_type = request.GET.get('type')
    search = request.GET.get('search')
    
    clients = Client.objects.all()
    
    if client_type:
        clients = clients.filter(client_type=client_type)
    
    if search:
        clients = clients.filter(
            Q(full_name__icontains=search) |
            Q(email__icontains=search) |
            Q(company_name__icontains=search)
        )
    
    context = {
        'clients': clients,
        'client_types': Client.CLIENT_TYPE_CHOICES,
    }
    return render(request, 'admin_dashboard/clients_list.html', context)


@login_required
@dashboard_access_required
def reports(request):
    """Dashboard reports and analytics"""
    access = DashboardAccessControl.objects.get(user=request.user)
    if not access.can_view_reports:
        messages.error(request, 'You do not have permission to view reports.')
        return redirect('admin_dashboard:dashboard')
    
    # Get date range from request
    report_type = request.GET.get('type', 'monthly')
    
    # Inquiries by status
    inquiries_by_status = Inquiry.objects.values('status').annotate(count=Count('id'))
    
    # Appointments by status
    appointments_by_status = Appointment.objects.values('status').annotate(count=Count('id'))
    
    # Services performance
    services_stats = Service.objects.annotate(
        appointment_count=Count('appointment')
    ).order_by('-appointment_count')
    
    context = {
        'report_type': report_type,
        'inquiries_by_status': inquiries_by_status,
        'appointments_by_status': appointments_by_status,
        'services_stats': services_stats,
    }
    return render(request, 'admin_dashboard/reports.html', context)
