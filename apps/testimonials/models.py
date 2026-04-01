from django.db import models
from django.utils.translation import gettext_lazy as _


class Testimonial(models.Model):
    """Client testimonials and case studies"""
    client_name = models.CharField(max_length=200)
    client_company = models.CharField(max_length=200)
    client_title = models.CharField(max_length=200, blank=True)
    
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    
    image = models.ImageField(upload_to='testimonials/', null=True, blank=True)
    
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("Testimonial")
        verbose_name_plural = _("Testimonials")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.client_name} - {self.client_company}"


class CaseStudy(models.Model):
    """Detailed case studies of projects"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    
    client_name = models.CharField(max_length=200)
    client_company = models.CharField(max_length=200)
    
    challenge = models.TextField()
    solution = models.TextField()
    results = models.TextField()
    
    featured_image = models.ImageField(upload_to='case_studies/')
    
    is_published = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Case Study")
        verbose_name_plural = _("Case Studies")
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
