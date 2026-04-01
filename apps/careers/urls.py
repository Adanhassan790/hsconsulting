from django.urls import path
from . import views

urlpatterns = [
    path('', views.careers_list, name='careers_list'),
    path('job/<int:pk>/', views.job_detail, name='job_detail'),
]
