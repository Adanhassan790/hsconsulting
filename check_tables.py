#!/usr/bin/env python
"""Check database tables"""
import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tables = cursor.fetchall()

if tables:
    print("Database Tables:")
    print("=" * 50)
    for table in tables:
        print(f"  - {table[0]}")
    print("=" * 50)
    
    # Check for core_coresettings specifically
    if any('coresettings' in t[0] for t in tables):
        print("\n✓ core_coresettings table EXISTS")
    else:
        print("\n✗ core_coresettings table NOT FOUND!")
else:
    print("ERROR: Database has NO TABLES!")

conn.close()
