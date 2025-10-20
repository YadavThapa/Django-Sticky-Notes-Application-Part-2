"""Export database to readable HTML format."""

from datetime import datetime
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
    """Export database contents to HTML file."""

    help = 'Export database contents to HTML file'

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            '--output',
            type=str,
            help='Output HTML file path',
            default='database_report.html'
        )

    def handle(self, *args, **options):
        """Execute the command."""
        output_path = options['output']

        self.stdout.write('Generating HTML database report...')

        html_content = self.generate_html()

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        notes_count = StickyNote.objects.count()
        users_count = User.objects.count()

        self.stdout.write(f'✅ HTML report generated: {output_path}')
        self.stdout.write(f'   - {notes_count} sticky notes')
        self.stdout.write(f'   - {users_count} users')

    def generate_html(self):
        """Generate HTML content."""
        export_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sticky Notes Database Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 40px;
            margin-bottom: 20px;
        }}
        .export-info {{
            background: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 30px;
            text-align: center;
        }}
        .note {{
            background: #fff9c4;
            border-left: 5px solid #f1c40f;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
        }}
        .note-title {{
            font-weight: bold;
            color: #2c3e50;
            font-size: 1.2em;
            margin-bottom: 10px;
        }}
        .note-content {{
            margin-bottom: 10px;
            white-space: pre-wrap;
        }}
        .note-meta {{
            font-size: 0.9em;
            color: #7f8c8d;
            border-top: 1px solid #ecf0f1;
            padding-top: 10px;
        }}
        .user {{
            background: #e8f6f3;
            border-left: 5px solid #27ae60;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
        }}
        .user-name {{
            font-weight: bold;
            color: #2c3e50;
            font-size: 1.1em;
            margin-bottom: 10px;
        }}
        .user-details {{
            font-size: 0.9em;
            color: #34495e;
        }}
        .stats {{
            display: flex;
            justify-content: space-around;
            margin: 30px 0;
        }}
        .stat-box {{
            background: #3498db;
            color: white;
            padding: 20px;
            border-radius: 5px;
            text-align: center;
            min-width: 150px;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
        }}
        .no-data {{
            text-align: center;
            color: #7f8c8d;
            font-style: italic;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📝 Sticky Notes Database Report</h1>

        <div class="export-info">
            <strong>Report Generated:</strong> {export_date}
        </div>

        <div class="stats">
            <div class="stat-box">
                <div class="stat-number">{StickyNote.objects.count()}</div>
                <div>Sticky Notes</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{User.objects.count()}</div>
                <div>Users</div>
            </div>
        </div>"""

        # Add sticky notes section
        html += '<h2>📝 Sticky Notes</h2>'
        notes = StickyNote.objects.all().order_by('-updated_at')

        if notes.exists():
            for note in notes:
                created = note.created_at.strftime('%Y-%m-%d %H:%M:%S')
                updated = note.updated_at.strftime('%Y-%m-%d %H:%M:%S')

                html += f"""
        <div class="note">
            <div class="note-title">{self.escape_html(note.title)}</div>
            <div class="note-content">{self.escape_html(note.content)}</div>
            <div class="note-meta">
                <strong>ID:</strong> {note.id} |
                <strong>Created:</strong> {created} |
                <strong>Updated:</strong> {updated}
            </div>
        </div>"""
        else:
            html += '<div class="no-data">No sticky notes found.</div>'

        # Add users section
        html += '<h2>👥 Users</h2>'
        users = User.objects.all().order_by('username')

        if users.exists():
            for user in users:
                joined = user.date_joined.strftime('%Y-%m-%d %H:%M:%S')
                last_login = (
                    user.last_login.strftime('%Y-%m-%d %H:%M:%S')
                    if user.last_login else 'Never'
                )

                html += f"""
        <div class="user">
            <div class="user-name">{self.escape_html(user.username)}</div>
            <div class="user-details">
                <strong>Email:</strong> {self.escape_html(user.email)}<br>
                <strong>Name:</strong> {self.escape_html(user.first_name)} \
{self.escape_html(user.last_name)}<br>
                <strong>Staff:</strong> {'Yes' if user.is_staff else 'No'} |
                <strong>Superuser:</strong> \
{'Yes' if user.is_superuser else 'No'}
                <br>
                <strong>Joined:</strong> {joined} |
                <strong>Last Login:</strong> {last_login}
            </div>
        </div>"""
        else:
            html += '<div class="no-data">No users found.</div>'

        html += """
    </div>
</body>
</html>"""

        return html

    def escape_html(self, text):
        """Escape HTML special characters."""
        if not text:
            return 'N/A'
        return (str(text)
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#x27;'))
