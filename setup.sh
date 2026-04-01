#!/bin/bash
# Setup script for HS Consulting Django Project
# Run this after cloning the repository

echo "======================================"
echo "HS Consulting - Setup Script"
echo "======================================"

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/Scripts/activate  # For Windows: venv\Scripts\activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Copy environment file
echo "Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration"
fi

# Create database
echo "Setting up database..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo "Creating superuser account..."
python manage.py createsuperuser

# Generate Kenyan tax calendar
echo "Generating Kenyan tax calendar..."
python create_fixtures.py
python manage.py loaddata kenyan_tax_calendar.json

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "======================================"
echo "✅ Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Update .env with your email and Twilio settings"
echo "2. Run: python manage.py runserver"
echo "3. Visit: http://localhost:8000"
echo "4. Admin: http://localhost:8000/admin"
echo ""
