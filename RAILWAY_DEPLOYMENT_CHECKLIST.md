# Railway Deployment Checklist ✅

## **Files to Delete (Render-related, no longer needed)**
- `render_init.py` - Delete
- `render_hard_reset.py` - Delete
- `render_deploy_fix.py` - Delete
- `render.yaml` - Delete

These files were for Render deployment. Railway uses `railway.toml` instead.

---

## **Email Functionality - UPDATED ✅**

### **Appointments:**
- ✅ Client receives confirmation email when booking
- ✅ Owner receives notification email when booking is made
- Email methods: `send_confirmation_email()`

### **Inquiries (Contact Us):**
- ✅ Client receives confirmation email
- ✅ Owner receives notification email
- Email methods: `send_confirmation_email()` and `send_owner_notification()`

### **Configuration Updated:**
- [config/settings.py](config/settings.py) - Added `OWNER_EMAIL` setting
- [.env.example](.env.example) - Updated for Railway + added `OWNER_EMAIL`
- [apps/inquiries/models.py](apps/inquiries/models.py) - Added email methods
- [apps/inquiries/views.py](apps/inquiries/views.py) - Sends emails on form submission
- [apps/appointments/models.py](apps/appointments/models.py) - Now sends to both client and owner

---

## **Email Templates Needed**

You need to create these email templates in `templates/emails/`:

### 1. `appointment_confirmation.html`
- Sent to client after booking
- Show appointment date, time, service

### 2. `appointment_notification_owner.html`
- Sent to owner when booking is made
- Show client details & appointment info

### 3. `inquiry_confirmation.html`
- Sent to client after contact form submission
- Thank you message

### 4. `inquiry_notification_owner.html`
- Sent to owner when inquiry received
- Show inquiry details & client contact info

---

## **Railway Environment Variables to Set**

In Railway Dashboard → Variables:

```
DEBUG=False
ALLOWED_HOSTS=your-railway-domain.railway.app
SECRET_KEY=<generate-new-secret-key>
OWNER_EMAIL=owner@hsconsulting.co.ke

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Partner Information
PARTNER_1_EMAIL=info@hsconsulting.co.ke
PARTNER_1_PHONE=+254729592895
PARTNER_2_EMAIL=ibrahimhussein481@gmail.com
PARTNER_2_PHONE=+254746645534

ADMIN_PASSWORD=<strong-password>
SITE_NAME=HS Consulting
```

DATABASE_URL will be auto-populated by Railway when you add PostgreSQL.

---

## **Next Steps**

1. ✅ Delete render files (listed above)
2. ✅ Create email templates (4 files needed)
3. ✅ Push to GitHub
4. ✅ Create Railway project and connect GitHub
5. ✅ Set environment variables in Railway
6. ✅ Deploy!

---

## **Testing Email Locally**

Before deploying, test emails locally by setting:

```
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

This prints emails to console instead of sending.

When ready for production:
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```
