#!/usr/bin/env python
"""Fix corrupted database"""
import os
import sys
import sqlite3

db_path = 'db.sqlite3'

print(f"Checking database at {db_path}...")
print("=" * 70)

# Drop all tables BEFORE Django loads
print("\n1. Dropping all existing tables...")
try:
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path, timeout=5)
        conn.isolation_level = None  # Autocommit mode
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        # Drop each table
        for table in tables:
            table_name = table[0]
            if table_name != 'sqlite_sequence':  # Skip system table
                print(f"   Dropping {table_name}...")
                try:
                    cursor.execute(f'DROP TABLE IF EXISTS "{table_name}";')
                except:
                    pass
        
        conn.close()
        print("✓ All tables dropped")
except Exception as e:
    print(f"WARNING: {e}")
    # Continue anyway

# Now run migrations
print("\n2. Running migrations...")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.core.management import call_command

try:
    call_command('migrate', '--noinput', verbosity=2)
    print("\n✓ Migrations completed successfully")
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ Database has been recreated successfully!")
print("=" * 70)
