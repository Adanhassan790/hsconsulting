from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Startup initialization'

    def handle(self, *args, **options):
        print('\n' + '='*80)
        print('STARTUP SEQUENCE')
        print('='*80 + '\n')
        
        # Run migrations (should already be done, but just in case)
        print('[1/3] Running any remaining migrations...')
        try:
            call_command('migrate', '--noinput', verbosity=0)
            print('✓ Migrations complete\n')
        except Exception as e:
            print(f'⚠ Migration issue: {e}\n')
        
        # Create superuser if missing
        print('[2/3] Ensuring superuser exists...')
        try:
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@hsconsulting.co.ke',
                    password='Admin@123'
                )
                print('✓ Superuser admin created\n')
            else:
                print('✓ Superuser admin exists\n')
        except Exception as e:
            print(f'⚠ Superuser: {e}\n')
        
        # Initialize minimal data
        print('[3/3] Initializing application data...')
        try:
            from apps.core.models import CoreSettings
            settings, _ = CoreSettings.objects.get_or_create(pk=1, defaults={
                'site_name': 'HS Consulting',
                'email': 'info@hsconsulting.co.ke',
                'phone': '+254729592895',
                'email_2': 'admin@hsconsulting.co.ke',
                'phone_2': '+254746645534',
                'address': 'Nairobi, Kenya',
                'city': 'Nairobi',
                'country': 'Kenya',
                'linkedin_url': 'https://www.linkedin.com/company/hsconsulting-ke/',
                'twitter_url': 'https://twitter.com/hsconsulting',
                'instagram_url': 'https://www.instagram.com/hsconsulting_ke/',
                'facebook_url': 'https://www.facebook.com/hsconsulting.ke/',
                'whatsapp_message': 'Hello! I would like to inquire about your services.',
            })
            print('✓ Core settings initialized\n')
        except Exception as e:
            print(f'⚠ Settings: {e}\n')
        
        print('='*80)
        print('✅ STARTUP COMPLETE - Ready to serve requests')
        print('='*80 + '\n')
