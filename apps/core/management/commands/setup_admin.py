#!/usr/bin/env python
"""
Django management command to set up admin user with password from environment variable
Run with: python manage.py setup_admin
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decouple import config


class Command(BaseCommand):
    help = 'Create or update admin superuser with password from ADMIN_PASSWORD env var'

    def handle(self, *args, **options):
        admin_password = config('ADMIN_PASSWORD', default='ChangeMeInProduction123!')
        
        try:
            admin = User.objects.get(username='admin')
            # Update existing admin password
            admin.set_password(admin_password)
            admin.save()
            self.stdout.write(self.style.SUCCESS('✓ Admin password updated'))
        except User.DoesNotExist:
            # Create new admin user
            User.objects.create_superuser('admin', 'admin@hsconsulting.co.ke', admin_password)
            self.stdout.write(self.style.SUCCESS('✓ Admin superuser created'))
        
        self.stdout.write(self.style.SUCCESS('Done!'))
