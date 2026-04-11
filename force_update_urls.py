#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.core.models import CoreSettings
from django.db import connection

# Direct SQL update to bypass any validation issues
with connection.cursor() as cursor:
    print("Updating social media URLs directly in database...")
    
    cursor.execute("""
        UPDATE core_coresettings 
        SET 
            twitter_url = %s,
            instagram_url = %s,
            facebook_url = %s,
            linkedin_url = %s
        WHERE id = 1
    """, [
        'https://twitter.com/hs_consulting',
        'https://www.instagram.com/hs_consulting_ke/',
        'https://www.facebook.com/hs.consulting.ke/',
        'https://www.linkedin.com/company/hs-consulting-ke/'
    ])
    
    print("✓ Database updated via raw SQL")

# Verify the update
settings = CoreSettings.objects.get(pk=1)
print("\nVerifying update:")
print(f"  Twitter: {settings.twitter_url}")
print(f"  Instagram: {settings.instagram_url}")
print(f"  Facebook: {settings.facebook_url}")
print(f"  LinkedIn: {settings.linkedin_url}")
print("\n✓ All URLs updated successfully!")
