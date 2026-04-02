from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from decouple import config
import os
import sys
from .models import CoreSettings, Page


def health_check(request):
    """Health check endpoint - diagnoses database and configuration issues"""
    diagnostics = {}
    
    # Database connection check
    try:
        db_conn = connections['default']
        with db_conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            diagnostics['database'] = {
                'status': '✅ Connected',
                'engine': db_conn.settings_dict.get('ENGINE', 'Unknown'),
                'name': db_conn.settings_dict.get('NAME', 'Unknown')
            }
    except OperationalError as e:
        diagnostics['database'] = {
            'status': '❌ Connection Failed',
            'error': str(e)
        }
    except Exception as e:
        diagnostics['database'] = {
            'status': '❌ Error',
            'error': str(e)
        }
    
    # Environment variables check
    diagnostics['environment'] = {
        'DEBUG': config('DEBUG', default='Not Set'),
        'ALLOWED_HOSTS': config('ALLOWED_HOSTS', default='Not Set')[:50] + '...',
        'DATABASE_URL': 'Set' if config('DATABASE_URL', default='') else 'Not Set',
        'DJANGO_SECRET_KEY': 'Set' if config('DJANGO_SECRET_KEY', default='') else 'Not Set',
    }
    
    # Django/Python info
    diagnostics['system'] = {
        'python_version': sys.version.split()[0],
        'django_version': __import__('django').get_version(),
        'platform': sys.platform,
    }
    
    # Try to query CoreSettings
    try:
        settings_obj = CoreSettings.objects.first()
        diagnostics['core_settings'] = {
            'status': '✅ Table exists' if settings_obj else '🟡 No data (empty)',
            'records': CoreSettings.objects.count()
        }
    except Exception as e:
        diagnostics['core_settings'] = {
            'status': '❌ Error',
            'error': str(e)
        }
    
    # Format response
    html = "<h1>🔍 Health Check Report</h1><pre>"
    import json
    html += json.dumps(diagnostics, indent=2)
    html += "</pre>"
    
    return HttpResponse(html, content_type='text/html')


def test(request):
    """Simple test view to verify server is responding"""
    return HttpResponse("✅ Server is running! Django is working correctly.")


def init(request):
    """Initialize CoreSettings if empty or update if needed"""
    try:
        # Create or get CoreSettings
        settings, created = CoreSettings.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'HS Consulting',
                'tagline': 'Your trusted tax consultation partner',
                'about_us': 'Leading tax consultation firm in Kenya',
                'mission': 'To provide comprehensive tax solutions',
                'email': 'info@hsconsulting.co.ke',
                'phone': '+254729592895',
                'whatsapp': '+254729592895',
                'email_2': 'ibrahimhussein481@gmail.com',
                'phone_2': '+254746645534',
                'whatsapp_2': '+254729592895',
                'address': 'Nairobi, Kenya',
                'city': 'Nairobi',
                'country': 'Kenya'
            }
        )
        
        # Ensure partner 2 info is set (for existing records)
        if not settings.email_2:
            settings.email_2 = 'admin@hsconsulting.co.ke'
        if not settings.phone_2:
            settings.phone_2 = '+254729592895'
        if not settings.whatsapp_2:
            settings.whatsapp_2 = '+254729592895'
        settings.save()
        
        msg = "✅ CoreSettings created" if created else "✅ CoreSettings updated with partner 2 info"
        return HttpResponse(f"{msg}: {settings.site_name}")
    except Exception as e:
        return HttpResponse(f"❌ Error: {e}", status=500)


def populate_deadlines(request):
    """Populate tax deadlines from management command"""
    try:
        from django.core.management import call_command
        from apps.appointments.models import TaxDeadline
        
        # Only populate if empty
        if TaxDeadline.objects.count() > 0:
            return HttpResponse(f"✅ Tax deadlines already exist: {TaxDeadline.objects.count()} records")
        
        call_command('populate_tax_deadlines', verbosity=0)
        count = TaxDeadline.objects.count()
        return HttpResponse(f"✅ Tax deadlines populated: {count} records created")
    except Exception as e:
        return HttpResponse(f"❌ Error: {e}", status=500)


def populate_services(request):
    """Populate services from management command"""
    try:
        from django.core.management import call_command
        from apps.services.models import Service
        
        # Only populate if empty
        if Service.objects.count() > 0:
            return HttpResponse(f"✅ Services already exist: {Service.objects.count()} records")
        
        call_command('populate_services', verbosity=0)
        count = Service.objects.count()
        return HttpResponse(f"✅ Services populated: {count} records created")
    except Exception as e:
        return HttpResponse(f"❌ Error: {e}", status=500)


def populate_testimonials(request):
    """Populate testimonials from management command"""
    try:
        from django.core.management import call_command
        from apps.testimonials.models import Testimonial
        
        # Only populate if empty
        if Testimonial.objects.count() > 0:
            return HttpResponse(f"✅ Testimonials already exist: {Testimonial.objects.count()} records")
        
        call_command('populate_testimonials', verbosity=0)
        count = Testimonial.objects.count()
        return HttpResponse(f"✅ Testimonials populated: {count} records created")
    except Exception as e:
        return HttpResponse(f"❌ Error: {e}", status=500)


def testimonials_debug(request):
    """Debug testimonials - check database and table"""
    try:
        import json
        from apps.testimonials.models import Testimonial
        
        # Check if table exists
        debug_info = {}
        
        # Check count
        count = Testimonial.objects.count()
        debug_info['count'] = count
        debug_info['status'] = 'OK' if count > 0 else 'NO DATA'
        
        if count > 0:
            # List testimonials
            testimonials = list(Testimonial.objects.values('id', 'client_name', 'is_published', 'is_featured'))
            debug_info['testimonials'] = testimonials
        
        debug_info['message'] = "Testimonials table exists and is queryable"
        
        html = f"<h2>Testimonials Debug Report</h2><pre>{json.dumps(debug_info, indent=2)}</pre>"
        return HttpResponse(html, content_type='text/html')
    except Exception as e:
        return HttpResponse(f"❌ Error accessing testimonials: {type(e).__name__}: {str(e)}", status=500, content_type='text/html')


def home(request):
    """Homepage view"""
    try:
        settings = CoreSettings.objects.first()
    except Exception as e:
        return HttpResponse(f"Error loading settings: {e}")
    
    # Get upcoming tax deadlines and group them
    try:
        from apps.appointments.models import TaxDeadline
        from datetime import date
        
        # Get all upcoming deadlines
        all_deadlines = TaxDeadline.objects.filter(
            deadline_date__gte=date.today()
        ).order_by('deadline_date')
        
        # Group PAYE, VAT, and Excise Duty (assume same deadline), keep Income Tax separate
        grouped_deadlines = []
        processed_dates = set()
        
        for deadline in all_deadlines:
            deadline_key = deadline.deadline_date
            
            # Skip if we've already added a deadline for this date
            if deadline_key in processed_dates:
                continue
            
            # For non-income-tax deadlines, group them as "PAYE & VAT"
            if deadline.deadline_type == 'income_tax':
                # Keep income tax as is
                grouped_deadlines.append(deadline)
                processed_dates.add(deadline_key)
            else:
                # Create a pseudo-deadline for grouped "PAYE & VAT" or other
                if deadline.deadline_type in ['paye', 'vat', 'excise_duty', 'other']:
                    grouped_deadlines.append(deadline)
                    processed_dates.add(deadline_key)
            
            # Only keep first 2 distinct deadlines
            if len(grouped_deadlines) >= 2:
                break
        
        upcoming_deadlines = grouped_deadlines[:2]
    except Exception as e:
        print(f"Error loading deadlines: {e}")
        upcoming_deadlines = []
    
    context = {
        'settings': settings,
        'upcoming_deadlines': upcoming_deadlines,
        'featured_testimonials': [],
    }
    
    try:
        return render(request, 'core/home.html', context)
    except Exception as e:
        return HttpResponse(f"Error rendering template: {type(e).__name__}: {str(e)[:500]}")


def page_detail(request, slug):
    """Display static page"""
    page = Page.objects.get(slug=slug, is_published=True)
    context = {
        'page': page,
    }
    return render(request, 'core/page_detail.html', context)


def about(request):
    """About page view"""
    context = {
        'page_title': 'About HS Consulting',
    }
    return render(request, 'core/about.html', context)
