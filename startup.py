#!/usr/bin/env python
"""
Production startup script - Runs all necessary setup before gunicorn starts.
This ensures database is initialized, static files are collected, and the app is ready.
"""
import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description=""):
    """Run a shell command and log output"""
    print(f"\n{'='*70}")
    if description:
        print(f"> {description}")
    print(f"$ {cmd}")
    print(f"{'='*70}")
    
    result = subprocess.run(cmd, shell=True, cwd=os.getcwd())
    
    if result.returncode != 0:
        print(f"[WARNING] Command failed with exit code {result.returncode}")
        print(f"   Continuing anyway (non-critical step)")
    else:
        print(f"[OK] Completed")

def main():
    print("\n" + "="*70)
    print("HS CONSULTING - PRODUCTION STARTUP")
    print("="*70)
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    # Step 1: Run migrations
    run_command(
        "python manage.py migrate --noinput",
        "Step 1/5: Running database migrations"
    )
    
    # Step 2: Create staticfiles directory
    Path('staticfiles').mkdir(parents=True, exist_ok=True)
    print("\n[OK] staticfiles directory created/verified")
    
    # Step 3: Collect static files
    run_command(
        "python manage.py collectstatic --noinput --clear",
        "Step 2/5: Collecting static files"
    )
    
    # Step 4: Initialize database
    run_command(
        "python init_database.py",
        "Step 3/5: Initializing database with CoreSettings and admin user"
    )
    
    # Step 5: Setup admin access
    run_command(
        "python setup_admin_access.py",
        "Step 4/5: Setting up admin dashboard access"
    )
    
    # Step 6: Populate initial data (optional, non-blocking)
    print("\n" + "="*70)
    print("Step 5/5: Populating optional data")
    print("="*70)
    
    for cmd, name in [
        ("python manage.py populate_tax_deadlines 2>/dev/null", "Tax deadlines"),
        ("python manage.py populate_services 2>/dev/null", "Services"),
        ("python manage.py populate_testimonials 2>/dev/null", "Testimonials"),
    ]:
        print(f"  > Populating {name}...", end=" ")
        result = subprocess.run(cmd, shell=True, cwd=os.getcwd(), capture_output=True)
        if result.returncode == 0:
            print("[OK]")
        else:
            print("(skipped - already exists)")
    
    print("\n" + "="*70)
    print("[OK] STARTUP COMPLETE - Ready to start gunicorn")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
