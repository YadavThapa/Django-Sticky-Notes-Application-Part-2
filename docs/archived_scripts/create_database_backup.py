#!/usr/bin/env python
"""Create a comprehensive database backup for the sticky notes project."""

import os
import sys
import json
from datetime import datetime

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'sticky_notes_config.settings')

try:
    import django
    django.setup()
    from django.contrib.auth.models import User
    from sticky_notes_app.models import StickyNote
except ImportError as e:
    print(f"Error importing Django: {e}")
    sys.exit(1)


def create_database_backup(output_filename=None):
    """Create a comprehensive database backup."""
    if output_filename is None:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_filename = f"reports/database_backup_{timestamp}.json"

    print("Creating database backup...")

    data = {
        'backup_info': {
            'export_date': datetime.now().isoformat(),
            'project_name': 'Sticky Notes Application',
            'django_version': django.get_version(),
            'backup_type': 'Complete Database Export'
        },
        'sticky_notes': [],
        'users': []
    }

    # Export sticky notes
    notes_count = 0
    for note in StickyNote.objects.all():
        data['sticky_notes'].append({
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'created_at': note.created_at.isoformat(),
            'updated_at': note.updated_at.isoformat()
        })
        notes_count += 1

    # Export users (basic info only, no sensitive data)
    users_count = 0
    for user in User.objects.all():
        data['users'].append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'date_joined': user.date_joined.isoformat(),
            'last_login': (
                user.last_login.isoformat() if user.last_login else None
            )
        })
        users_count += 1

    # Write backup file
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("✅ Database backup created successfully!")
    print(f"   📄 File: {output_filename}")
    print(f"   📝 Sticky Notes: {notes_count}")
    print(f"   👤 Users: {users_count}")
    print(f"   📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return output_filename


if __name__ == '__main__':
    # Check if output file is provided as argument
    provided_file = sys.argv[1] if len(sys.argv) > 1 else None
    create_database_backup(provided_file)
