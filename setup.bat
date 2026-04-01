@echo off
REM Setup script for HS Consulting Django Project (Windows)
REM Run this after cloning the repository

echo ======================================
echo HS Consulting - Setup Script (Windows)
echo ======================================
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Copy environment file
echo Setting up environment variables...
if not exist .env (
    copy .env.example .env
    echo. & echo WARNING: Please update .env with your configuration & echo.
)

REM Create database
echo Setting up database...
python manage.py makemigrations
python manage.py migrate

REM Create superuser
echo Creating superuser account...
python manage.py createsuperuser

REM Generate Kenyan tax calendar
echo Generating Kenyan tax calendar...
python create_fixtures.py
python manage.py loaddata kenyan_tax_calendar.json

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

echo.
echo ======================================
echo Setup Complete!
echo ======================================
echo.
echo Next steps:
echo 1. Update .env with your email and Twilio settings
echo 2. Run: python manage.py runserver
echo 3. Visit: http://localhost:8000
echo 4. Admin: http://localhost:8000/admin
echo.
pause
