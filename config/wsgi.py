"""
WSGI config for HS Consulting project.
"""

import os
import sys

from django.core.wsgi import get_wsgi_application
from django.core.management import call_command
from django.db import connection
from django.db.utils import OperationalError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialize Django
application = get_wsgi_application()

# Run startup tasks ONLY in production (when DATABASE_URL is set)
if os.environ.get('DATABASE_URL'):
    try:
        # Check if we can connect to database
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Run migrations - CRITICAL for database setup
        try:
            print("Starting migrations...", file=sys.stderr)
            call_command('migrate', '--noinput', verbosity=2)
            print("✓ Migrations completed successfully", file=sys.stderr)
        except Exception as e:
            print(f"⚠ Attempted migration error: {type(e).__name__}: {str(e)[:200]}", file=sys.stderr)
            # Continue anyway - tables might already exist
        
        # Try to create superuser
        try:
            from django.contrib.auth.models import User
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@hsconsulting.co.ke',
                    password='Admin@123'
                )
                print("✓ Superuser created", file=sys.stderr)
        except Exception as e:
            print(f"⚠ Superuser error: {e}", file=sys.stderr)
        
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
                print("✓ CoreSettings initialized", file=sys.stderr)
            else:
                # Update if partner 2 info is missing
                if not settings.email_2:
                    settings.email_2 = 'admin@hsconsulting.co.ke'
                    settings.phone_2 = '+254729592895'
                    settings.whatsapp_2 = '+254729592895'
                    settings.save()
                    print("✓ CoreSettings updated with partner 2 info", file=sys.stderr)
        except Exception as e:
            print(f"⚠ CoreSettings error: {e}", file=sys.stderr)
        
        # Try to populate tax deadlines
        try:
            from apps.appointments.models import TaxDeadline
            if TaxDeadline.objects.count() == 0:
                call_command('populate_tax_deadlines', verbosity=0)
                print("✓ Tax deadlines populated", file=sys.stderr)
        except Exception as e:
            print(f"⚠ Tax deadline population error: {e}", file=sys.stderr)
        
        # Try to populate services
        try:
            from apps.services.models import Service
            if Service.objects.count() == 0:
                call_command('populate_services', verbosity=0)
                print("✓ Services populated", file=sys.stderr)
        except Exception as e:
            print(f"⚠ Services population error: {e}", file=sys.stderr)
        
        # Try to populate testimonials
        try:
            from apps.testimonials.models import Testimonial
            if Testimonial.objects.count() == 0:
                call_command('populate_testimonials', verbosity=0)
                print("✓ Testimonials populated", file=sys.stderr)
        except Exception as e:
            print(f"⚠ Testimonials population error: {e}", file=sys.stderr)
    
    except OperationalError as e:
        print(f"✗ Database connection failed: {e}", file=sys.stderr)
