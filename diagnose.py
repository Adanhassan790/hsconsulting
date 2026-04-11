#!/usr/bin/env python
"""
Simple diagnostic script to check what's wrong with production startup
"""
import os
import sys
import subprocess
from pathlib import Path

print("\n" + "="*80)
print("DIAGNOSTIC CHECK - What's wrong with startup?")
print("="*80 + "\n")

# Check Python
print(f"[1] Python: {sys.executable}")
print(f"    Version: {sys.version.split()[0]}")

# Check Git
print(f"\n[2] Git availability:")
result = subprocess.run("git --version", shell=True, capture_output=True, text=True)
print(f"    {result.stdout.strip() if result.returncode == 0 else 'GIT NOT FOUND'}")

# Check working directory
print(f"\n[3] Working directory: {os.getcwd()}")
result = subprocess.run("ls -la", shell=True, capture_output=True, text=True)
print(f"    Contents:")
for line in result.stdout.split('\n')[:15]:
    if line.strip():
        print(f"      {line}")

# Check static files before
print(f"\n[4] Static files BEFORE collectstatic:")
staticfiles = Path('staticfiles')
if staticfiles.exists():
    count = sum(1 for _ in staticfiles.rglob('*') if _.is_file())
    print(f"    Directory exists: YES ({count} files)")
else:
    print(f"    Directory exists: NO")

# Try to run collectstatic manually
print(f"\n[5] Running: python manage.py collectstatic --noinput --clear")
print("-" * 80)
result = subprocess.run(
    "python manage.py collectstatic --noinput --clear",
    shell=True,
    capture_output=True,
    text=True,
    timeout=30
)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
print(f"Return code: {result.returncode}")
print("-" * 80)

# Check static files after
print(f"\n[6] Static files AFTER collectstatic:")
if staticfiles.exists():
    count = sum(1 for _ in staticfiles.rglob('*') if _.is_file())
    print(f"    Total files: {count}")
    
    # List first 20 files
    files = list(staticfiles.rglob('*'))[:20]
    print(f"    First files:")
    for f in files:
        if f.is_file():
            rel = f.relative_to(staticfiles)
            print(f"      - {rel}")
else:
    print(f"    Directory does not exist!")

# Try migrations
print(f"\n[7] Running: python manage.py migrate --noinput")
print("-" * 80)
result = subprocess.run(
    "python manage.py migrate --noinput",
    shell=True,
    capture_output=True,
    text=True,
    timeout=30
)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr[:500])
print(f"Return code: {result.returncode}")
print("-" * 80)

# Check database
print(f"\n[8] Database check:")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
try:
    import django
    django.setup()
    from django.db import connections
    
    conn = connections['default']
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1")
        print(f"    [OK] Database connected")
    
    # Check if CoreSettings table exists
    try:
        from apps.core.models import CoreSettings
        count = CoreSettings.objects.count()
        print(f"    [OK] CoreSettings table exists ({count} records)")
    except Exception as e:
        print(f"    [ERROR] CoreSettings error: {type(e).__name__}: {str(e)[:100]}")
        
except Exception as e:
    print(f"    [ERROR] {type(e).__name__}: {str(e)[:200]}")

print("\n" + "="*80)
print("DIAGNOSTIC COMPLETE")
print("="*80 + "\n")
