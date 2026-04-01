import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist

try:
    # Try to render the home template
    html = render_to_string('core/home.html', {
        'settings': None,
        'upcoming_deadlines': [],
        'featured_testimonials': [],
    })
    print("✅ Template 'core/home.html' renders successfully!")
    print(f"   Template length: {len(html)} characters")
except TemplateDoesNotExist as e:
    print(f"❌ Template not found: {e}")
except Exception as e:
    print(f"❌ Template rendering error: {type(e).__name__}: {e}")
