from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('book/', views.book_appointment, name='book'),
    path('success/<int:pk>/', views.booking_success, name='booking_success'),
    path('tax-calendar/', views.tax_calendar, name='tax_calendar'),
]
