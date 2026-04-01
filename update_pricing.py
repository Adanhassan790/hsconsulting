import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from apps.services.models import Service

print("Updating all services to 'Contact for Pricing'...\n")

services = Service.objects.all()

for service in services:
    service.price_label = 'Contact for Pricing'
    service.save()
    print(f"✓ Updated: {service.name}")

print(f"\nDone! All {services.count()} services now show 'Contact for Pricing'")
