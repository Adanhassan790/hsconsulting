"""
Fixture to populate Kenyan Tax Calendar
Load with: python manage.py loaddata kenyan_tax_calendar.json
"""

import json
from datetime import date

# Create JSON fixture for Kenyan tax deadlines
fixtures = [
    {
        "model": "appointments.taxdeadline",
        "pk": 1,
        "fields": {
            "name": "Monthly VAT Return - Due",
            "description": "Submit monthly Value Added Tax (VAT) return to KRA",
            "deadline_date": "2026-02-20",
            "deadline_type": "vat",
            "recurring": True,
            "next_deadline": "2026-03-20"
        }
    },
    {
        "model": "appointments.taxdeadline",
        "pk": 2,
        "fields": {
            "name": "Monthly PAYE/WCF - Due",
            "description": "Submit monthly PAYE (Pay As You Earn) and Withholding Tax returns",
            "deadline_date": "2026-02-10",
            "deadline_type": "paye",
            "recurring": True,
            "next_deadline": "2026-03-10"
        }
    },
    {
        "model": "appointments.taxdeadline",
        "pk": 3,
        "fields": {
            "name": "Quarterly Excise Duty Return - Due",
            "description": "Submit quarterly excise duty returns to KRA",
            "deadline_date": "2026-04-20",
            "deadline_type": "excise_duty",
            "recurring": True,
            "next_deadline": "2026-07-20"
        }
    },
    {
        "model": "appointments.taxdeadline",
        "pk": 4,
        "fields": {
            "name": "Annual Personal Income Tax Return - Due",
            "description": "Individual income tax return filing deadline",
            "deadline_date": "2026-06-30",
            "deadline_type": "income_tax",
            "recurring": True,
            "next_deadline": "2027-06-30"
        }
    },
    {
        "model": "appointments.taxdeadline",
        "pk": 5,
        "fields": {
            "name": "ETIMS Compliance - Mandatory",
            "description": "E-Tax Invoice Management System compliance for all retail traders",
            "deadline_date": "2026-03-01",
            "deadline_type": "other",
            "recurring": False,
            "next_deadline": None
        }
    },
    {
        "model": "appointments.taxdeadline",
        "pk": 6,
        "fields": {
            "name": "Annual Corporate Tax Return - Due",
            "description": "Corporate income tax return filing deadline",
            "deadline_date": "2026-06-30",
            "deadline_type": "income_tax",
            "recurring": True,
            "next_deadline": "2027-06-30"
        }
    },
    {
        "model": "appointments.taxdeadline",
        "pk": 7,
        "fields": {
            "name": "Estimated VAT Quarterly Installment - Due",
            "description": "Estimated quarterly VAT installment payment",
            "deadline_date": "2026-03-31",
            "deadline_type": "vat",
            "recurring": True,
            "next_deadline": "2026-06-30"
        }
    },
    {
        "model": "appointments.taxdeadline",
        "pk": 8,
        "fields": {
            "name": "Annual Stamp Duty Declaration - Due",
            "description": "Submit annual stamp duty returns",
            "deadline_date": "2026-06-30",
            "deadline_type": "other",
            "recurring": True,
            "next_deadline": "2027-06-30"
        }
    },
    {
        "model": "appointments.taxdeadline",
        "pk": 9,
        "fields": {
            "name": "Business Tax Return (if applicable) - Due",
            "description": "Business tax declaration and payment if applicable",
            "deadline_date": "2026-06-30",
            "deadline_type": "other",
            "recurring": True,
            "next_deadline": "2027-06-30"
        }
    },
    {
        "model": "appointments.taxdeadline",
        "pk": 10,
        "fields": {
            "name": "Property Tax Annual Return - Due",
            "description": "Annual property tax return filing (where applicable)",
            "deadline_date": "2026-05-31",
            "deadline_type": "other",
            "recurring": True,
            "next_deadline": "2027-05-31"
        }
    }
]

# Save as JSON file
with open('kenyan_tax_calendar.json', 'w') as f:
    json.dump(fixtures, f, indent=2)

print("Created kenyan_tax_calendar.json")
