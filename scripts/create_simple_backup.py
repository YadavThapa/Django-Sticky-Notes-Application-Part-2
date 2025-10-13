#!/usr/bin/env python
"""Create a simple, clean database backup similar to the original format."""

import os
import sys
import json
from datetime import datetime

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sticky_notes_config.settings')

try:
    import django
    django.setup()
    from django.contrib.auth.models import User
    from sticky_notes_app.models import StickyNote
except ImportError as e:
    print(f"Error importing Django: {e}")
    sys.exit(1)


def create_simple_backup():
    """Create a simple backup in the same format as the original."""
    print("Creating simple database backup...")

    data = {
        'export_date': datetime.now().isoformat(),
        'sticky_notes': [],
        'users': []
    }

    for note in StickyNote.objects.all():
        data['sticky_notes'].append({
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'created_at': note.created_at.isoformat(),
            'updated_at': note.updated_at.isoformat()
        })

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

    output_file = (
        "reports/database_backups/json_exports/my_database_backup.json"
    )

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Simple backup created: {output_file}")
    print(f"   📝 {len(data['sticky_notes'])} sticky notes")
    print(f"   👤 {len(data['users'])} users")

    return output_file


if __name__ == '__main__':
    create_simple_backup()
