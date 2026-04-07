#!/usr/bin/env python
"""
Manually migrate - run migrations even if they seem to have already been attempted
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command

print("=" * 80)
print("FORCE RUNNING ALL PENDING MIGRATIONS")
print("=" * 80)

try:
    # Show pending migrations first
    call_command('showmigrations', '--plan')
    print("\n" + "=" * 80)
    print("APPLYING MIGRATIONS...")
    print("=" * 80 + "\n")
    
    # Apply all migrations
    call_command('migrate', verbosity=2)
    
    print("\n" + "=" * 80)
    print("✓ MIGRATIONS COMPLETE")
    print("=" * 80)
except Exception as e:
    print(f"\n✗ Migration error: {e}")
    sys.exit(1)
