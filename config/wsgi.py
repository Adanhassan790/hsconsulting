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
        
        # Try to run migrations
        try:
            # Use --fake-initial to handle cases where tables exist but migrations aren't recorded
            call_command('migrate', '--noinput', '--fake-initial', verbosity=0)
            print("✓ Migrations applied successfully", file=sys.stderr)
        except Exception as e:
            print(f"⚠ Migration error: {e}", file=sys.stderr)
        
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
    
    except OperationalError as e:
        print(f"✗ Database connection failed: {e}", file=sys.stderr)
