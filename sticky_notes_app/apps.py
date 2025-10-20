"""Django app configuration for sticky_notes."""

from django.apps import AppConfig


class StickyNotesConfig(AppConfig):
    """Configuration for the sticky_notes Django app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sticky_notes_app'
