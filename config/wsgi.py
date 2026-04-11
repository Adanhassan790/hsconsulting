"""
WSGI config for HS Consulting project.
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application
from django.core.management import call_command
from django.db import connection, connections
from django.db.utils import OperationalError, ProgrammingError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Ensure staticfiles directory exists (needed for WhiteNoise middleware)
from django.conf import settings as django_settings
static_root = Path(django_settings.STATIC_ROOT)
static_root.mkdir(parents=True, exist_ok=True)

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
            from django.db import connection
            
            # Verify table exists before querying
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='core_coresettings';"
                )
                table_exists = cursor.fetchone() is not None
            
            if not table_exists:
                print("⚠ STARTUP: CoreSettings table not found, skipping initialization", file=sys.stderr)
            else:
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
                if created:
                    print("✓ STARTUP: CoreSettings initialized", file=sys.stderr)
                else:
                    # Update if partner 2 info is missing
                    if not settings.email_2:
                        settings.email_2 = 'ibrahimhussein481@gmail.com'
                        settings.phone_2 = '+254746645534'
                        settings.whatsapp_2 = '+254729592895'
                        settings.save()
                        print("✓ STARTUP: CoreSettings updated", file=sys.stderr)
        except (OperationalError, ProgrammingError) as e:
            print(f"⚠ STARTUP: CoreSettings DB error (table not ready): {type(e).__name__}", file=sys.stderr)
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
