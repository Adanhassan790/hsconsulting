from django.urls import path
from . import views

app_name = 'inquiries'

urlpatterns = [
    path('contact/', views.contact_us, name='contact'),
    path('success/', views.contact_success, name='contact_success'),
]
