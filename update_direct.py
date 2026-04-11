#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.core.models import CoreSettings

print("Fetching CoreSettings...")
settings = CoreSettings.objects.get(pk=1)

print("Current values:")
print(f"  Twitter: {repr(settings.twitter_url)}")
print(f"  Instagram: {repr(settings.instagram_url)}")
print(f"  Facebook: {repr(settings.facebook_url)}")
print(f"  LinkedIn: {repr(settings.linkedin_url)}")

print("\nUpdating URLs...")
settings.twitter_url = 'https://twitter.com/hs_consulting'
settings.instagram_url = 'https://www.instagram.com/hs_consulting_ke/'
settings.facebook_url = 'https://www.facebook.com/hs.consulting.ke/'
settings.linkedin_url = 'https://www.linkedin.com/company/hs-consulting-ke/'

print("Calling full_clean()...")
try:
    settings.full_clean()
    print("✓ Validation passed")
except Exception as e:
    print(f"⚠ Validation issue: {e}")

print("Saving...")
settings.save()
print("✓ Saved to database")

print("\nVerifying...")
updated = CoreSettings.objects.get(pk=1)
print(f"  Twitter: {repr(updated.twitter_url)}")
print(f"  Instagram: {repr(updated.instagram_url)}")
print(f"  Facebook: {repr(updated.facebook_url)}")
print(f"  LinkedIn: {repr(updated.linkedin_url)}")
print("\n✅ Done!")
