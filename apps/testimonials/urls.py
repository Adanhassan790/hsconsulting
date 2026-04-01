from django.urls import path
from . import views

app_name = 'testimonials'

urlpatterns = [
    path('', views.testimonials_list, name='list'),
    path('case-studies/', views.case_studies_list, name='case_studies'),
    path('case-studies/<slug:slug>/', views.case_study_detail, name='case_study_detail'),
]
