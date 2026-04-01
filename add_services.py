import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from apps.services.models import Service

services = [
    {
        'name': 'Tax Health Checks',
        'slug': 'tax-health-checks',
        'description': 'Comprehensive tax compliance and health assessment.',
        'long_description': 'Evaluate your tax position and identify areas for optimization and compliance improvement.',
        'price_label': 'Contact for Pricing',
        'order': 1
    },
    {
        'name': 'Strategic Tax Advisory',
        'slug': 'strategic-tax-advisory',
        'description': 'Expert tax planning and strategic advisory services.',
        'long_description': 'Develop comprehensive tax strategies to minimize your tax burden legally.',
        'price_label': 'Contact for Pricing',
        'order': 2
    },
    {
        'name': 'Income Tax Filing and Advisory',
        'slug': 'income-tax-filing-advisory',
        'description': 'Complete income tax filing and personalized advisory.',
        'long_description': 'Professional income tax return preparation and advisory for individuals and businesses.',
        'price_label': 'From Ksh 5,000',
        'order': 3
    },
    {
        'name': 'VAT Filing & ETIMS Implementation',
        'slug': 'vat-filing-etims',
        'description': 'VAT compliance and ETIMS system implementation.',
        'long_description': 'Ensure full compliance with Kenyan VAT requirements and ETIMS regulations.',
        'price_label': 'From Ksh 8,000',
        'order': 4
    },
    {
        'name': 'PAYE Filing',
        'slug': 'paye-filing',
        'description': 'Professional PAYE returns and payroll tax management.',
        'long_description': 'Accurate PAYE filing and statutory deduction management for businesses.',
        'price_label': 'From Ksh 3,000',
        'order': 5
    },
    {
        'name': 'Withholding Tax Management',
        'slug': 'withholding-tax-management',
        'description': 'Withholding tax compliance and management services.',
        'long_description': 'Manage all withholding tax obligations and KRA compliance requirements.',
        'price_label': 'Contact for Pricing',
        'order': 6
    },
    {
        'name': 'Bookkeeping & Financial Statements',
        'slug': 'bookkeeping-financial-statements',
        'description': 'Professional bookkeeping and financial statement preparation.',
        'long_description': 'Accurate record-keeping and timely financial statement preparation for your business.',
        'price_label': 'From Ksh 5,000',
        'order': 7
    },
    {
        'name': 'Resolving Errors in the VAT Returns',
        'slug': 'resolving-vat-errors',
        'description': 'Expert resolution of VAT return discrepancies.',
        'long_description': 'Identify and correct VAT return errors to ensure KRA compliance.',
        'price_label': 'Contact for Pricing',
        'order': 8
    },
    {
        'name': 'Migrated Legacy Ledger Correction',
        'slug': 'legacy-ledger-correction',
        'description': 'Correction of migrated legacy ledger accounts.',
        'long_description': 'Resolve issues with legacy account migrations and ensure system accuracy.',
        'price_label': 'Contact for Pricing',
        'order': 9
    },
    {
        'name': 'KRA Audits, Objections and Appeals',
        'slug': 'kra-audits-objections',
        'description': 'Expert representation in KRA audits and appeals.',
        'long_description': 'Professional representation and support during KRA audits, objections, and appeals.',
        'price_label': 'Contact for Pricing',
        'order': 10
    },
    {
        'name': 'Correction of Errors in the iTAX Ledgers',
        'slug': 'itax-ledger-correction',
        'description': 'Resolution of iTAX ledger errors and discrepancies.',
        'long_description': 'Correct iTAX ledger errors and ensure accurate tax records.',
        'price_label': 'Contact for Pricing',
        'order': 11
    },
    {
        'name': 'Closing Out on Applications Pending at the KRA',
        'slug': 'kra-pending-applications',
        'description': 'Resolution of pending applications with KRA.',
        'long_description': 'Expert assistance in resolving and closing out applications pending with KRA.',
        'price_label': 'Contact for Pricing',
        'order': 12
    },
    {
        'name': 'Corporate Tax Planning & More',
        'slug': 'corporate-tax-planning',
        'description': 'Comprehensive corporate tax planning and related services.',
        'long_description': 'Strategic tax planning for corporations including restructuring and optimization.',
        'price_label': 'Contact for Pricing',
        'order': 13
    },
]

for svc_data in services:
    svc, created = Service.objects.get_or_create(slug=svc_data['slug'], defaults=svc_data)
    if created:
        print(f'✓ Created: {svc.name}')
    else:
        print(f'✓ Already exists: {svc.name}')

print(f'\nTotal services: {Service.objects.count()}')
