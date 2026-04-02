release: python manage.py makemigrations --noinput && python manage.py migrate --noinput && python manage.py collectstatic --noinput
web: python manage.py makemigrations --noinput; python manage.py migrate --noinput; python manage.py collectstatic --noinput; exec gunicorn config.wsgi:application --log-file - --timeout 600
