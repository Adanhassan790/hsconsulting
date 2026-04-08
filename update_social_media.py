#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.core.models import CoreSettings

settings = CoreSettings.objects.first()
if settings:
    print("Updating CoreSettings with social media URLs...")
    settings.twitter_url = 'https://twitter.com/hs_consulting'
    settings.instagram_url = 'https://www.instagram.com/hs_consulting_ke/'
    settings.facebook_url = 'https://www.facebook.com/hs.consulting.ke/'
    settings.linkedin_url = 'https://www.linkedin.com/company/hs-consulting-ke/'
    settings.whatsapp_message = 'Hello! I would like to inquire about your services.'
    settings.save()
    print("✓ Social media URLs updated successfully!")
    print(f"  Twitter: {settings.twitter_url}")
    print(f"  Instagram: {settings.instagram_url}")
    print(f"  Facebook: {settings.facebook_url}")
    print(f"  LinkedIn: {settings.linkedin_url}")
else:
    print("No CoreSettings found - creating one...")
    CoreSettings.objects.create(
        site_name='HS Consulting',
        email='info@hsconsulting.co.ke',
        phone='+254729592895',
        address='Nairobi, Kenya',
        city='Nairobi',
        country='Kenya',
        twitter_url='https://twitter.com/hs_consulting',
        instagram_url='https://www.instagram.com/hs_consulting_ke/',
        facebook_url='https://www.facebook.com/hs.consulting.ke/',
        linkedin_url='https://www.linkedin.com/company/hs-consulting-ke/',
        whatsapp_message='Hello! I would like to inquire about your services.'
    )
    print("✓ CoreSettings created with social media URLs!")
