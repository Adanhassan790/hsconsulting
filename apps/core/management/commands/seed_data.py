from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import connection
from datetime import timedelta

class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **options):
        # Import models
        from apps.core.models import CoreSettings, Page
        from apps.services.models import Service, ServiceFAQ
        from apps.blog.models import BlogCategory, BlogPost
        from apps.testimonials.models import Testimonial, CaseStudy
        from apps.appointments.models import TaxDeadline
        
        self.stdout.write("Seeding database with sample data...")
        
        # Create Core Settings
        settings, created = CoreSettings.objects.get_or_create(
            id=1,
            defaults={
                'site_name': 'HS Consulting',
                'business_description': 'Professional Tax and Financial Solutions in Kenya',
                'phone': '+254 (0) 123 456 789',
                'email': 'info@hsconsulting.co.ke',
                'address': 'Nairobi, Kenya',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created Core Settings'))
        
        # Create Services
        services_data = [
            {
                'name': 'Tax Return Filing',
                'slug': 'tax-return-filing',
                'description': 'Complete tax return preparation and filing for individuals and businesses.',
                'price': '5,000',
                'is_active': True,
            },
            {
                'name': 'VAT & ETIMS Management',
                'slug': 'vat-etims-management',
                'description': 'Complete VAT management and ETIMS compliance for KRA.',
                'price': '8,000',
                'is_active': True,
            },
            {
                'name': 'Payroll Processing',
                'slug': 'payroll-processing',
                'description': 'Monthly payroll processing and statutory deductions.',
                'price': '3,000',
                'is_active': True,
            },
        ]
        
        for svc in services_data:
            service, created = Service.objects.get_or_create(slug=svc['slug'], defaults=svc)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created Service: {svc["name"]}'))
                
                # Add FAQs
                ServiceFAQ.objects.get_or_create(
                    service=service,
                    question='How long does this service take?',
                    defaults={'answer': 'Most services are completed within 5-7 working days.'}
                )
        
        # Create Blog Categories and Posts
        category, created = BlogCategory.objects.get_or_create(
            name='Tax Tips',
            defaults={'slug': 'tax-tips'}
        )
        
        blog_posts = [
            {
                'title': 'Top Tax Deductions for Small Business Owners',
                'slug': 'tax-deductions-small-business',
                'content': 'Discover the most important tax deductions available for small business owners in Kenya...',
            },
            {
                'title': 'Understanding ETIMS in Kenya',
                'slug': 'understanding-etims-kenya',
                'content': 'ETIMS (Excise Tax Invoice Management System) is mandatory for all VAT-registered businesses...',
            },
        ]
        
        for post_data in blog_posts:
            post, created = BlogPost.objects.get_or_create(
                slug=post_data['slug'],
                defaults={
                    'title': post_data['title'],
                    'content': post_data['content'],
                    'category': category,
                    'is_published': True,
                    'published_date': timezone.now(),
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created Blog Post: {post_data["title"]}'))
        
        # Create Testimonials
        testimonials = [
            {
                'client_name': 'John Mwangi',
                'client_company': 'Tech Solutions Ltd',
                'content': 'HS Consulting has been instrumental in ensuring our tax compliance. Highly professional!',
                'rating': 5,
                'is_featured': True,
            },
            {
                'client_name': 'Sarah Kipchoge',
                'client_company': 'Fashion Boutique',
                'content': 'Great service! They helped us save thousands in tax liability.',
                'rating': 5,
                'is_featured': True,
            },
        ]
        
        for test_data in testimonials:
            testimonial, created = Testimonial.objects.get_or_create(
                client_name=test_data['client_name'],
                defaults=test_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created Testimonial: {test_data["client_name"]}'))
        
        # Create Case Studies
        case_studies = [
            {
                'title': 'How We Reduced Business Tax by 40%',
                'slug': 'reduced-tax-40-percent',
                'client_name': 'James Okonkwo',
                'client_company': 'Manufacturing Ltd',
                'challenge': 'The business was overpaying taxes due to poor record keeping...',
                'solution': 'We restructured their accounting system and identified applicable deductions...',
                'results': 'Successfully reduced annual tax liability by 40% while ensuring full compliance.',
            },
        ]
        
        for case_data in case_studies:
            case, created = CaseStudy.objects.get_or_create(
                slug=case_data['slug'],
                defaults=case_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created Case Study: {case_data["title"]}'))
        
        # Create Tax Deadlines
        tax_deadlines = [
            {
                'name': 'Monthly VAT Return',
                'description': 'Submit your monthly VAT return to KRA',
                'deadline_date': timezone.now() + timedelta(days=15),
                'is_recurring': True,
            },
            {
                'name': 'Annual Tax Return',
                'description': 'File your annual income tax return',
                'deadline_date': timezone.now() + timedelta(days=60),
                'is_recurring': True,
            },
        ]
        
        for deadline_data in tax_deadlines:
            deadline, created = TaxDeadline.objects.get_or_create(
                name=deadline_data['name'],
                defaults=deadline_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created Tax Deadline: {deadline_data["name"]}'))
        
        self.stdout.write(self.style.SUCCESS('✓ Database seeding completed successfully!'))
