from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Job, JobApplication
from .forms import JobApplicationForm


def careers_list(request):
    """Display all active job postings"""
    jobs = Job.objects.filter(is_active=True, status='open')
    
    # Filter by employment type if provided
    employment_type = request.GET.get('type')
    if employment_type:
        jobs = jobs.filter(employment_type=employment_type)
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        jobs = jobs.filter(title__icontains=search) | jobs.filter(description__icontains=search)
    
    # Get featured jobs
    featured_jobs = Job.objects.filter(is_active=True, status='open', featured=True)[:3]
    
    # Pagination
    paginator = Paginator(jobs, 12)
    page = request.GET.get('page')
    jobs = paginator.get_page(page)
    
    context = {
        'jobs': jobs,
        'featured_jobs': featured_jobs,
        'search': search,
        'employment_type': employment_type,
        'employment_types': Job.EMPLOYMENT_TYPE_CHOICES,
    }
    return render(request, 'careers/careers_list.html', context)


def job_detail(request, pk):
    """Display job details and application form"""
    job = get_object_or_404(Job, pk=pk, is_active=True)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            try:
                application.save()
                messages.success(request, 'Your application has been submitted successfully! We\'ll review it and get back to you soon.')
                return redirect('careers_list')
            except Exception as e:
                messages.error(request, 'You have already applied for this position.')
                return redirect('job_detail', pk=pk)
    else:
        form = JobApplicationForm()
    
    # Get related job postings
    related_jobs = Job.objects.filter(
        is_active=True, 
        status='open', 
        department=job.department
    ).exclude(pk=pk)[:3]
    
    context = {
        'job': job,
        'form': form,
        'related_jobs': related_jobs,
    }
    return render(request, 'careers/job_detail.html', context)
