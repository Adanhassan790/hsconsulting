# HS CONSULTING - SYSTEM ARCHITECTURE DIAGRAM

## High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         INTERNET / BROWSERS                              │
└────────────────────┬────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        NGINX WEB SERVER                                  │
│  (Reverse proxy, static files, SSL/HTTPS)                              │
└────────────────────┬────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    GUNICORN APP SERVER                                   │
│                 (Django 4.2 Application)                                │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                   DJANGO REQUEST/RESPONSE                        │  │
│  ├──────────────────────────────────────────────────────────────────┤  │
│  │  URLs (config/urls.py)                                           │  │
│  │   ├─ /                           → apps.core.views              │  │
│  │   ├─ /services/                 → apps.services.views          │  │
│  │   ├─ /appointments/             → apps.appointments.views      │  │
│  │   ├─ /inquiries/                → apps.inquiries.views         │  │
│  │   ├─ /clients/                  → apps.clients.views           │  │
│  │   ├─ /blog/                     → apps.blog.views              │  │
│  │   ├─ /accounts/                 → apps.accounts.views          │  │
│  │   └─ /admin-dashboard/          → apps.admin_dashboard.views  │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└────────────┬──────────────────────────────────────────────┬──────────────┘
             │                                              │
             ▼                                              ▼
┌────────────────────────────┐          ┌──────────────────────────────┐
│    DATABASE                 │          │  BACKGROUND TASKS           │
│  (PostgreSQL / SQLite)      │          │  (Celery + Redis)           │
│                             │          │                              │
│  ├─ Users                   │          │  ├─ Email reminders (24h)   │
│  ├─ Clients                 │          │  ├─ SMS reminders (Twilio)  │
│  ├─ Services                │          │  ├─ Inquiry follow-ups      │
│  ├─ Appointments            │          │  ├─ Tax deadline alerts     │
│  ├─ Inquiries               │          │  └─ Scheduled reports       │
│  ├─ Blog Posts              │          │                              │
│  ├─ Documents               │          │  Runs Every:                │
│  └─ Tax Deadlines           │          │  ├─ Every 24 hours          │
│                             │          │  ├─ Every week              │
│  Updated by:                │          │  └─ On schedule (Beat)      │
│  ├─ Admin form submissions  │          └──────────────────────────────┘
│  ├─ Client actions          │
│  └─ API endpoints           │
└────────────────────────────┘
             │
             └─────────────────────────────────────────────────────────┐
                                                                       │
              ┌────────────────────────────────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                                      │
│                                                                           │
│  ├─ Email Service (Gmail / SendGrid / SMTP)                             │
│  │  └─ Sends appointment confirmations and reminders                    │
│  │                                                                       │
│  ├─ Twilio SMS Gateway                                                  │
│  │  └─ Sends appointment reminders via SMS                             │
│  │                                                                       │
│  └─ Static File Storage (S3 / CloudFront optional)                      │
│     └─ CSS, JS, images, client documents                               │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Application Flow Diagram

```
                            PUBLIC WEBSITE
                           
    ┌──────────────────────────────────────────────────┐
    │                                                  │
    ├─ Homepage                                        │
    │  ├─ Services preview                            │
    │  ├─ Recent testimonials                         │
    │  └─ Upcoming tax deadlines                      │
    │                                                  │
    ├─ Services Page                                  │
    │  └─ Detail pages for each service               │
    │                                                  │
    ├─ Book Appointment                               │
    │  └─ Form → Appointment model                    │
    │     └─ Email confirmation                       │
    │     └─ 24-hour email reminder                   │
    │     └─ 24-hour SMS reminder                     │
    │                                                  │
    ├─ Contact/Inquiry                                │
    │  └─ Form → Inquiry model                        │
    │                                                  │
    ├─ Blog                                           │
    │  └─ Posts with comments                         │
    │                                                  │
    └─ Testimonials & Case Studies                   │
                                                      │
    ┌──────────────────────────────────────────────────┐
    │           CLIENT PORTAL (Authenticated)         │
    │                                                  │
    ├─ Login/Register                                 │
    │  └─ Email confirmation                          │
    │                                                  │
    ├─ Dashboard                                      │
    │  ├─ Upcoming appointments                       │
    │  └─ Recent documents                            │
    │                                                  │
    ├─ Documents                                      │
    │  ├─ Upload new documents                        │
    │  └─ Track status                                │
    │                                                  │
    └─ Profile Management                            │
                                                      │
    ┌──────────────────────────────────────────────────┐
    │      STAFF ADMIN DASHBOARD (Protected)          │
    │      (2 team members with permissions)          │
    │                                                  │
    ├─ Dashboard (Overview)                          │
    │  ├─ 4 Metric cards                             │
    │  ├─ Recent inquiries list                       │
    │  ├─ Upcoming appointments                       │
    │  └─ Upcoming tax deadlines                      │
    │                                                  │
    ├─ Inquiry Management                            │
    │  ├─ Filter by status                           │
    │  ├─ Update status (new/contacted/in_progress..) │
    │  ├─ Add internal notes                         │
    │  └─ Schedule follow-up                         │
    │                                                  │
    ├─ Appointment Management                        │
    │  ├─ Calendar view                              │
    │  ├─ View all appointments                      │
    │  ├─ Update status                              │
    │  ├─ Send manual reminders                      │
    │  └─ Assign to staff                            │
    │                                                  │
    ├─ Client Management                             │
    │  ├─ View all clients                           │
    │  ├─ Filter by type (individual/corporate/sme) │
    │  ├─ Search                                      │
    │  ├─ View service history                       │
    │  └─ View uploaded documents                    │
    │                                                  │
    ├─ Reports & Analytics                           │
    │  ├─ Inquiries by status (chart)                │
    │  ├─ Appointments by status (chart)             │
    │  ├─ Service performance metrics                │
    │  └─ Monthly/yearly reports                     │
    │                                                  │
    └─ Django Admin Panel                            │
       ├─ Full model management                       │
       ├─ User & permissions                          │
       ├─ Email logs                                  │
       └─ Activity logs                               │
```

---

## Data Model Relationships Diagram

```
                        ┌─────────────┐
                        │    User     │ (Django built-in)
                        │ (Auth)      │
                        └──────┬──────┘
                               │
                    ┌──────────┼───────────┐
                    │          │           │
                    ▼          ▼           ▼
            ┌─────────────┐  ┌────────────┐  ┌─────────────────┐
            │  Client     │  │  Admin     │  │ DashboardAccess │
            │             │  │            │  │ Control         │
            └──────┬──────┘  └────────────┘  └─────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
        ▼          ▼          ▼
   ┌─────────┐ ┌─────────┐ ┌──────────────┐
   │ClientDoc│ │ServiceH │ │ Appointment  │
   │ument   │ │ istory  │ │ (booked from │
   └─────────┘ └─────────┘ │  public site)│
                           └──────┬───────┘
                                  │
                                  ▼
                          ┌───────────────┐
                          │     Service   │
                          │               │
                          └───────┬───────┘
                                  │
                                  ▼
                          ┌───────────────┐
                          │ ServiceFAQ    │
                          │               │
                          └───────────────┘

        ┌──────────────────────────────────────────────┐
        │                                              │
        ▼                                              ▼
    ┌─────────────┐                          ┌──────────────┐
    │  Inquiry    │                          │ TaxDeadline  │
    │ (from       │                          │ (auto-pop    │
    │  contact    │                          │  Kenyan)     │
    │  form)      │                          └──────────────┘
    └─────────────┘

        ┌──────────────────────────────────────────────┐
        │                                              │
        ▼                                              ▼
    ┌──────────────┐                          ┌───────────────┐
    │  BlogPost    │                          │ Testimonial   │
    ├──────────────┤                          ├───────────────┤
    │ BlogCategory │                          │  CaseStudy    │
    │ BlogComment  │                          └───────────────┘
    └──────────────┘

    ┌────────────────────────────────────────────────┐
    │              ReminderLog                       │
    │ (tracks email & SMS reminders sent)           │
    └────────────────────────────────────────────────┘
```

---

## Request Flow: Appointment Booking

```
1. User visits /appointments/book/

2. GET Request
   ├─ renders appointments/book_appointment.html
   └─ shows AppointmentForm

3. User fills form and submits (POST)
   ├─ Form validation (AppointmentForm)
   ├─ Create Appointment model instance
   ├─ Save to database
   ├─ Trigger email task to Celery
   ├─ Redirect to booking_success page
   └─ Show success message

4. Asynchronous Email Task (Celery)
   ├─ send_appointment_reminders() task runs
   ├─ 24 hours before appointment:
   │  ├─ Send email via Django Email
   │  ├─ Send SMS via Twilio
   │  └─ Log in ReminderLog model
   └─ Mark reminder_sent flags in Appointment model

5. Admin Dashboard
   ├─ Staff sees appointment in calendar
   ├─ Can view appointment details
   ├─ Can update status (scheduled → confirmed → completed)
   └─ Can see reminder logs
```

---

## Request Flow: Admin Dashboard Access

```
1. Staff member navigates to /admin-dashboard/

2. @login_required decorator
   ├─ Check if user is authenticated
   └─ Redirect to login if not

3. @dashboard_access_required decorator
   ├─ Check DashboardAccessControl
   ├─ Verify can_access_dashboard = True
   └─ Redirect if no permission

4. Dashboard view executes
   ├─ Query metrics:
   │  ├─ new_inquiries count
   │  ├─ scheduled_appointments count
   │  ├─ total_clients count
   │  └─ pending_documents count
   │
   ├─ Get recent data:
   │  ├─ recent_inquiries (5 latest)
   │  ├─ upcoming_appointments (next 7 days)
   │  └─ upcoming_deadlines (next 30 days)
   │
   └─ Pass context to template

5. Template renders dashboard
   ├─ Display 4 metric cards
   ├─ Show recent inquiries table
   ├─ Show upcoming appointments
   ├─ Show tax deadlines
   └─ Display navigation menu

6. Staff can click on sections
   ├─ Inquiries → /admin-dashboard/inquiries/
   │  └─ Filter by status
   │  └─ Click inquiry → /admin-dashboard/inquiries/<id>/
   │     └─ Update status and notes
   │
   ├─ Appointments → /admin-dashboard/appointments/
   │  └─ Calendar view with monthly filter
   │
   ├─ Clients → /admin-dashboard/clients/
   │  └─ Search and filter by type
   │
   └─ Reports → /admin-dashboard/reports/
      └─ View analytics and charts
```

---

## Email System Flow

```
User books appointment
         │
         ▼
Appointment created
         │
         ├─ IMMEDIATE: send_confirmation_email()
         │  └─ Django Email backend
         │     └─ SMTP to user
         │
         └─ SCHEDULED: Celery Beat (every hour)
            └─ Check for appointments in next 24 hours
               └─ If not already sent reminder:
                  ├─ Send email reminder
                  ├─ Send SMS via Twilio
                  └─ Log in ReminderLog
```

---

## Color Scheme Implementation

```
PRIMARY RED (#DC143C)
├─ CTA Buttons (Book Now, Submit)
├─ Important badges
├─ Section underlines
├─ Hover states
└─ Alert highlights

DARK BLACK (#1A1A1A)
├─ Navigation bar
├─ Admin sidebar
├─ Headers
├─ Main text
└─ Emphasis elements

WHITE (#FFFFFF)
├─ Page background
├─ Card backgrounds
├─ Text on dark backgrounds
└─ "Clean" sections

LIGHT GRAY (#F5F5F5)
├─ Secondary backgrounds
├─ Section dividers
└─ Admin dashboard background
```

---

## Development Timeline Estimate

```
Phase 1: Frontend Templates (7-10 days)
├─ Homepage and hero section
├─ Services pages
├─ Appointment booking form
├─ Blog pages
├─ Client portal pages
├─ Admin dashboard pages
└─ Email templates

Phase 2: Integration & Testing (5-7 days)
├─ Form to view connections
├─ Email/SMS configuration
├─ Celery task testing
├─ Database testing
├─ User flow testing
└─ Browser compatibility

Phase 3: Deployment (3-5 days)
├─ Server setup
├─ Database migration
├─ SSL/HTTPS configuration
├─ Email/SMS credentials
├─ Static files deployment
└─ Monitoring setup

TOTAL: 3-4 weeks to production launch
```

---

This architecture is:
✅ Scalable - Can handle multiple users
✅ Maintainable - Clean separation of concerns
✅ Extensible - Easy to add new features
✅ Reliable - Error handling and logging
✅ Secure - Authentication and authorization
✅ Professional - Production-ready code
