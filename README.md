# HS Consulting - Professional Website

A complete Django web application for HS Consulting, a tax consulting and financial services firm in Kenya.

## 🎯 Features

### Frontend Features
- **Responsive Website** with Red, Black & White color scheme
- **Service Showcase** - Display all tax consulting services
- **Appointment Booking System** - Online appointment scheduling
- **Contact/Inquiry Form** - Lead capture and management
- **Tax Calendar** - Auto-populated Kenyan tax deadlines
- **Blog** - Articles for SEO and thought leadership
- **Testimonials & Case Studies**
- **Client Portal** - Secure document upload and management

### Admin Dashboard (Staff)
- **Inquiry Management** - Track and manage client inquiries with status updates
- **Appointment Management** - Calendar view, scheduling, client tracking
- **Client Directory** - Complete client profiles with history
- **Automated Reminders** - Email and SMS reminders 24 hours before appointments
- **Tax Deadline Tracking** - Auto-populated with Kenyan tax calendar
- **Reports & Analytics** - Insights into business metrics
- **Blog Management** - Create and publish articles
- **User Access Control** - Manage permissions for 2 team members
- **Activity Logging** - Track all staff actions

### Client Portal
- **Dashboard** - View appointments and documents
- **Secure Login** - Email/password authentication
- **Document Upload** - Upload tax returns, financial statements, etc.
- **Service History** - Track all services provided
- **Appointment History** - View past and upcoming appointments

## 🛠 Tech Stack

- **Backend**: Python Django 4.2
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Task Queue**: Celery with Redis
- **Email**: Django Email with SMTP
- **SMS**: Twilio integration
- **API**: Django REST Framework

## 📋 Project Structure

```
hsconsulting/
├── config/                 # Settings & Configuration
├── apps/
│   ├── core/              # Homepage & pages
│   ├── services/          # Services management
│   ├── appointments/      # Booking & tax calendar
│   ├── inquiries/         # Contact form & leads
│   ├── clients/           # Client portal
│   ├── blog/              # Articles
│   ├── testimonials/      # Reviews & case studies
│   ├── accounts/          # Auth
│   └── admin_dashboard/   # Staff dashboard
├── templates/             # HTML templates
├── static/                # CSS, JS, images
├── media/                 # Uploaded files
└── requirements.txt       # Dependencies
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9+
- Git
- Redis (for Celery)
- PostgreSQL (recommended for production)

### 1. Clone & Setup

```bash
cd c:\Users\Ibnuhassan\Desktop\projects\hsconsulting

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy example env file
copy .env.example .env

# Update .env with your settings
```

### 2. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 3. Create Initial Data (Kenyan Tax Calendar)

```bash
python manage.py shell
```

Then in the shell:
```python
from apps.appointments.models import TaxDeadline
from datetime import date

# Add Kenyan tax deadlines
deadlines = [
    TaxDeadline(
        name="VAT Returns Due",
        description="Monthly VAT return submission deadline",
        deadline_date=date(2026, 2, 20),
        deadline_type='vat',
        recurring=True,
    ),
    # Add more deadlines as needed...
]

for deadline in deadlines:
    deadline.save()
```

### 4. Create Admin User

```bash
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
# Terminal 1: Django development server
python manage.py runserver

# Terminal 2: Celery for background tasks (optional)
celery -A config worker -l info

# Terminal 3: Celery Beat for scheduled tasks (optional)
celery -A config beat -l info
```

Visit: `http://localhost:8000`

## 📊 Admin Setup

1. Go to `http://localhost:8000/admin/`
2. Login with superuser credentials
3. Grant dashboard access to staff:
   - Go to "Dashboard Access Control"
   - Create entry for each staff member
   - Check required permissions

## 🔧 Configuration

### Email Setup (Gmail Example)

1. Create an [App Password](https://myaccount.google.com/apppasswords)
2. Add to `.env`:
```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### SMS Reminders (Twilio)

1. Sign up at [Twilio.com](https://www.twilio.com)
2. Get your Account SID, Auth Token, and Phone Number
3. Add to `.env`:
```
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
TWILIO_PHONE_NUMBER=+1234567890
```

### Tax Calendar Dates

Update Kenyan tax deadlines in Django admin:
- `/admin/appointments/taxdeadline/`

Current deadlines include:
- Monthly VAT (20th of each month)
- Monthly PAYE (10th of each month)
- Quarterly Excise Duty
- Annual Income Tax Returns
- VAT Registration deadline
- ETIMS compliance deadlines

## 🎨 Customization

### Colors
Edit `static/css/style.css`:
```css
:root {
    --primary-red: #DC143C;    /* Change red here */
    --dark-black: #1A1A1A;     /* Change black here */
    --light-white: #FFFFFF;    /* White stays same */
}
```

### Services
Add services in Django admin:
- `/admin/services/service/`

Each service can have FAQs attached.

### Blog
Create blog posts in Django admin:
- `/admin/blog/blogpost/`

Publish and mark as featured to control visibility.

## 📱 Mobile Reminders

The system automatically sends:
- **Email Reminders** - 24 hours before appointment
- **SMS Reminders** - 24 hours before appointment (if Twilio configured)

Configure in `config/tasks.py`

## 🔐 Security Checklist

Before going live:

- [ ] Change `DJANGO_SECRET_KEY` in `.env`
- [ ] Set `DEBUG=False` in production
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure HTTPS/SSL
- [ ] Set up backups
- [ ] Configure email properly
- [ ] Set `ALLOWED_HOSTS` correctly
- [ ] Use environment-specific settings
- [ ] Enable CSRF protection
- [ ] Set up logging

## 📞 Support & Contact

For issues or questions:
- Email: ibrahimhussein481@gmail.com
- Phone: 0729592895
- WhatsApp: 0746645534
- Website: hsconsulting.co.ke

## 📄 License

This project is proprietary to HS Consulting.

---

**Last Updated**: March 2026
**Version**: 1.0.0
