"""Export database to readable JSON format."""

import json
from datetime import datetime
from typing import TYPE_CHECKING
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from sticky_notes_app.models import StickyNote

if TYPE_CHECKING:
    # This helps the type checker understand Django model managers
    from django.db.models import Manager
    StickyNote.objects: Manager[StickyNote]  # type: ignore
    User.objects: Manager[User]  # type: ignore


class Command(BaseCommand):
    """Export database contents to JSON file."""

    help = 'Export database contents to JSON file'

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            '--output',
            type=str,
            help='Output file path',
            default='database_export.json'
        )

    def handle(self, *args, **options):
        """Execute the command."""
        output_path = options['output']

        self.stdout.write('Exporting database to JSON...')

        data = {
            'export_date': datetime.now().isoformat(),
            'sticky_notes': [],
            'users': []
        }

        # Export sticky notes
        for note in StickyNote.objects.all():
            data['sticky_notes'].append({
                'id': note.id,
                'title': note.title,
                'content': note.content,
                'created_at': note.created_at.isoformat(),
                'updated_at': note.updated_at.isoformat()
            })

        # Export users (basic info only)
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
                    user.last_login.isoformat()
                    if user.last_login else None
                )
            })

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        notes_count = len(data['sticky_notes'])
        users_count = len(data['users'])

        self.stdout.write(
            f'✅ Export completed: {output_path}'
        )
        self.stdout.write(
            f'   - {notes_count} sticky notes exported'
        )
        self.stdout.write(
            f'   - {users_count} users exported'
        )
