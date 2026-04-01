from django.shortcuts import render
from django.http import HttpResponse
from .models import CoreSettings, Page


def test(request):
    """Simple test view to verify server is responding"""
    return HttpResponse("✅ Server is running! Django is working correctly.")


def home(request):
    """Homepage view"""
    try:
        settings = CoreSettings.objects.first()
    except Exception as e:
        return HttpResponse(f"Error loading settings: {e}")
    
    # Get upcoming tax deadlines
    try:
        from apps.appointments.models import TaxDeadline
        from datetime import date
        upcoming_deadlines = TaxDeadline.objects.filter(
            deadline_date__gte=date.today()
        ).order_by('deadline_date')[:5]  # Get top 5 upcoming deadlines
    except Exception as e:
        print(f"Error loading deadlines: {e}")
        upcoming_deadlines = []
    
    context = {
        'settings': settings,
        'upcoming_deadlines': upcoming_deadlines,
        'featured_testimonials': [],
    }
    
    try:
        return render(request, 'core/home.html', context)
    except Exception as e:
        return HttpResponse(f"Error rendering template: {type(e).__name__}: {str(e)[:500]}")


def page_detail(request, slug):
    """Display static page"""
    page = Page.objects.get(slug=slug, is_published=True)
    context = {
        'page': page,
    }
    return render(request, 'core/page_detail.html', context)


def about(request):
    """About page view"""
    context = {
        'page_title': 'About HS Consulting',
    }
    return render(request, 'core/about.html', context)
