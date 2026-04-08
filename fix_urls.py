#!/usr/bin/env python
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.core.models import CoreSettings

# Update directly with correct URLs
settings = CoreSettings.objects.filter(pk=1).first()
if settings:
    print("Updating CoreSettings with correct URL formats...")
    settings.twitter_url = 'https://twitter.com/hs_consulting'
    settings.instagram_url = 'https://www.instagram.com/hs_consulting_ke/'
    settings.facebook_url = 'https://www.facebook.com/hs.consulting.ke/'
    settings.linkedin_url = 'https://www.linkedin.com/company/hs-consulting-ke/'
    settings.save()
    
    # Verify the update
    updated = CoreSettings.objects.get(pk=1)
    print("\n✓ URLs Updated Successfully!")
    print(f"  Twitter: {updated.twitter_url}")
    print(f"  Instagram: {updated.instagram_url}")
    print(f"  Facebook: {updated.facebook_url}")
    print(f"  LinkedIn: {updated.linkedin_url}")
else:
    print("No CoreSettings found!")
