#!/usr/bin/env python
"""Populate Kenyan tax deadlines for 2026"""
print("Starting tax deadlines population script...")

import os
import django
from datetime import date, datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.appointments.models import TaxDeadline

def populate_tax_deadlines():
    """Populate Kenyan tax deadlines for 2026"""
    
    try:
        # Clear existing deadlines
        TaxDeadline.objects.all().delete()
        print("✓ Cleared existing deadlines")
        
        # First deadline for testing
        deadline1 = TaxDeadline.objects.create(
            name='PAYE Due',
            description='PAYE (Pay As You Earn) tax payments and returns due',
            deadline_date=date(2026, 4, 10),
            deadline_type='paye',
            recurring=True,
        )
        print(f"✓ Created: {deadline1.name}")
        
        deadline2 = TaxDeadline.objects.create(
            name='VAT Filing',
            description='Monthly VAT returns submission deadline',
            deadline_date=date(2026, 4, 20),
            deadline_type='vat',
            recurring=True,
        )
        print(f"✓ Created: {deadline2.name}")
        
        deadline3 = TaxDeadline.objects.create(
            name='Income Tax Filing',
            description='Annual income tax return filing deadline for individuals',
            deadline_date=date(2026, 6, 30),
            deadline_type='income_tax',
            recurring=True,
        )
        print(f"✓ Created: {deadline3.name}")
        
        deadline4 = TaxDeadline.objects.create(
            name='Corporate Tax Filing',
            description='Corporate tax returns submission deadline',
            deadline_date=date(2026, 5, 31),
            deadline_type='income_tax',
            recurring=True,
        )
        print(f"✓ Created: {deadline4.name}")
        
        deadline5 = TaxDeadline.objects.create(
            name='Withholding Tax Returns',
            description='Submit withholding tax statements and payments',
            deadline_date=date(2026, 4, 15),
            deadline_type='other',
            recurring=True,
        )
        print(f"✓ Created: {deadline5.name}")
        
        print("\n✓ Successfully populated tax deadlines")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    populate_tax_deadlines()
