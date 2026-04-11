#!/usr/bin/env python
"""Reset migrations and recreate database"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from django.core.management import call_command

print("Clearing migration history...")
try:
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM django_migrations WHERE app='core'")
        cursor.execute("DELETE FROM django_migrations WHERE app='admin_dashboard'")
        cursor.execute("DELETE FROM django_migrations WHERE app='appointments'")
        cursor.execute("DELETE FROM django_migrations WHERE app='blog'")
        cursor.execute("DELETE FROM django_migrations WHERE app='careers'")
        cursor.execute("DELETE FROM django_migrations WHERE app='clients'")
        cursor.execute("DELETE FROM django_migrations WHERE app='inquiries'")
        cursor.execute("DELETE FROM django_migrations WHERE app='services'")
        cursor.execute("DELETE FROM django_migrations WHERE app='testimonials'")
    print("✓ Migration history cleared")
except Exception as e:
    print(f"Note: {e}")

print("\nRunning all migrations...")
try:
    call_command('migrate', '--noinput', verbosity=2)
    print("✓ Migrations completed successfully")
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)

print("\nDatabase tables recreated!")
