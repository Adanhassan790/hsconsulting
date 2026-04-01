from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('inquiries/', views.inquiries_list, name='inquiries_list'),
    path('inquiries/<int:pk>/', views.inquiry_detail, name='inquiry_detail'),
    path('appointments/', views.appointments_calendar, name='appointments_calendar'),
    path('clients/', views.clients_list, name='clients_list'),
    path('reports/', views.reports, name='reports'),
]
