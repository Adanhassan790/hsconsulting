from django.db import ProgrammingError, OperationalError
from django.db.utils import DatabaseError


def global_settings(request):
    """Make CoreSettings available to all templates"""
    settings = None
    
    try:
        from apps.core.models import CoreSettings
        settings = CoreSettings.objects.first()
    except (ProgrammingError, OperationalError, DatabaseError):
        # Table doesn't exist yet (during initial setup/migrations) or DB connection issue
        # Return None and templates should handle missing settings gracefully
        pass
    except Exception as e:
        # Log other errors but don't crash
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Error loading CoreSettings: {e}")
    
    return {
        'settings': settings,
    }
