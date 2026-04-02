from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
from django.db import connection
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = 'Run startup tasks: migrations, static files, superuser creation'

    def handle(self, *args, **options):
        """Execute all startup tasks"""
        
        # Check database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            self.stdout.write(self.style.SUCCESS('✓ Database connected'))
        except OperationalError as e:
            self.stdout.write(self.style.ERROR(f'✗ Database connection failed: {e}'))
            return
        
        # Create any missing migrations
        try:
            self.stdout.write('Creating missing migrations...')
            call_command('makemigrations', '--noinput', verbosity=0)
            self.stdout.write(self.style.SUCCESS('✓ Migrations created/updated'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠ Makemigrations warning: {e}'))
        
        # Run migrations
        try:
            self.stdout.write('Running migrations...')
            call_command('migrate', '--noinput', verbosity=1)
            self.stdout.write(self.style.SUCCESS('✓ Migrations applied'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Migration error: {e}'))
            return
        
        # Collect static files
        try:
            self.stdout.write('Collecting static files...')
            call_command('collectstatic', '--noinput', verbosity=0)
            self.stdout.write(self.style.SUCCESS('✓ Static files collected'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠ Collectstatic warning: {e}'))
        
        # Create superuser if it doesn't exist
        try:
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@hsconsulting.co.ke',
                    password='Admin@123'
                )
                self.stdout.write(self.style.SUCCESS('✓ Superuser admin created'))
            else:
                self.stdout.write(self.style.SUCCESS('✓ Superuser admin already exists'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠ Superuser warning: {e}'))
        
        self.stdout.write(self.style.SUCCESS('\n✓✓✓ All startup tasks completed! ✓✓✓'))
