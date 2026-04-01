from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import ClientRegistrationForm


def register(request):
    """Client registration"""
    if request.user.is_authenticated:
        return redirect('clients:dashboard')
    
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('clients:create_profile')
    else:
        form = ClientRegistrationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login_view(request):
    """Client login"""
    if request.user.is_authenticated:
        return redirect('clients:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('clients:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    """Client logout"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('core:home')
