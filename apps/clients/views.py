from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Client, ClientDocument, ServiceHistory


@login_required
def client_dashboard(request):
    """Client portal dashboard"""
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        return redirect('clients:create_profile')
    
    recent_documents = client.documents.all()[:5]
    service_history = client.service_history.all()[:5]
    
    context = {
        'client': client,
        'recent_documents': recent_documents,
        'service_history': service_history,
    }
    return render(request, 'clients/dashboard.html', context)


@login_required
def client_documents(request):
    """View and manage client documents"""
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        return redirect('clients:create_profile')
    
    documents = client.documents.all()
    context = {
        'documents': documents,
    }
    return render(request, 'clients/documents.html', context)


@login_required
def upload_document(request):
    """Upload new document"""
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        return redirect('clients:create_profile')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        document_type = request.POST.get('document_type')
        description = request.POST.get('description')
        file = request.FILES.get('file')
        
        if title and document_type and file:
            ClientDocument.objects.create(
                client=client,
                title=title,
                document_type=document_type,
                description=description,
                file=file,
            )
            messages.success(request, 'Document uploaded successfully!')
            return redirect('clients:documents')
    
    context = {
        'document_types': ClientDocument.DOCUMENT_TYPE_CHOICES,
    }
    return render(request, 'clients/upload_document.html', context)


def create_profile(request):
    """Create client profile after registration"""
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        company_name = request.POST.get('company_name')
        client_type = request.POST.get('client_type')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code', '')
        
        if full_name and client_type and phone and address and city:
            Client.objects.create(
                user=request.user,
                full_name=full_name,
                company_name=company_name,
                client_type=client_type,
                phone=phone,
                address=address,
                city=city,
                postal_code=postal_code,
            )
            messages.success(request, 'Profile created successfully!')
            return redirect('clients:dashboard')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'clients/create_profile.html')
