#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.core.models import CoreSettings

settings = CoreSettings.objects.get(pk=1)
print("Current database values:")
print(f"  Twitter: '{settings.twitter_url}'")
print(f"  Instagram: '{settings.instagram_url}'")
print(f"  Facebook: '{settings.facebook_url}'")
print(f"  LinkedIn: '{settings.linkedin_url}'")
