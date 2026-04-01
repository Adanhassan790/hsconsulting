

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
