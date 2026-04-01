from django.shortcuts import render, get_object_or_404
from .models import Service


def services_list(request):
    """List all services"""
    services = Service.objects.filter(is_active=True)
    context = {
        'services': services,
    }
    return render(request, 'services/services_list.html', context)


def service_detail(request, slug):
    """Service detail page"""
    service = get_object_or_404(Service, slug=slug, is_active=True)
    faqs = service.faqs.all()
    context = {
        'service': service,
        'faqs': faqs,
    }
    return render(request, 'services/service_detail.html', context)
