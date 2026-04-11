#!/usr/bin/env python
"""
Setup script to configure CoreSettings for production deployment
Run with: python manage.py shell < setup_core_settings.py
"""
import os
from apps.core.models import CoreSettings

# Get or create CoreSettings
settings, created = CoreSettings.objects.get_or_create(pk=1)

# Site Information
settings.site_name = 'HS Consulting'
settings.tagline = 'Your Trusted Tax Consultation Partner'
settings.about_us = '''HS Consulting is a leading tax and financial consulting firm in Kenya. 
We provide comprehensive tax solutions, financial advisory, and business consulting services to individuals and corporations.'''
settings.mission = '''To deliver exceptional tax consulting and financial advisory services that empower our clients 
to make informed decisions and achieve their business objectives.'''

# Primary Partner Contact (Partner 1)
settings.email = 'info@hsconsulting.co.ke'
settings.phone = '+254729592895'
settings.whatsapp = '+254729592895'

# Secondary Partner Contact (Partner 2)
settings.email_2 = 'ibrahimhussein481@gmail.com'
settings.phone_2 = '+254746645534'
settings.whatsapp_2 = '+254729592895'

# Social Media URLs
# ADD YOUR SOCIAL MEDIA LINKS HERE:
settings.linkedin_url = 'https://www.linkedin.com/company/hsconsulting'  # Update with actual link
settings.twitter_url = 'https://twitter.com/hsconsulting'  # Update with actual link
settings.instagram_url = 'https://www.instagram.com/hsconsulting'  # Update with actual link
settings.facebook_url = 'https://www.facebook.com/hsconsulting'  # Update with actual link

# WhatsApp Message Template
settings.whatsapp_message = 'Hello! I would like to inquire about your services.'

# Address Information
settings.address = 'Nairobi, Kenya'
settings.city = 'Nairobi'
settings.country = 'Kenya'

# Save the settings
settings.save()

print("✓ CoreSettings configured successfully!")
print(f"  Site: {settings.site_name}")
print(f"  Email 1: {settings.email}")
print(f"  Email 2: {settings.email_2}")
print(f"  Phone 1: {settings.phone}")
print(f"  Phone 2: {settings.phone_2}")
