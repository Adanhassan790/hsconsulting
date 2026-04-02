from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('init/', views.init, name='init'),
    path('populate-deadlines/', views.populate_deadlines, name='populate_deadlines'),
    path('populate-services/', views.populate_services, name='populate_services'),
    path('health/', views.health_check, name='health_check'),
    path('test/', views.test, name='test'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('page/<slug:slug>/', views.page_detail, name='page_detail'),
]
