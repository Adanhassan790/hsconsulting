import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from apps.core.views import home
from django.test import RequestFactory

factory = RequestFactory()
request = factory.get('/')

try:
    response = home(request)
    print(f"✅ Home view works! Status: {response.status_code}")
except Exception as e:
    print(f"❌ Error in home view:")
    print(f"   {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
