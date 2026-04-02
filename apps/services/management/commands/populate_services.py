from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.services.models import Service


class Command(BaseCommand):
    help = 'Populate Kenyan tax consulting services'

    def handle(self, *args, **options):
        self.stdout.write('Populating services...')
        Service.objects.all().delete()
        
        services = [
            {
                'name': 'Tax Return Filing',
                'description': 'Complete tax return preparation and filing for individuals and businesses',
                'long_description': 'Professional preparation and submission of annual tax returns to KRA. We ensure timely filing with all required documentation and schedules.',
                'price_label': 'Contact for Pricing',
                'order': 1,
            },
            {
                'name': 'VAT & ETIMS Compliance',
                'description': 'Comprehensive VAT management and ETIMS compliance for KRA',
                'long_description': 'End-to-end VAT management including monthly return preparation, ETIMS integration, and KRA compliance. We manage all VAT obligations.',
                'price_label': 'Contact for Pricing',
                'order': 2,
            },
            {
                'name': 'Payroll Processing',
                'description': 'Monthly payroll processing and statutory deductions',
                'long_description': 'Complete payroll management including salary calculations, PAYE, NHIF, NSSF, and other statutory deductions with monthly reporting.',
                'price_label': 'Contact for Pricing',
                'order': 3,
            },
            {
                'name': 'Company Registration & Compliance',
                'description': 'Business registration and ongoing statutory compliance',
                'long_description': 'Assistance with company registration, business registration, and maintaining compliance with all regulatory requirements.',
                'price_label': 'Contact for Pricing',
                'order': 4,
            },
            {
                'name': 'Audit Services',
                'description': 'Professional external and internal audit services',
                'long_description': 'Comprehensive audit services including financial statement audits, internal audits, and compliance audits.',
                'price_label': 'Contact for Pricing',
                'order': 5,
            },
            {
                'name': 'Bookkeeping & Accounting',
                'description': 'Monthly bookkeeping and financial statement preparation',
                'long_description': 'Professional bookkeeping services including transaction recording, reconciliation, and monthly financial statement preparation.',
                'price_label': 'Contact for Pricing',
                'order': 6,
            },
            {
                'name': 'Tax Advisory',
                'description': 'Strategic tax planning to optimize your tax position and reduce liabilities',
                'long_description': 'Expert consultation on tax-efficient business structures, investment strategies, and tax minimization techniques.',
                'price_label': 'Contact for Pricing',
                'order': 7,
            },
            {
                'name': 'Financial Consulting',
                'description': 'Expert guidance on financial management and forecasting',
                'long_description': 'Strategic financial planning including cash flow analysis, budgeting, financial forecasting, and performance analysis.',
                'price_label': 'Contact for Pricing',
                'order': 8,
            },
            {
                'name': 'PAYE Management',
                'description': 'PAYE (Pay As You Earn) processing and KRA compliance',
                'long_description': 'Comprehensive PAYE management including withholding calculations, monthly remittance, and KRA reconciliation.',
                'price_label': 'Contact for Pricing',
                'order': 9,
            },
            {
                'name': 'Withholding Tax Services',
                'description': 'Withholding tax declarations and compliance management',
                'long_description': 'Management of withholding tax obligations including contractor withholds, service provider withholding, and monthly declarations.',
                'price_label': 'Contact for Pricing',
                'order': 10,
            },
            {
                'name': 'Corporate Tax Planning',
                'description': 'Strategic corporate tax planning and optimization',
                'long_description': 'Advanced tax planning strategies for corporations including income planning, deduction optimization, and tax risk management.',
                'price_label': 'Contact for Pricing',
                'order': 11,
            },
            {
                'name': 'Personal Income Tax Planning',
                'description': 'Individual tax planning and optimization strategies',
                'long_description': 'Personal tax planning including investment income management, expense optimization, and retirement planning tax strategies.',
                'price_label': 'Contact for Pricing',
                'order': 12,
            },
            {
                'name': 'Tax Compliance Review',
                'description': 'Comprehensive tax compliance review and remediation',
                'long_description': 'Review of current tax compliance status, identification of gaps, and assistance in bringing operations into full compliance.',
                'price_label': 'Contact for Pricing',
                'order': 13,
            }
        ]
        
        created_count = 0
        for service_data in services:
            try:
                service_data['slug'] = slugify(service_data['name'])
                service = Service.objects.create(**service_data)
                self.stdout.write(f'✓ Created: {service.name}')
                created_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Failed to create {service_data["name"]}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'✓ Successfully created {created_count} services'))
