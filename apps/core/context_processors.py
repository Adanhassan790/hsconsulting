from apps.core.models import CoreSettings
from django.db import ProgrammingError


def global_settings(request):
    """Make CoreSettings available to all templates"""
    try:
        settings = CoreSettings.objects.first()
    except (ProgrammingError, Exception):
        # Table doesn't exist yet (during migrations) or other DB error
        settings = None
    
    return {
        'settings': settings,
    }
