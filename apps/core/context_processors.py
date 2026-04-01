from apps.core.models import CoreSettings


def global_settings(request):
    """Make CoreSettings available to all templates"""
    try:
        settings = CoreSettings.objects.first()
    except:
        settings = None
    
    return {
        'settings': settings,
    }
