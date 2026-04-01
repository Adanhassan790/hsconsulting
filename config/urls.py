"""
URL configuration for HS Consulting project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Apps
    path('', include(('apps.core.urls', 'core'))),
    path('services/', include(('apps.services.urls', 'services'))),
    path('appointments/', include(('apps.appointments.urls', 'appointments'))),
    path('inquiries/', include(('apps.inquiries.urls', 'inquiries'))),
    path('clients/', include(('apps.clients.urls', 'clients'))),
    path('testimonials/', include(('apps.testimonials.urls', 'testimonials'))),
    path('blog/', include(('apps.blog.urls', 'blog'))),
    path('accounts/', include(('apps.accounts.urls', 'accounts'))),
    path('admin-dashboard/', include(('apps.admin_dashboard.urls', 'admin_dashboard'))),
    path('careers/', include(('apps.careers.urls', 'careers'))),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
