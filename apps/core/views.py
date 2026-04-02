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
    """Initialize CoreSettings if empty"""
    try:
        if CoreSettings.objects.exists():
            return HttpResponse("✅ CoreSettings already initialized")
        
        # Create default CoreSettings
        settings = CoreSettings.objects.create(
            site_name='HS Consulting',
            tagline='Your trusted tax consultation partner',
            about_us='Leading tax consultation firm in Kenya',
            mission='To provide comprehensive tax solutions',
            email='info@hsconsulting.co.ke',
            phone='+254729592895',
            whatsapp='+254729592895',
            email_2='admin@hsconsulting.co.ke',
            phone_2='+254729592895',
            whatsapp_2='+254729592895',
            address='Nairobi, Kenya',
            city='Nairobi',
            country='Kenya'
        )
        return HttpResponse(f"✅ CoreSettings initialized: {settings.site_name}")
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


def home(request):
    """Homepage view"""
    try:
        settings = CoreSettings.objects.first()
    except Exception as e:
        return HttpResponse(f"Error loading settings: {e}")
    
    # Get upcoming tax deadlines
    try:
        from apps.appointments.models import TaxDeadline
        from datetime import date
        upcoming_deadlines = TaxDeadline.objects.filter(
            deadline_date__gte=date.today()
        ).order_by('deadline_date')[:5]  # Get top 5 upcoming deadlines
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
