import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from apps.core.models import CoreSettings

settings = CoreSettings.objects.first()
if settings:
    settings.phone = '0729592895'
    settings.email = 'ibrahimhussein481@gmail.com'
    settings.whatsapp = '0746645534'
    settings.save()
    print('✓ Contact info updated:')
    print(f'  Email: {settings.email}')
    print(f'  Phone: {settings.phone}')
    print(f'  WhatsApp: {settings.whatsapp}')
else:
    print('✗ CoreSettings not found. Creating...')
    CoreSettings.objects.create(
        phone='0729592895',
        email='ibrahimhussein481@gmail.com',
        whatsapp='0746645534',
        about_us='HS Consulting - Professional Tax and Financial Solutions',
        mission='To simplify tax compliance for businesses in Kenya',
        address='Nairobi, Kenya',
        city='Nairobi'
    )
    print('✓ CoreSettings created with new contact info')
