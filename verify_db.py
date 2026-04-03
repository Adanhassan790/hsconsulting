import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.services.models import Service
from apps.core.models import CoreSettings
from apps.testimonials.models import Testimonial

print("\n" + "="*70)
print("LOCAL DATABASE VERIFICATION")
print("="*70)

# Check services
print("\n[1] Services Status:")
service_count = Service.objects.count()
print(f"  Total: {service_count}")
if service_count > 0:
    print("  Sample services:")
    for svc in Service.objects.all()[:3]:
        # Check for emojis
        has_emoji = any(ord(char) > 127 for char in svc.name)
        emoji_marker = " ❌ (HAS EMOJI)" if has_emoji else " ✓"
        print(f"    - {svc.name}{emoji_marker}")

# Check CoreSettings
print("\n[2] Core Settings (Partner Info):")
try:
    settings = CoreSettings.objects.get(pk=1)
    print(f"  Partner 1:")
    print(f"    Email: {settings.email}")
    print(f"    Phone: {settings.phone}")
    print(f"  Partner 2:")
    print(f"    Email: {settings.email_2}")
    print(f"    Phone: {settings.phone_2}")
except CoreSettings.DoesNotExist:
    print("  ⚠ CoreSettings not initialized")

# Check Testimonials
print("\n[3] Testimonials Status:")
testimonial_count = Testimonial.objects.count()
print(f"  Total: {testimonial_count}")
if testimonial_count > 0:
    sample = Testimonial.objects.first()
    print(f"  Sample: {sample.client_name} - {sample.rating} stars")

print("\n" + "="*70)
print("✅ VERIFICATION COMPLETE")
print("="*70 + "\n")
