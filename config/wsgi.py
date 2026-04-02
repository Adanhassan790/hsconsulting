"""
WSGI config for HS Consulting project.
"""

import os
import sys

from django.core.wsgi import get_wsgi_application
from django.core.management import call_command
from django.db import connection, connections
from django.db.utils import OperationalError, ProgrammingError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialize Django
application = get_wsgi_application()

# Run startup tasks ONLY in production (when DATABASE_URL is set)
if os.environ.get('DATABASE_URL'):
    try:
        # Check if we can connect to database
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        print("=" * 60, file=sys.stderr)
        print("STARTUP: Database connected, running initialization...", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        
        # Run migrations - CRITICAL for database setup
        try:
            print("STARTUP: Running migrations...", file=sys.stderr)
            call_command('migrate', '--noinput', verbosity=1)
            print("✓ STARTUP: Migrations completed", file=sys.stderr)
        except Exception as e:
            print(f"⚠ STARTUP: Migration warning: {type(e).__name__}: {str(e)[:150]}", file=sys.stderr)
        
        # Try to create superuser
        try:
            from django.contrib.auth.models import User
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@hsconsulting.co.ke',
                    password='Admin@123'
                )
                print("✓ STARTUP: Superuser created", file=sys.stderr)
        except Exception as e:
            print(f"⚠ STARTUP: Superuser creation issue: {e}", file=sys.stderr)
        
        # Initialize CoreSettings
        try:
            from apps.core.models import CoreSettings
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
                    'email_2': 'admin@hsconsulting.co.ke',
                    'phone_2': '+254729592895',
                    'whatsapp_2': '+254729592895',
                    'address': 'Nairobi, Kenya',
                    'city': 'Nairobi',
                    'country': 'Kenya'
                }
            )
            if created:
                print("✓ STARTUP: CoreSettings initialized", file=sys.stderr)
            else:
                # Update if partner 2 info is missing
                if not settings.email_2:
                    settings.email_2 = 'admin@hsconsulting.co.ke'
                    settings.phone_2 = '+254729592895'
                    settings.whatsapp_2 = '+254729592895'
                    settings.save()
                    print("✓ STARTUP: CoreSettings updated", file=sys.stderr)
        except Exception as e:
            print(f"⚠ STARTUP: CoreSettings error: {type(e).__name__}: {str(e)[:150]}", file=sys.stderr)
        
        # Try to populate tax deadlines
        try:
            from apps.appointments.models import TaxDeadline
            if TaxDeadline.objects.count() == 0:
                call_command('populate_tax_deadlines', verbosity=0)
                print("✓ STARTUP: Tax deadlines populated", file=sys.stderr)
        except ProgrammingError:
            print("⚠ STARTUP: Tax deadlines table not ready yet", file=sys.stderr)
        except Exception as e:
            print(f"⚠ STARTUP: Tax deadlines error: {type(e).__name__}", file=sys.stderr)
        
        # Try to populate services
        try:
            from apps.services.models import Service
            if Service.objects.count() == 0:
                call_command('populate_services', verbosity=0)
                print("✓ STARTUP: Services populated", file=sys.stderr)
        except ProgrammingError:
            print("⚠ STARTUP: Services table not ready yet", file=sys.stderr)
        except Exception as e:
            print(f"⚠ STARTUP: Services error: {type(e).__name__}", file=sys.stderr)
        
        # Try to populate testimonials
        try:
            from apps.testimonials.models import Testimonial
            if Testimonial.objects.count() == 0:
                call_command('populate_testimonials', verbosity=0)
                print("✓ STARTUP: Testimonials populated", file=sys.stderr)
        except ProgrammingError:
            print("⚠ STARTUP: Testimonials table not ready yet", file=sys.stderr)
        except Exception as e:
            print(f"⚠ STARTUP: Testimonials error: {type(e).__name__}", file=sys.stderr)
        
        print("=" * 60, file=sys.stderr)
        print("STARTUP: Initialization complete", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
    
    except OperationalError as e:
        print(f"✗ STARTUP: Database connection failed: {e}", file=sys.stderr)
    except Exception as e:
        print(f"✗ STARTUP: Unexpected error: {type(e).__name__}: {e}", file=sys.stderr)
