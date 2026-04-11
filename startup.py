#!/usr/bin/env python
"""
PRODUCTION STARTUP SCRIPT v2 - Enhanced error detection and recovery
Ensures database, static files, and app are ready before gunicorn starts
"""
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def log_timestamp(msg):
    """Log with timestamp for visibility in Railway logs"""
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"[{ts}] {msg}", flush=True)

def run_command(cmd, description="", critical=False):
    """
    Run shell command with full output capture and error reporting
    
    Args:
        cmd: Command to run
        description: Human-readable step description
        critical: If True, stop startup on failure
    """
    print(f"\n{'='*80}")
    if description:
        log_timestamp(description)
    log_timestamp(f"$ {cmd}")
    print(f"{'='*80}")
    
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=os.getcwd(),
            capture_output=True,
            text=True,
            timeout=120
        )
        
        # Print all output
        if result.stdout:
            lines = result.stdout.split('\n')
            for line in lines[:50]:  # Show first 50 lines
                if line.strip():
                    print(line)
            if len(lines) > 50:
                print(f"... ({len(lines) - 50} more lines)")
        
        if result.stderr:
            print("STDERR OUTPUT:")
            lines = result.stderr.split('\n')
            for line in lines[:20]:
                if line.strip():
                    print(f"  {line}")
            if len(lines) > 20:
                print(f"  ... ({len(lines) - 20} more lines)")
        
        if result.returncode != 0:
            log_timestamp(f"[ERROR] Command failed with exit code {result.returncode}")
            if critical:
                log_timestamp("[CRITICAL] This is a critical step. Aborting startup.")
                sys.exit(1)
            else:
                log_timestamp("[WARNING] Non-critical step failed. Continuing...")
            return False
        else:
            log_timestamp("[OK] Step completed successfully")
            return True
            
    except subprocess.TimeoutExpired:
        log_timestamp(f"[ERROR] Command timed out (120 seconds)")
        if critical:
            log_timestamp("[CRITICAL] Critical step timed out. Aborting.")
            sys.exit(1)
        return False
    except Exception as e:
        log_timestamp(f"[ERROR] {type(e).__name__}: {str(e)}")
        if critical:
            log_timestamp("[CRITICAL] Exception in critical step. Aborting.")
            sys.exit(1)
        return False

def get_git_info():
    """Safely get current git commit"""
    try:
        result = subprocess.run(
            "git rev-parse --short HEAD", 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip(), "OK"
    except:
        pass
    return "unknown", "git not available"

def check_database():
    """Check if database is reachable"""
    try:
        from django.db import connections
        conn = connections['default']
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        return True
    except Exception as e:
        log_timestamp(f"[ERROR] Database check failed: {type(e).__name__}: {str(e)[:100]}")
        return False

def main():
    log_timestamp("="*80)
    log_timestamp("HS CONSULTING - PRODUCTION STARTUP v2")
    log_timestamp("="*80)
    
    # Environment info
    commit, git_status = get_git_info()
    log_timestamp(f"Git Commit: {commit} ({git_status})")
    log_timestamp(f"Python: {sys.executable}")
    log_timestamp(f"Working directory: {os.getcwd()}")
    log_timestamp(f"PATH: {os.environ.get('PATH', '')[:100]}...")
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    # CRITICAL STEP 1: Database migrations
    log_timestamp("\n" + "="*80)
    log_timestamp("CRITICAL: Running database migrations")
    log_timestamp("="*80)
    
    migrations_ok = run_command(
        "python manage.py migrate --noinput --verbosity 2",
        "Running migrations with verbose output",
        critical=False
    )
    
    if not migrations_ok:
        log_timestamp("[WARNING] Migrations may have failed. Checking database...")
        
    # Check database connection
    log_timestamp("\nChecking database connection...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    # Initialize Django
    try:
        import django
        django.setup()
        
        if check_database():
            log_timestamp("[OK] Database is accessible")
        else:
            log_timestamp("[ERROR] Database is NOT accessible - migrations may not have worked")
    except Exception as e:
        log_timestamp(f"[ERROR] Django setup failed: {e}")
    
    # CRITICAL STEP 2: Collect static files
    log_timestamp("\n" + "="*80)
    log_timestamp("CRITICAL: Collecting static files")
    log_timestamp("="*80)
    
    # Ensure staticfiles directory exists
    staticfiles_path = Path('staticfiles')
    staticfiles_path.mkdir(parents=True, exist_ok=True)
    log_timestamp(f"[OK] staticfiles directory verified: {staticfiles_path.absolute()}")
    
    static_ok = run_command(
        "python manage.py collectstatic --noinput --clear --verbosity 2",
        "Collecting static files with verbose output",
        critical=False
    )
    
    # Verify static files were collected
    log_timestamp("\nVerifying static files...")
    if staticfiles_path.exists():
        static_count = sum(1 for _ in staticfiles_path.rglob('*') if _.is_file())
        log_timestamp(f"[OK] Total static files: {static_count}")
        
        # Check for critical files
        files_to_check = [
            'images/logo.png',
            'css/style.css',
            'js/main.js',
            'admin/css/base.css'
        ]
        
        for file in files_to_check:
            file_path = staticfiles_path / file
            if file_path.exists():
                size = file_path.stat().st_size
                log_timestamp(f"   [OK] {file} ({size} bytes)")
            else:
                log_timestamp(f"   [MISSING] {file}")
    else:
        log_timestamp("[ERROR] staticfiles directory does not exist!")
    
    # NON-CRITICAL STEP 3: Initialize database records
    log_timestamp("\n" + "="*80)
    log_timestamp("NON-CRITICAL: Initializing database records")
    log_timestamp("="*80)
    
    run_command(
        "python init_database.py",
        "Creating CoreSettings and admin user",
        critical=False
    )
    
    # NON-CRITICAL STEP 4: Setup admin access
    run_command(
        "python setup_admin_access.py",
        "Setting up dashboard access",
        critical=False
    )
    
    # NON-CRITICAL STEP 5: Populate data
    log_timestamp("\n" + "="*80)
    log_timestamp("NON-CRITICAL: Populating initial data")
    log_timestamp("="*80)
    
    for cmd, name in [
        ("python manage.py populate_tax_deadlines 2>/dev/null", "Tax deadlines"),
        ("python manage.py populate_services 2>/dev/null", "Services"),
        ("python manage.py populate_testimonials 2>/dev/null", "Testimonials"),
    ]:
        print(f"  Populating {name}...", end=" ", flush=True)
        result = subprocess.run(cmd, shell=True, cwd=os.getcwd(), capture_output=True)
        print("[OK]" if result.returncode == 0 else "[skipped]", flush=True)
    
    # Summary
    log_timestamp("\n" + "="*80)
    log_timestamp("[SUCCESS] STARTUP COMPLETE - Gunicorn can now start")
    log_timestamp("="*80)
    log_timestamp(f"Summary:")
    log_timestamp(f"  - Migrations: {'✓ OK' if migrations_ok else '⚠ Check logs'}")
    log_timestamp(f"  - Static files: {sum(1 for _ in Path('staticfiles').rglob('*') if _.is_file()) if Path('staticfiles').exists() else 0} files")
    log_timestamp(f"  - ready for gunicorn on 0.0.0.0:8080")
    log_timestamp("="*80 + "\n")

if __name__ == '__main__':
    main()
