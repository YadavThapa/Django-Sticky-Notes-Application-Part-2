#!/usr/bin/env python
"""Check database state and create table if needed."""
import os
import sys

import django
from django.db import connection

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()


def check_and_create_table():
    """Check if the StickyNote table exists and create it if not."""
    with connection.cursor() as cursor:
        # Check if table exists
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='sticky_notes_stickynote'
        """)
        table_exists = cursor.fetchone()

        if table_exists:
            print("Table sticky_notes_stickynote already exists")
        else:
            print("Table sticky_notes_stickynote does not exist, creating...")

            # Create the table manually
            cursor.execute("""
                CREATE TABLE sticky_notes_stickynote (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR(200) NOT NULL,
                    content TEXT NOT NULL,
                    created_at DATETIME NOT NULL,
                    updated_at DATETIME NOT NULL
                )
            """)
            print("Table created successfully")

        # List all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        all_tables = cursor.fetchall()
        print("All tables:", [table[0] for table in all_tables])


if __name__ == "__main__":
    check_and_create_table()