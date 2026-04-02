release: python manage.py startup
web: python manage.py startup; gunicorn config.wsgi:application --log-file - --timeout 600
