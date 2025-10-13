#!/usr/bin/env python
"""Create JSON database backup using Django management command style."""

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


def create_json_backup(target_file=None):
    """Create a JSON database backup."""
    if target_file is None:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        base_path = "reports/database_backups/json_exports/"
        output_file = f"{base_path}json_backup_{timestamp}.json"
    else:
        output_file = target_file

    print('Exporting database to JSON...')

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

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    notes_count = len(data['sticky_notes'])
    users_count = len(data['users'])

    print(f'✅ JSON Export completed: {output_file}')
    print(f'   - {notes_count} sticky notes exported')
    print(f'   - {users_count} users exported')

    return output_file


if __name__ == '__main__':
    provided_file = sys.argv[1] if len(sys.argv) > 1 else None
    create_json_backup(provided_file)
