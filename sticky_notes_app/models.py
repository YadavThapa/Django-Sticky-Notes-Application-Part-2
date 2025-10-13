"""Django models for the sticky_notes app."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db import models as django_models
    from django.urls import reverse as django_reverse
    from django.utils import timezone as django_timezone
else:
    from django.db import models as django_models
    from django.urls import reverse as django_reverse
    from django.utils import timezone as django_timezone


class StickyNote(django_models.Model):
    """Model representing a sticky note with title and content."""

    objects = django_models.Manager()  # type: ignore
    title = django_models.CharField(max_length=200)  # type: ignore
    content = django_models.TextField()  # type: ignore
    created_at = django_models.DateTimeField(  # type: ignore
        default=django_timezone.now
    )
    updated_at = django_models.DateTimeField(auto_now=True)  # type: ignore

    class Meta:
        """Meta configuration for StickyNote model."""
        app_label = 'sticky_notes_app'
        db_table = 'sticky_notes_stickynote'
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        """Return string representation of the sticky note."""
        return str(self.title)

    def get_absolute_url(self) -> str:
        """Return the absolute URL for this sticky note."""
        return django_reverse("note_detail", kwargs={"pk": self.pk})
