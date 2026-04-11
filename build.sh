#!/bin/bash
set -o errexit

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Initializing database..."
python init_database.py

echo "Setting up admin dashboard access control..."
python setup_admin_access.py 2>/dev/null || echo "Dashboard access already configured"

echo "Populating initial data..."
python manage.py populate_tax_deadlines 2>/dev/null || echo "Tax deadlines already populated"
python manage.py populate_services 2>/dev/null || echo "Services already populated"
python manage.py populate_testimonials 2>/dev/null || echo "Testimonials already populated"

echo "Build complete!"
