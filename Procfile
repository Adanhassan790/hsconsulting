release: bash build.sh
web: gunicorn config.wsgi:application --workers 2 --worker-class sync --bind 0.0.0.0:8080 --timeout 600 --log-level info
