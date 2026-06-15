from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.services.models import Service
from apps.blog.models import BlogPost


class StaticViewSitemap(Sitemap):
    priority = 0.9
    changefreq = 'weekly'

    def items(self):
        return [
            'core:home',
            'core:about',
            'services:list',
            'blog:list',
            'testimonials:list',
            'inquiries:contact',
            'careers:careers_list',
            'appointments:tax_calendar',
        ]

    def location(self, item):
        return reverse(item)


class ServiceSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return Service.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f'/services/{obj.slug}/'


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.published_at

    def location(self, obj):
        return f'/blog/{obj.slug}/'
