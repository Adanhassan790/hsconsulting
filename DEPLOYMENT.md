# DEPLOYMENT GUIDE - HS Consulting

## Pre-Deployment Checklist

### 1. Environment Preparation

- [ ] Update `.env` with production settings
- [ ] Change `DJANGO_SECRET_KEY` to a random secure string
- [ ] Set `DEBUG = False`
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Configure database (PostgreSQL recommended)
- [ ] Set up Redis for Celery
- [ ] Configure email (Gmail, SendGrid, or custom SMTP)
- [ ] Set up Twilio for SMS (optional but recommended)

### 2. Security Configuration

```bash
# Generate a secure secret key
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Update `.env`:
```
DEBUG=False
DJANGO_SECRET_KEY=<generated-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 3. Database Migration

```bash
# Use PostgreSQL in production
python manage.py migrate --database=production

# Create superuser
python manage.py createsuperuser

# Load tax calendar
python create_fixtures.py
python manage.py loaddata kenyan_tax_calendar.json
```

### 4. Static Files

```bash
# Collect static files
python manage.py collectstatic --noinput

# Upload to S3 or CDN (optional but recommended)
# Configure AWS_STORAGE_BUCKET_NAME in .env
```

## Deployment Options

### Option A: Heroku Deployment

#### 1. Install Heroku CLI

```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

#### 2. Prepare for Heroku

Create `Procfile`:
```
web: gunicorn config.wsgi
worker: celery -A config worker -l info
beat: celery -A config beat -l info
```

Create `runtime.txt`:
```
python-3.11.0
```

#### 3. Deploy

```bash
heroku login
heroku create your-app-name
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# Load tax calendar
heroku run python create_fixtures.py
heroku run python manage.py loaddata kenyan_tax_calendar.json
```

### Option B: Traditional VPS (AWS EC2, DigitalOcean, etc.)

#### 1. Server Setup

```bash
# SSH into your server
ssh ubuntu@your_server_ip

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install python3.11 python3-pip python3-venv postgresql redis-server nginx git

# Clone repository
git clone your-repo-url
cd hsconsulting
```

#### 2. Django Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure .env
nano .env
# Update all production settings

# Database setup
python manage.py migrate
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

#### 3. Gunicorn Setup

Install Gunicorn:
```bash
pip install gunicorn
```

Create `/etc/systemd/system/hsconsulting.service`:
```ini
[Unit]
Description=HS Consulting Django App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/hsconsulting
ExecStart=/home/ubuntu/hsconsulting/venv/bin/gunicorn \
    --workers 4 \
    --bind 127.0.0.1:8000 \
    config.wsgi:application

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable hsconsulting
sudo systemctl start hsconsulting
```

#### 4. Nginx Configuration

Create `/etc/nginx/sites-available/hsconsulting`:
```nginx
upstream hsconsulting {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com www.yourdomain.com;

    # SSL certificates (use Let's Encrypt with Certbot)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Static files
    location /static/ {
        alias /home/ubuntu/hsconsulting/staticfiles/;
        expires 30d;
    }

    # Media files
    location /media/ {
        alias /home/ubuntu/hsconsulting/media/;
        expires 7d;
    }

    # Proxy requests
    location / {
        proxy_pass http://hsconsulting;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/hsconsulting /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 5. SSL Certificate (Let's Encrypt)

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com
```

#### 6. Celery Setup

Create `/etc/systemd/system/celery-worker.service`:
```ini
[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=ubuntu
WorkingDirectory=/home/ubuntu/hsconsulting
ExecStart=/home/ubuntu/hsconsulting/venv/bin/celery -A config worker \
    --loglevel=info \
    --logfile=/var/log/celery/%n%I.log \
    --pidfile=/var/run/celery/%n.pid \
    --uid=ubuntu \
    --gid=ubuntu \
    --detach

[Install]
WantedBy=multi-user.target
```

Create `/etc/systemd/system/celery-beat.service`:
```ini
[Unit]
Description=Celery Beat Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/hsconsulting
ExecStart=/home/ubuntu/hsconsulting/venv/bin/celery -A config beat \
    --loglevel=info

[Install]
WantedBy=multi-user.target
```

Enable services:
```bash
sudo systemctl enable celery-worker celery-beat
sudo systemctl start celery-worker celery-beat
```

### Option C: Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: hsconsulting
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: your_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:your_password@db:5432/hsconsulting
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  celery:
    build: .
    command: celery -A config worker -l info
    depends_on:
      - redis
      - db

  beat:
    build: .
    command: celery -A config beat -l info
    depends_on:
      - redis
      - db

volumes:
  postgres_data:
```

Deploy:
```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## Post-Deployment

### 1. Monitoring & Logging

```bash
# View Django logs
tail -f logs/django.log

# View Celery logs
tail -f logs/celery.log

# Monitor processes
systemctl status hsconsulting
systemctl status celery-worker
systemctl status celery-beat
```

### 2. Backups

Setup automatic database backups:
```bash
# Create backup script
nano backup_db.sh
```

```bash
#!/bin/bash
pg_dump hsconsulting | gzip > /backups/db_$(date +%Y%m%d_%H%M%S).sql.gz
```

Add to crontab:
```bash
0 2 * * * /home/ubuntu/hsconsulting/backup_db.sh
```

### 3. Updates & Maintenance

```bash
# Pull latest changes
git pull origin main

# Install new dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Restart services
sudo systemctl restart hsconsulting
sudo systemctl restart celery-worker
```

## Troubleshooting

### Static files not loading
```bash
python manage.py collectstatic --noinput
# Check Nginx configuration for static location
```

### Emails not sending
- Verify email credentials in `.env`
- Check spam folder
- Review email logs: `python manage.py shell` then `from apps.appointments.models import Appointment`

### Celery not working
```bash
# Check Redis connection
redis-cli ping

# Check Celery worker logs
journalctl -u celery-worker -f

# Restart Celery
sudo systemctl restart celery-worker celery-beat
```

### Database issues
```bash
# Check database connection
psql -U postgres -d hsconsulting

# Run migrations
python manage.py migrate

# Clear cache if needed
python manage.py clear_cache
```

## Monitoring Commands

```bash
# Check disk usage
df -h

# Check memory usage
free -h

# Check running processes
ps aux | grep python

# Check system logs
journalctl -n 50

# Monitor Nginx
sudo systemctl status nginx
```

## SSL/HTTPS renewal

```bash
# Renew certificate (automatic after setup)
sudo certbot renew --dry-run  # Test
sudo certbot renew            # Actual renewal
```

---

**Support**: For issues, check logs and Django error messages carefully. Most issues are environmental configuration problems.
