# Generated migration for careers app

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('department', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('requirements', models.TextField(help_text='List job requirements')),
                ('responsibilities', models.TextField(help_text='List job responsibilities')),
                ('employment_type', models.CharField(choices=[('full_time', 'Full-Time'), ('part_time', 'Part-Time'), ('contract', 'Contract'), ('internship', 'Internship')], max_length=20)),
                ('location', models.CharField(default='Nairobi, Kenya', max_length=200)),
                ('salary_range', models.CharField(blank=True, help_text='e.g. KES 50,000 - 100,000', max_length=100)),
                ('status', models.CharField(choices=[('open', 'Open'), ('closed', 'Closed'), ('filled', 'Filled')], default='open', max_length=20)),
                ('posted_date', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateTimeField()),
                ('featured', models.BooleanField(default=False, help_text='Display on homepage')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Job Posting',
                'verbose_name_plural': 'Job Postings',
                'ordering': ['-posted_date'],
            },
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('resume', models.FileField(upload_to='resumes/%Y/%m/')),
                ('cover_letter', models.TextField()),
                ('status', models.CharField(choices=[('applied', 'Applied'), ('reviewing', 'Under Review'), ('shortlisted', 'Shortlisted'), ('interview', 'Interview Scheduled'), ('rejected', 'Rejected'), ('accepted', 'Accepted')], default='applied', max_length=20)),
                ('applied_date', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, help_text='Internal notes')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='careers.job')),
            ],
            options={
                'verbose_name': 'Job Application',
                'verbose_name_plural': 'Job Applications',
                'ordering': ['-applied_date'],
                'unique_together': {('job', 'email')},
            },
        ),
    ]
