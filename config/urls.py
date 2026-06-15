"""
URL configuration for HS Consulting project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from apps.core.sitemaps import StaticViewSitemap, ServiceSitemap, BlogSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'services': ServiceSitemap,
    'blog': BlogSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    
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

# Serve media files always (user uploads, images)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files - ALWAYS in production with WhiteNoise, or in DEBUG
# WhiteNoise will efficiently serve these in production
# Django fallback in development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
