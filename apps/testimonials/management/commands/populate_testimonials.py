from django.core.management.base import BaseCommand
from apps.testimonials.models import Testimonial


class Command(BaseCommand):
    help = 'Populate client testimonials'

    def handle(self, *args, **options):
        self.stdout.write('Populating testimonials...')
        Testimonial.objects.all().delete()
        
        testimonials = [
            {
                'client_name': 'John Mwangi',
                'client_company': 'Tech Solutions Ltd',
                'client_title': 'Finance Director',
                'content': 'HS Consulting has been instrumental in managing our tax compliance. Their professionalism is exceptional and they save us thousands in tax liability every year.',
                'rating': 5,
                'is_featured': True,
                'is_published': True,
            },
            {
                'client_name': 'Sarah Kipchoge',
                'client_company': 'Fashion Boutique Kenya',
                'client_title': 'Business Owner',
                'content': 'They helped us streamline our VAT and ETIMS compliance. The team is knowledgeable, responsive, and genuinely cares about our success.',
                'rating': 5,
                'is_featured': True,
                'is_published': True,
            },
            {
                'client_name': 'James Okonkwo',
                'client_company': 'Manufacturing Ltd',
                'client_title': 'General Manager',
                'content': 'The team expertise in ETIMS and VAT compliance is unmatched. Excellent service and professional handling of all tax matters.',
                'rating': 5,
                'is_featured': True,
                'is_published': True,
            },
            {
                'client_name': 'Grace Wanjiru',
                'client_company': 'Real Estate Investments',
                'client_title': 'CEO',
                'content': 'Outstanding tax advisory services. They helped us optimize our portfolio structure and significantly reduced our tax burden.',
                'rating': 5,
                'is_featured': False,
                'is_published': True,
            },
            {
                'client_name': 'Peter Kamau',
                'client_company': 'Construction Company',
                'client_title': 'Business Owner',
                'content': 'Very professional team. They handle our payroll, VAT, and corporate tax perfectly. Highly recommended!',
                'rating': 5,
                'is_featured': False,
                'is_published': True,
            },
            {
                'client_name': 'Emma Kariuki',
                'client_company': 'Healthcare Solutions',
                'client_title': 'Accounting Manager',
                'content': 'Great service! They simplified our accounting process and made tax filing a breeze. Team is always available for questions.',
                'rating': 5,
                'is_featured': False,
                'is_published': True,
            },
        ]
        
        created_count = 0
        for testimonial_data in testimonials:
            try:
                testimonial = Testimonial.objects.create(**testimonial_data)
                self.stdout.write(f'✓ Created: {testimonial.client_name} - {testimonial.client_company}')
                created_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Failed: {testimonial_data["client_name"]}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'✓ Successfully created {created_count} testimonials'))
