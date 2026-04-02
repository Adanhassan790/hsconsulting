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
