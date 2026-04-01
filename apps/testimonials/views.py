from django.shortcuts import render, get_object_or_404
from .models import Testimonial, CaseStudy


def testimonials_list(request):
    """List testimonials"""
    testimonials = Testimonial.objects.filter(is_published=True)
    featured = testimonials.filter(is_featured=True)[:3]
    
    context = {
        'testimonials': testimonials,
        'featured': featured,
    }
    return render(request, 'testimonials/list.html', context)


def case_studies_list(request):
    """List case studies"""
    case_studies = CaseStudy.objects.filter(is_published=True)
    
    context = {
        'case_studies': case_studies,
    }
    return render(request, 'testimonials/case_studies.html', context)


def case_study_detail(request, slug):
    """Case study detail"""
    case_study = get_object_or_404(CaseStudy, slug=slug, is_published=True)
    
    context = {
        'case_study': case_study,
    }
    return render(request, 'testimonials/case_study_detail.html', context)
