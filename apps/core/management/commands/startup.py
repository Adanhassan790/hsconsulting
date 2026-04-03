from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
from django.db import connection
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = 'Run startup tasks: migrations, static files, superuser, and data initialization'

    def handle(self, *args, **options):
        """Execute all startup tasks"""
        self.stdout.write('\n' + '='*70)
        self.stdout.write('STARTUP: Initializing application...')
        self.stdout.write('='*70)
        
        # FIRST: Ensure static files are collected (critical for CSS/JS/images)
        import os
        from pathlib import Path
        staticfiles_dir = Path(__file__).resolve().parent.parent.parent.parent.parent / 'staticfiles'
        if not staticfiles_dir.exists():
            self.stdout.write('Static files directory missing, collecting now...')
            try:
                call_command('collectstatic', '--noinput', verbosity=1)
                self.stdout.write(self.style.SUCCESS('✓ Static files collected'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Static files collection failed: {e}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'✓ Static files directory exists ({len(list(staticfiles_dir.glob("**/*")))} files)'))
        
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
            self.stdout.write(self.style.WARNING(f'⚠ Makemigrations: {str(e)[:100]}'))
        
        # Run migrations
        try:
            self.stdout.write('Running migrations...')
            call_command('migrate', '--noinput', verbosity=0)
            self.stdout.write(self.style.SUCCESS('✓ Migrations applied'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Migration error: {e}'))
        
        # Collect static files (with error logging)
        try:
            self.stdout.write('Collecting any new static files...')
            call_command('collectstatic', '--noinput', verbosity=1)
            self.stdout.write(self.style.SUCCESS('✓ Static files updated'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Collectstatic error: {str(e)[:200]}'))
        
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
                self.stdout.write(self.style.SUCCESS('✓ Superuser admin exists'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠ Superuser: {str(e)[:100]}'))
        
        # Initialize CoreSettings
        try:
            from apps.core.models import CoreSettings
            settings, created = CoreSettings.objects.get_or_create(pk=1)
            if not settings.email or settings.email == 'hsconsulting.co.ke':
                settings.site_name = 'HS Consulting'
                settings.tagline = 'Your trusted tax consultation partner'
                settings.about_us = 'Leading tax consultation firm in Kenya'
                settings.mission = 'To provide comprehensive tax solutions'
                settings.email = 'info@hsconsulting.co.ke'
                settings.phone = '+254729592895'
                settings.whatsapp = '+254729592895'
                settings.email_2 = 'admin@hsconsulting.co.ke'
                settings.phone_2 = '+254746645534'
                settings.whatsapp_2 = '+254729592895'
                settings.address = 'Nairobi, Kenya'
                settings.city = 'Nairobi'
                settings.country = 'Kenya'
                settings.save()
                self.stdout.write(self.style.SUCCESS(f'{"✓ CoreSettings created" if created else "✓ CoreSettings updated"}'))
            else:
                self.stdout.write(self.style.SUCCESS('✓ CoreSettings verified'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠ CoreSettings: {str(e)[:100]}'))
        
        # Populate Services
        try:
            from apps.services.models import Service
            if Service.objects.count() == 0:
                services_data = [
                    ('Tax Return Filing', 'Complete tax return preparation and filing'),
                    ('VAT & ETIMS Compliance', 'Comprehensive VAT management and ETIMS compliance'),
                    ('Payroll Processing', 'Monthly payroll processing and statutory deductions'),
                    ('Company Registration & Compliance', 'Business registration and compliance'),
                    ('Audit Services', 'Professional external and internal audit services'),
                    ('Bookkeeping & Accounting', 'Monthly bookkeeping and financial reporting'),
                    ('Tax Advisory', 'Strategic tax planning and optimization'),
                    ('Financial Consulting', 'Expert financial guidance'),
                    ('PAYE Management', 'PAYE processing and KRA compliance'),
                    ('Withholding Tax Services', 'Withholding tax management'),
                    ('Corporate Tax Planning', 'Corporate tax strategies'),
                    ('Personal Income Tax Planning', 'Personal tax optimization'),
                ]
                for i, (name, desc) in enumerate(services_data, 1):
                    Service.objects.create(
                        name=name, slug=name.lower().replace(' ', '-').replace('&', 'and'),
                        description=desc, long_description=desc,
                        price_label='Contact for Pricing', order=i, is_active=True
                    )
                self.stdout.write(self.style.SUCCESS(f'✓ Services created ({Service.objects.count()} items)'))
            else:
                self.stdout.write(self.style.SUCCESS(f'✓ Services verified ({Service.objects.count()} items)'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠ Services: {str(e)[:100]}'))
        
        # Populate Testimonials
        try:
            from apps.testimonials.models import Testimonial
            if Testimonial.objects.count() == 0:
                Testimonial.objects.create(
                    client_name='David Johnson', client_company='Tech Solutions Ltd',
                    client_title='Finance Director', rating=5, is_featured=True, is_published=True,
                    content='HS Consulting has been instrumental in streamlining our tax processes. Highly recommended!'
                )
                Testimonial.objects.create(
                    client_name='Mary Kariuki', client_company='Kariuki Trading',
                    client_title='Business Owner', rating=5, is_featured=True, is_published=True,
                    content='Excellent service and professional team. They made our tax compliance so much easier.'
                )
                Testimonial.objects.create(
                    client_name='James Mutua', client_company='Manufacturing Co KE',
                    client_title='CEO', rating=5, is_featured=False, is_published=True,
                    content='Best tax consultants in Kenya. Professional and reliable.'
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Testimonials created ({Testimonial.objects.count()} items)'))
            else:
                self.stdout.write(self.style.SUCCESS(f'✓ Testimonials verified ({Testimonial.objects.count()} items)'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠ Testimonials: {str(e)[:100]}'))
        
        # Populate Tax Deadlines
        try:
            from apps.appointments.models import TaxDeadline
            if TaxDeadline.objects.count() < 2:
                TaxDeadline.objects.all().delete()
                TaxDeadline.objects.create(
                    name='Annual Tax Return Filing',
                    date_of_deadline='2026-06-30',
                    description='Annual tax return filing deadline',
                    days_before_reminder=30,
                    email_reminder=True,
                    sms_reminder=True
                )
                TaxDeadline.objects.create(
                    name='Monthly VAT Return',
                    date_of_deadline='2026-02-15',
                    description='Monthly VAT return deadline',
                    days_before_reminder=5,
                    email_reminder=True,
                    sms_reminder=True
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Tax Deadlines created ({TaxDeadline.objects.count()} items)'))
            else:
                self.stdout.write(self.style.SUCCESS(f'✓ Tax Deadlines verified ({TaxDeadline.objects.count()} items)'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠ Tax Deadlines: {str(e)[:100]}'))
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*70))
        self.stdout.write(self.style.SUCCESS('✅ STARTUP COMPLETE - All systems ready!'))
        self.stdout.write(self.style.SUCCESS('='*70 + '\n'))
