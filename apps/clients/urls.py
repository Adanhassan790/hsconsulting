from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('dashboard/', views.client_dashboard, name='dashboard'),
    path('documents/', views.client_documents, name='documents'),
    path('upload/', views.upload_document, name='upload_document'),
    path('create-profile/', views.create_profile, name='create_profile'),
]
