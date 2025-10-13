"""Simple management command to view database contents."""

from typing import TYPE_CHECKING
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from sticky_notes.models import StickyNote

if TYPE_CHECKING:
    # This helps the type checker understand Django model managers
    from django.db.models import Manager
    StickyNote.objects: Manager[StickyNote]  # type: ignore
    User.objects: Manager[User]  # type: ignore


class Command(BaseCommand):
    """Command to display database contents in a readable format."""

    help = 'Display database contents in a readable format'

    def handle(self, *args, **options):
        """Execute the command."""
        self.stdout.write('\n' + '='*60)
        self.stdout.write('       STICKY NOTES DATABASE VIEWER')
        self.stdout.write('='*60 + '\n')

        self.display_notes()
        self.display_users()

        self.stdout.write('\n' + '='*60)

    def display_notes(self):
        """Display sticky notes in a readable format."""
        self.stdout.write('📝 STICKY NOTES')
        self.stdout.write('-' * 40)

        notes = StickyNote.objects.all().order_by('-updated_at')

        if not notes.exists():
            self.stdout.write('No sticky notes found in database.\n')
            return

        for i, note in enumerate(notes, 1):
            self.stdout.write(f'\n[{i}] ID: {note.id}')
            self.stdout.write(f'    Title: {note.title}')
            self.stdout.write(f'    Content: {note.content}')
            created = note.created_at.strftime("%Y-%m-%d %H:%M:%S")
            self.stdout.write(f'    Created: {created}')
            updated = note.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            self.stdout.write(f'    Updated: {updated}')

        total = notes.count()
        self.stdout.write(f'\nTotal sticky notes: {total}')

    def display_users(self):
        """Display users in a readable format."""
        self.stdout.write('\n👥 USERS')
        self.stdout.write('-' * 40)

        users = User.objects.all().order_by('username')

        if not users.exists():
            self.stdout.write('No users found in database.\n')
            return

        for i, user in enumerate(users, 1):
            self.stdout.write(f'\n[{i}] ID: {user.id}')
            self.stdout.write(f'    Username: {user.username}')
            self.stdout.write(f'    Email: {user.email}')
            self.stdout.write(f'    First Name: {user.first_name or "N/A"}')
            self.stdout.write(f'    Last Name: {user.last_name or "N/A"}')
            self.stdout.write(f'    Is Staff: {user.is_staff}')
            self.stdout.write(f'    Is Superuser: {user.is_superuser}')
            joined = user.date_joined.strftime("%Y-%m-%d %H:%M:%S")
            self.stdout.write(f'    Date Joined: {joined}')
            if user.last_login:
                last_login = user.last_login.strftime("%Y-%m-%d %H:%M:%S")
            else:
                last_login = "Never"
            self.stdout.write(f'    Last Login: {last_login}')

        total = users.count()
        self.stdout.write(f'\nTotal users: {total}')
