from django.core.management.base import BaseCommand
from datetime import date
from apps.appointments.models import TaxDeadline


class Command(BaseCommand):
    help = 'Populate Kenyan tax deadlines'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing deadlines...')
        TaxDeadline.objects.all().delete()
        
        deadlines = [
            TaxDeadline(
                name='PAYE Due',
                description='PAYE (Pay As You Earn) tax payments and returns due',
                deadline_date=date(2026, 4, 10),
                deadline_type='paye',
                recurring=True,
            ),
            TaxDeadline(
                name='VAT Filing',
                description='Monthly VAT returns submission deadline',
                deadline_date=date(2026, 4, 20),
                deadline_type='vat',
                recurring=True,
            ),
            TaxDeadline(
                name='Income Tax Filing',
                description='Annual income tax return filing deadline for individuals',
                deadline_date=date(2026, 6, 30),
                deadline_type='income_tax',
                recurring=True,
            ),
            TaxDeadline(
                name='Corporate Tax Filing',
                description='Corporate tax returns submission deadline',
                deadline_date=date(2026, 5, 31),
                deadline_type='income_tax',
                recurring=True,
            ),
            TaxDeadline(
                name='Withholding Tax Returns',
                description='Submit withholding tax statements and payments',
                deadline_date=date(2026, 4, 15),
                deadline_type='other',
                recurring=True,
            ),
        ]
        
        created = TaxDeadline.objects.bulk_create(deadlines)
        self.stdout.write(self.style.SUCCESS(f'✓ Successfully created {len(created)} tax deadlines'))
        
        for d in created:
            self.stdout.write(f'  • {d.name} - {d.deadline_date}')
