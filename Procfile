release: python manage.py migrate --noinput && python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@hsconsulting.co.ke', 'Admin@123')"
web: python manage.py collectstatic --noinput && gunicorn config.wsgi:application --log-file - --timeout 600
