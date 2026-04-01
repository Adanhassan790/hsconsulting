#!/usr/bin/env python
"""Update CoreSettings with partner contact information"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.core.models import CoreSettings

def update_contact_info():
    """Update CoreSettings with both partner contact information"""
    try:
        settings = CoreSettings.objects.first()
        
        if not settings:
            print("✗ CoreSettings not found. Please create one first.")
            return
        
        # Update primary partner info
        settings.email = 'hsconsulting.co.ke'
        settings.email_2 = 'ibrahimhussein481@gmail.com'
        settings.phone = '0729592895'
        settings.whatsapp = '0729592895'
        settings.phone_2 = '0746645534'
        settings.whatsapp_2 = '0746645534'
        
        settings.save()
        
        print("✓ Contact info updated successfully:")
        print(f"  Primary Email: {settings.email}")
        print(f"  Secondary Email: {settings.email_2}")
        print(f"  Primary Phone/WhatsApp: {settings.phone}")
        print(f"  Secondary Phone/WhatsApp: {settings.phone_2}")
        
    except Exception as e:
        print(f"✗ Error updating contact info: {e}")

if __name__ == '__main__':
    update_contact_info()
