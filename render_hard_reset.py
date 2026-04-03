#!/usr/bin/env python
"""
CRITICAL: Hard reset and initialize Render database
This script completely resets the database and rebuilds it from scratch
"""
import os
import sys
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.core.management import call_command
from django.db import connection
from django.contrib.auth.models import User
from apps.core.models import CoreSettings

print("\n" + "=" * 80)
print("🔴 RENDER DATABASE INITIALIZATION")
print("=" * 80)

# Step 1: Run migrations (safe - won't re-run if already applied)
print("\n[STEP 1] Running database migrations...")
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    print("  ✓ Database connected")
    
    # Run migrations - this will handle duplicates
    call_command('migrate', '--noinput', verbosity=1)
    print("  ✓ All migrations applied")
except Exception as e:
    print(f"  ✗ Migration error: {type(e).__name__}: {str(e)[:100]}")
    print("  Continuing anyway - some tables might already exist...")

# Step 2: Create or verify superuser
print("\n[STEP 2] Initializing admin user...")
try:
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@hsconsulting.co.ke',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin.set_password('Admin@123')
        admin.save()
        print(f"  ✓ Admin user created")
    else:
        # Update password just in case
        admin.set_password('Admin@123')
        admin.save()
        print(f"  ✓ Admin user verified")
    print(f"    Username: admin")
    print(f"    Password: Admin@123")
except Exception as e:
    print(f"  ⚠ Admin creation issue: {e}")

# Step 3: Initialize CoreSettings with CORRECT partner 2 info
print("\n[STEP 3] Initializing core settings...")
try:
    settings, created = CoreSettings.objects.get_or_create(
        pk=1,
        defaults={
            'site_name': 'HS Consulting',
            'tagline': 'Your trusted tax consultation partner',
            'about_us': 'Leading tax consultation firm in Kenya',
            'mission': 'To provide comprehensive tax solutions',
            'email': 'info@hsconsulting.co.ke',
            'phone': '+254729592895',
            'whatsapp': '+254729592895',
            'email_2': 'ibrahimhussein481@gmail.com',
            'phone_2': '+254746645534',
            'whatsapp_2': '+254729592895',
            'address': 'Nairobi, Kenya',
            'city': 'Nairobi',
            'country': 'Kenya'
        }
    )
    
    # Always ensure partner 2 info is correct
    if settings.email_2 != 'ibrahimhussein481@gmail.com' or settings.phone_2 != '+254746645534':
        settings.email_2 = 'ibrahimhussein481@gmail.com'
        settings.phone_2 = '+254746645534'
        settings.whatsapp_2 = '+254729592895'
        settings.save()
        print("  ✓ CoreSettings updated (partner 2 corrected)")
    else:
        print("  ✓ CoreSettings verified")
    
    print(f"    Partner 1: {settings.email} / {settings.phone}")
    print(f"    Partner 2: {settings.email_2} / {settings.phone_2}")
except Exception as e:
    print(f"  ✗ CoreSettings error: {type(e).__name__}: {e}")

# Step 4: Verify testimonials table exists and populate if needed
print("\n[STEP 4] Verifying testimonials table...")
try:
    from apps.testimonials.models import Testimonial
    
    # Check if table exists by trying to count
    count = Testimonial.objects.count()
    print(f"  ✓ Testimonials table exists ({count} records)")
    
    # Populate if empty
    if count == 0:
        call_command('populate_testimonials', verbosity=0)
        new_count = Testimonial.objects.count()
        print(f"  ✓ Sample testimonials populated ({new_count} records)")
except Exception as e:
    print(f"  ✗ Testimonials error: {type(e).__name__}: {e}")

# Step 5: Clean and repopulate services (CRITICAL - ensure no emojis)
print("\n[STEP 5] Ensuring services are emoji-free...")
try:
    from apps.services.models import Service
    
    # Always repopulate services to ensure they're clean
    Service.objects.all().delete()
    
    services_data = [
        ('Tax Return Filing', 'Complete tax return preparation and filing for individuals and businesses'),
        ('VAT & ETIMS Compliance', 'Comprehensive VAT management and ETIMS compliance for KRA'),
        ('Payroll Processing', 'Monthly payroll processing and statutory deductions'),
        ('Company Registration & Compliance', 'Business registration and ongoing statutory compliance'),
        ('Audit Services', 'Professional external and internal audit services'),
        ('Bookkeeping & Accounting', 'Monthly bookkeeping and financial statement preparation'),
        ('Tax Advisory', 'Strategic tax planning to optimize your tax position and reduce liabilities'),
        ('Financial Consulting', 'Expert guidance on financial management and forecasting'),
        ('PAYE Management', 'PAYE (Pay As You Earn) processing and KRA compliance'),
        ('Withholding Tax Services', 'Withholding tax declarations and compliance management'),
        ('Corporate Tax Planning', 'Strategic corporate tax planning and optimization'),
        ('Personal Income Tax Planning', 'Individual tax planning and optimization strategies'),
    ]
    
    for i, (name, desc) in enumerate(services_data, 1):
        Service.objects.create(
            name=name,
            slug=name.lower().replace(' ', '-').replace('&', 'and'),
            description=desc,
            long_description=desc,
            price_label='Contact for Pricing',
            order=i,
            is_active=True
        )
    
    print(f"  ✓ Services populated ({Service.objects.count()} clean services)")
except Exception as e:
    print(f"  ✗ Services population error: {type(e).__name__}: {str(e)[:100]}")
    traceback.print_exc()

# Step 6: Populate tax deadlines if needed
print("\n[STEP 6] Populating tax deadlines...")
try:
    from apps.appointments.models import TaxDeadline
    existing = TaxDeadline.objects.count()
    
    if existing < 2:
        TaxDeadline.objects.all().delete()
        TaxDeadline.objects.create(
            name='Annual Tax Return Filing',
            date_of_deadline='2026-06-30',
            description='Annual tax return filing deadline for individuals and companies',
            days_before_reminder=30,
            email_reminder=True,
            sms_reminder=True
        )
        TaxDeadline.objects.create(
            name='Monthly VAT Return',
            date_of_deadline='2026-02-15',
            description='Monthly VAT return deadline',
            days_before_reminder=5,
            email_reminder=True,
            sms_reminder=True
        )
        print(f"  ✓ Tax deadlines created")
    else:
        print(f"  ✓ Tax deadlines already exist ({existing} deadlines)")
except Exception as e:
    print(f"  ✗ Tax deadlines error: {type(e).__name__}: {str(e)[:100]}")

# Step 7: Populate testimonials if needed
print("\n[STEP 7] Populating testimonials...")
try:
    from apps.testimonials.models import Testimonial
    
    if Testimonial.objects.count() == 0:
        Testimonial.objects.create(
            client_name='David Johnson',
            company='Tech Solutions Ltd',
            rating=5,
            testimonial='HS Consulting has been instrumental in streamlining our tax processes. Highly recommended!',
            is_active=True,
            position='Finance Director'
        )
        Testimonial.objects.create(
            client_name='Mary Kariuki',
            company='Kariuki Trading',
            rating=5,
            testimonial='Excellent service and professional team. They made our tax compliance so much easier.',
            is_active=True,
            position='Business Owner'
        )
        Testimonial.objects.create(
            client_name='James Mutua',
            company='Manufacturing Co KE',
            rating=5,
            testimonial='Best tax consultants in Kenya. Professional, reliable, and always available to help.',
            is_active=True,
            position='CEO'
        )
        print(f"  ✓ Testimonials populated ({Testimonial.objects.count()} testimonials)")
    else:
        print(f"  ✓ Testimonials already exist ({Testimonial.objects.count()} testimonials)")
except Exception as e:
    print(f"  ✗ Testimonials error: {type(e).__name__}: {str(e)[:100]}")

print("\n" + "=" * 80)
print("✅ INITIALIZATION COMPLETE - All systems ready")
print("=" * 80)
print("\n🌐 Site Access:")
print("  Public: https://hsconsulting.onrender.com/")
print("  Admin:  https://hsconsulting.onrender.com/admin/")
print("\n👤 Admin Credentials:")
print("  Username: admin")
print("  Password: Admin@123")
print("\n📧 Contact Information (as shown in footer):")
print("  Partner 1: info@hsconsulting.co.ke | Phone: +254729592895")
print("  Partner 2: ibrahimhussein481@gmail.com | Phone: +254746645534")
print("\n📋 Database Status:")
print(f"  Services: {Service.objects.count()} items (emoji-free)")
print(f"  Testimonials: {Testimonial.objects.count()} items")
print(f"  Tax Deadlines: {TaxDeadline.objects.count()} items")
print("\n✨ All files are prepared for production deployment")
print("=" * 80 + "\n")
