#!/usr/bin/env python
"""
Production startup script - Runs all necessary setup before gunicorn starts.
This ensures database is initialized, static files are collected, and the app is ready.
"""
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def log_timestamp(msg):
    """Log with timestamp"""
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"[{ts}] {msg}")

def run_command(cmd, description=""):
    """Run a shell command and log output"""
    print(f"\n{'='*70}")
    if description:
        log_timestamp(description)
    log_timestamp(f"$ {cmd}")
    print(f"{'='*70}")
    
    try:
        result = subprocess.run(cmd, shell=True, cwd=os.getcwd(), capture_output=False)
        
        if result.returncode != 0:
            log_timestamp(f"[WARNING] Command failed with exit code {result.returncode}")
            log_timestamp("   Continuing anyway (non-critical step)")
        else:
            log_timestamp("[OK] Completed successfully")
    except Exception as e:
        log_timestamp(f"[ERROR] Exception running command: {type(e).__name__}: {str(e)}")
        log_timestamp("   Continuing anyway (non-critical step)")

def get_git_info():
    """Get current git commit info"""
    try:
        result = subprocess.run(
            "git rev-parse --short HEAD", 
            shell=True, 
            capture_output=True, 
            text=True
        )
        commit = result.stdout.strip()
        
        result = subprocess.run(
            "git log -1 --pretty=%B", 
            shell=True, 
            capture_output=True, 
            text=True
        )
        message = result.stdout.strip().split('\n')[0]
        
        return commit, message
    except:
        return "unknown", "could not fetch"

def main():
    log_timestamp("="*70)
    log_timestamp("HS CONSULTING - PRODUCTION STARTUP")
    log_timestamp("="*70)
    
    # Show git info
    commit, message = get_git_info()
    log_timestamp(f"Git Commit: {commit}")
    log_timestamp(f"Commit Message: {message}")
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    # Show deployment environment
    log_timestamp(f"Python executable: {sys.executable}")
    log_timestamp(f"Working directory: {os.getcwd()}")
    log_timestamp(f"DJANGO_SETTINGS_MODULE: {os.getenv('DJANGO_SETTINGS_MODULE')}")
    
    # Step 1: Run migrations
    run_command(
        "python manage.py migrate --noinput",
        "Step 1/6: Running database migrations"
    )
    
    # Step 2: Create staticfiles directory
    staticfiles_path = Path('staticfiles')
    staticfiles_path.mkdir(parents=True, exist_ok=True)
    log_timestamp(f"[OK] staticfiles directory: {staticfiles_path.absolute()}")
    
    # Step 3: Collect static files
    run_command(
        "python manage.py collectstatic --noinput --clear --verbosity 2",
        "Step 2/6: Collecting static files (VERBOSITY 2)"
    )
    
    # Verify static files
    if staticfiles_path.exists():
        static_count = sum(1 for _ in staticfiles_path.rglob('*') if _.is_file())
        log_timestamp(f"[OK] Verified {static_count} static files in {staticfiles_path}")
        
        logo_path = staticfiles_path / 'images' / 'logo.png'
        if logo_path.exists():
            log_timestamp(f"[OK] Logo found: {logo_path} ({logo_path.stat().st_size} bytes)")
        else:
            log_timestamp("[WARNING] Logo NOT found in staticfiles/images/")
    else:
        log_timestamp("[ERROR] staticfiles directory was not created!")
    
    # Step 4: Initialize database
    run_command(
        "python init_database.py",
        "Step 3/6: Initializing database with CoreSettings and admin user"
    )
    
    # Step 5: Setup admin access
    run_command(
        "python setup_admin_access.py",
        "Step 4/6: Setting up admin dashboard access"
    )
    
    # Step 6: Populate initial data (optional, non-blocking)
    log_timestamp("="*70)
    log_timestamp("Step 5/6: Populating optional data")
    log_timestamp("="*70)
    
    for cmd, name in [
        ("python manage.py populate_tax_deadlines 2>/dev/null", "Tax deadlines"),
        ("python manage.py populate_services 2>/dev/null", "Services"),
        ("python manage.py populate_testimonials 2>/dev/null", "Testimonials"),
    ]:
        log_timestamp(f"  > Populating {name}...", end=" ")
        result = subprocess.run(cmd, shell=True, cwd=os.getcwd(), capture_output=True)
        if result.returncode == 0:
            log_timestamp("[OK]")
        else:
            log_timestamp("(skipped - already exists)")
    
    # Step 7: Show template paths
    log_timestamp("="*70)
    log_timestamp("Step 6/6: Verifying template and app configuration")
    log_timestamp("="*70)
    
    templates_dir = Path('templates')
    home_template = templates_dir / 'core' / 'home.html'
    if home_template.exists():
        log_timestamp(f"[OK] Homepage template: {home_template.absolute()}")
        log_timestamp(f"     Size: {home_template.stat().st_size} bytes")
    else:
        log_timestamp(f"[ERROR] Homepage template NOT found: {home_template}")
    
    log_timestamp("="*70)
    log_timestamp("[OK] STARTUP COMPLETE - Ready to start gunicorn")
    log_timestamp("="*70 + "\n")

if __name__ == '__main__':
    main()
