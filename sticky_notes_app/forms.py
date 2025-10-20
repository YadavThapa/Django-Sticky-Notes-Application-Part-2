"""Django forms for the sticky notes application."""
from django import forms
from .models import StickyNote


class StickyNoteForm(forms.ModelForm):
    """Form for creating and editing sticky notes."""

    class Meta:
        """Meta configuration for StickyNoteForm."""
        model = StickyNote
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter note title...",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Write your note content here...",
                }
            ),
        }
