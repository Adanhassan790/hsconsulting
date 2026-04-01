"""
Django settings for HS Consulting project.
"""

from pathlib import Path
from decouple import config
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET_KEY', default='django-insecure-change-this-key-in-production-NOW')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,*.railway.app', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition
INSTALLED_APPS = [
    # 'daphne',  # ASGI support - install when needed
    'jazzmin',  # Modern admin interface - must be before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'crispy_forms',
    'crispy_bootstrap5',
    'corsheaders',
    'django_celery_beat',
    'timezone_field',
    'django_filters',
    
    # Local apps
    'apps.core',
    'apps.services',
    'apps.appointments',
    'apps.inquiries',
    'apps.clients',
    'apps.testimonials',
    'apps.blog',
    'apps.accounts',
    'apps.admin_dashboard',
    'apps.careers',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise for static files
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Disable HTTPS enforcement in development
if DEBUG:
    SECURE_PROXY_SSL_HEADER = None
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
else:
    # Production security settings
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.global_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': config('DB_NAME', default=str(BASE_DIR / 'db.sqlite3')),
        'USER': config('DB_USER', default=''),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default=''),
        'PORT': config('DB_PORT', default=''),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# CORS settings
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:3000,http://127.0.0.1:3000', cast=lambda v: [s.strip() for s in v.split(',')])

# Celery Configuration
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Nairobi'

# Email Configuration
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@hsconsulting.co.ke')

# Twilio Configuration
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID', default='')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN', default='')
TWILIO_PHONE_NUMBER = config('TWILIO_PHONE_NUMBER', default='')

# Login URL
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'admin_dashboard:dashboard'
LOGOUT_REDIRECT_URL = 'core:home'

# Static files configuration for production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Jazzmin Admin Configuration
JAZZMIN_SETTINGS = {
    "site_header": "HS Consulting Admin",
    "site_title": "HS Consulting",
    "index_title": "Welcome to HS Consulting Admin",
    "welcome_sign": "Welcome to HS Consulting Administration Panel",
    "copyright": "HS Consulting (c) 2026",
    "search_model": ["core.CoreSettings", "services.Service", "inquiries.Inquiry"],
    "topmenu_links": [
        {"name": "Home", "url": "/", "permissions": ["auth.add_user"]},
        {"name": "Support", "url": "/admin/login/?next=/admin/", "new_window": False},
    ],
    "userswitcher": False,
    "show_ui_builder": False,
    "navigation": {
        "Services": {
            "items": [
                {"model": "services.Service"},
                {"model": "services.ServiceFAQ"},
            ]
        },
        "Appointments": {
            "items": [
                {"model": "appointments.Appointment"},
                {"model": "appointments.AppointmentSlot"},
                {"model": "appointments.TaxDeadline"},
            ]
        },
        "Inquiries": {
            "items": [
                {"model": "inquiries.Inquiry"},
            ]
        },
        "Clients": {
            "items": [
                {"model": "clients.Client"},
                {"model": "clients.ClientDocument"},
            ]
        },
        "Blog": {
            "items": [
                {"model": "blog.BlogPost"},
                {"model": "blog.BlogCategory"},
            ]
        },
        "Testimonials": {
            "items": [
                {"model": "testimonials.Testimonial"},
                {"model": "testimonials.CaseStudy"},
            ]
        },
        "Careers": {
            "items": [
                {"model": "careers.Job"},
                {"model": "careers.JobApplication"},
            ]
        },
    }
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small": False,
    "footer_small": False,
    "body_small": False,
    "brand_small": False,
    "brand_colour": "navbar-danger",
    "accent": "accent-primary",
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_accordion": True,
    "navbar_pause_auto_display_breadcrumbs": False,
    "sidebar_nav_foldable": True,
}


# Jazzmin Admin Configuration
JAZZMIN_SETTINGS = {
    "site_header": "HS Consulting Admin",
    "site_title": "HS Consulting",
    "index_title": "Welcome to HS Consulting Admin",
    "welcome_sign": "Welcome to HS Consulting Administration Panel",
    "copyright": "HS Consulting © 2026",
    "search_model": ["core.CoreSettings", "services.Service", "inquiries.Inquiry"],
    "topmenu_links": [
        {"name": "Home", "url": "/", "permissions": ["auth.add_user"]},
        {"name": "Support", "url": "/admin/login/?next=/admin/", "new_window": False},
    ],
    "userswitcher": False,
    "show_ui_builder": False,
    "navigation": {
        "Services": {
            "items": [
                {"model": "services.Service"},
                {"model": "services.ServiceFAQ"},
            ]
        },
        "Appointments": {
            "items": [
                {"model": "appointments.Appointment"},
                {"model": "appointments.AppointmentSlot"},
                {"model": "appointments.TaxDeadline"},
            ]
        },
        "Inquiries": {
            "items": [
                {"model": "inquiries.Inquiry"},
            ]
        },
        "Clients": {
            "items": [
                {"model": "clients.Client"},
                {"model": "clients.ClientDocument"},
            ]
        },
        "Blog": {
            "items": [
                {"model": "blog.BlogPost"},
                {"model": "blog.BlogCategory"},
            ]
        },
        "Testimonials": {
            "items": [
                {"model": "testimonials.Testimonial"},
                {"model": "testimonials.CaseStudy"},
            ]
        },
        "Careers": {
            "items": [
                {"model": "careers.Job"},
                {"model": "careers.JobApplication"},
            ]
        },
    }
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small": False,
    "footer_small": False,
    "body_small": False,
    "brand_small": False,
    "brand_colour": "navbar-danger",
    "accent": "accent-primary",
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_accordion": True,
    "navbar_pause_auto_display_breadcrumbs": False,
    "sidebar_nav_foldable": True,
}
