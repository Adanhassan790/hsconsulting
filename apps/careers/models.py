from django.db import models
from django.utils import timezone


class Job(models.Model):
    """Job posting model"""
    
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full-Time'),
        ('part_time', 'Part-Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('filled', 'Filled'),
    ]
    
    title = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField(help_text="List job requirements")
    responsibilities = models.TextField(help_text="List job responsibilities")
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES)
    location = models.CharField(max_length=200, default="Nairobi, Kenya")
    salary_range = models.CharField(max_length=100, blank=True, help_text="e.g. KES 50,000 - 100,000")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    posted_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    featured = models.BooleanField(default=False, help_text="Display on homepage")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-posted_date']
        verbose_name = 'Job Posting'
        verbose_name_plural = 'Job Postings'
    
    def __str__(self):
        return f"{self.title} ({self.department})"
    
    @property
    def is_deadline_passed(self):
        return self.deadline <= timezone.now()
    
    @property
    def can_apply(self):
        return self.status == 'open' and not self.is_deadline_passed and self.is_active


class JobApplication(models.Model):
    """Job application model"""
    
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('reviewing', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview Scheduled'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ]
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    resume = models.FileField(upload_to='resumes/%Y/%m/')
    cover_letter = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text="Internal notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-applied_date']
        verbose_name = 'Job Application'
        verbose_name_plural = 'Job Applications'
        unique_together = ('job', 'email')
    
    def __str__(self):
        return f"{self.full_name} - {self.job.title}"
