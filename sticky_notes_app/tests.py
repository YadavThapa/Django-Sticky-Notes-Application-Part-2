"""
Comprehensive test suite for the Sticky Notes application.

This module contains unit tests for models, views, forms, and URLs
to ensure the sticky notes application works correctly.
"""

from typing import TYPE_CHECKING
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.messages import get_messages
from django.core.exceptions import ValidationError
from .models import StickyNote
from .forms import StickyNoteForm

if TYPE_CHECKING:
    # This helps the type checker understand Django model managers
    from django.db.models import Manager
    StickyNote.objects: Manager[StickyNote]  # type: ignore


class StickyNoteModelTests(TestCase):
    """Test cases for the StickyNote model."""

    def setUp(self):
        """Set up test data."""
        self.note = StickyNote.objects.create(
            title="Test Note",
            content="This is a test note content."
        )

    def test_string_representation(self):
        """Test that the model's string representation is the title."""
        self.assertEqual(str(self.note), "Test Note")

    def test_get_absolute_url(self):
        """Test that get_absolute_url returns the correct URL."""
        expected_url = reverse('note_detail', kwargs={'pk': self.note.pk})
        self.assertEqual(self.note.get_absolute_url(), expected_url)

    def test_note_creation_with_timestamps(self):
        """Test that notes are created with correct timestamps."""
        note = StickyNote.objects.create(
            title="Time Test Note",
            content="Testing timestamps"
        )
        self.assertIsNotNone(note.created_at)
        self.assertIsNotNone(note.updated_at)
        self.assertTrue(note.created_at <= timezone.now())
        self.assertTrue(note.updated_at <= timezone.now())

    def test_note_ordering(self):
        """Test that notes are ordered by updated_at in descending order."""
        # Clear existing notes from setUp
        StickyNote.objects.all().delete()

        # Create multiple notes
        note1 = StickyNote.objects.create(title="Note 1", content="Content 1")
        StickyNote.objects.create(title="Note 2", content="Content 2")
        StickyNote.objects.create(title="Note 3", content="Content 3")

        # Update note1 to make it the most recently updated
        note1.content = "Updated content"
        note1.save()

        notes = StickyNote.objects.all()
        self.assertEqual(notes[0], note1)  # Most recently updated first

    def test_note_title_max_length(self):
        """Test that note title respects max_length constraint."""
        long_title = "x" * 201  # Exceeds max_length of 200
        note = StickyNote(title=long_title, content="Test content")

        with self.assertRaises(ValidationError):
            note.full_clean()

    def test_note_content_can_be_long(self):
        """Test that note content can be very long (TextField)."""
        long_content = "x" * 5000  # Very long content
        note = StickyNote.objects.create(
            title="Long Content Note",
            content=long_content
        )
        self.assertEqual(len(note.content), 5000)

    def test_note_fields_required(self):
        """Test that required fields are properly validated."""
        # Test empty title
        note = StickyNote(title="", content="Test content")
        with self.assertRaises(ValidationError):
            note.full_clean()

        # Test empty content
        note = StickyNote(title="Test title", content="")
        with self.assertRaises(ValidationError):
            note.full_clean()


class StickyNoteFormTests(TestCase):
    """Test cases for the StickyNoteForm."""

    def test_form_with_valid_data(self):
        """Test form with valid data."""
        form_data = {
            'title': 'Test Note',
            'content': 'This is test content.'
        }
        form = StickyNoteForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_with_empty_title(self):
        """Test form with empty title."""
        form_data = {
            'title': '',
            'content': 'This is test content.'
        }
        form = StickyNoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_form_with_empty_content(self):
        """Test form with empty content."""
        form_data = {
            'title': 'Test Note',
            'content': ''
        }
        form = StickyNoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_form_save(self):
        """Test that form saves data correctly."""
        form_data = {
            'title': 'Form Test Note',
            'content': 'This note was created via form.'
        }
        form = StickyNoteForm(data=form_data)
        self.assertTrue(form.is_valid())

        note = form.save()
        self.assertEqual(note.title, 'Form Test Note')
        self.assertEqual(note.content, 'This note was created via form.')

    def test_form_widgets(self):
        """Test that form widgets have correct CSS classes."""
        form = StickyNoteForm()

        # Check title widget
        title_widget = form.fields['title'].widget
        self.assertIn('form-control', title_widget.attrs['class'])
        self.assertIn('Enter note title...', title_widget.attrs['placeholder'])

        # Check content widget
        content_widget = form.fields['content'].widget
        self.assertIn('form-control', content_widget.attrs['class'])
        self.assertEqual(content_widget.attrs['rows'], 6)
        self.assertIn('Write your note content here...',
                      content_widget.attrs['placeholder'])


class StickyNoteViewTests(TestCase):
    """Test cases for the sticky note views."""

    def setUp(self):
        """Set up test data and client."""
        self.client = Client()
        self.note = StickyNote.objects.create(
            title="Test Note",
            content="This is a test note."
        )

    def test_note_list_view(self):
        """Test the note list view."""
        url = reverse('note_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note")
        self.assertContains(response, self.note.content)
        self.assertIn('notes', response.context)

    def test_note_list_view_with_multiple_notes(self):
        """Test note list view with multiple notes."""
        # Create additional notes
        StickyNote.objects.create(title="Note 2", content="Content 2")
        StickyNote.objects.create(title="Note 3", content="Content 3")

        url = reverse('note_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['notes']), 3)

    def test_note_detail_view(self):
        """Test the note detail view."""
        url = reverse('note_detail', kwargs={'pk': self.note.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.note.title)
        self.assertContains(response, self.note.content)
        self.assertEqual(response.context['note'], self.note)

    def test_note_detail_view_404(self):
        """Test note detail view with non-existent note."""
        url = reverse('note_detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_note_create_view_get(self):
        """Test GET request to note create view."""
        url = reverse('note_create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create New Note")
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], StickyNoteForm)

    def test_note_create_view_post_valid(self):
        """Test POST request to note create view with valid data."""
        url = reverse('note_create')
        data = {
            'title': 'New Note',
            'content': 'This is a new note created via POST.'
        }
        response = self.client.post(url, data)

        # Should redirect to detail view
        note = StickyNote.objects.get(title='New Note')
        detail_url = reverse('note_detail', kwargs={'pk': note.pk})
        self.assertRedirects(response, detail_url)

        # Check that note was created
        self.assertEqual(StickyNote.objects.count(), 2)  # Original + new
        self.assertEqual(note.content, 'This is a new note created via POST.')

    def test_note_create_view_post_invalid(self):
        """Test POST request to note create view with invalid data."""
        url = reverse('note_create')
        data = {
            'title': '',  # Empty title should be invalid
            'content': 'This note has no title.'
        }
        response = self.client.post(url, data)

        # Should stay on create page
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create New Note")

        # Should not create note
        self.assertEqual(StickyNote.objects.count(), 1)  # Only original note

    def test_note_update_view_get(self):
        """Test GET request to note update view."""
        url = reverse('note_update', kwargs={'pk': self.note.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Note")
        self.assertIn('form', response.context)
        self.assertIn('note', response.context)
        self.assertEqual(response.context['note'], self.note)

    def test_note_update_view_post_valid(self):
        """Test POST request to note update view with valid data."""
        url = reverse('note_update', kwargs={'pk': self.note.pk})
        data = {
            'title': 'Updated Note Title',
            'content': 'This note has been updated.'
        }
        response = self.client.post(url, data)

        # Should redirect to detail view
        self.assertRedirects(
            response, reverse('note_detail', kwargs={'pk': self.note.pk}))

        # Check that note was updated
        updated_note = StickyNote.objects.get(pk=self.note.pk)
        self.assertEqual(updated_note.title, 'Updated Note Title')
        self.assertEqual(updated_note.content, 'This note has been updated.')

    def test_note_update_view_404(self):
        """Test note update view with non-existent note."""
        url = reverse('note_update', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_note_delete_view_get(self):
        """Test GET request to note delete view."""
        url = reverse('note_delete', kwargs={'pk': self.note.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.note.title)
        self.assertIn('note', response.context)
        self.assertEqual(response.context['note'], self.note)

    def test_note_delete_view_post(self):
        """Test POST request to note delete view."""
        url = reverse('note_delete', kwargs={'pk': self.note.pk})
        response = self.client.post(url)

        # Should redirect to list view
        self.assertRedirects(response, reverse('note_list'))

        # Check that note was deleted
        self.assertEqual(StickyNote.objects.count(), 0)

    def test_note_delete_view_404(self):
        """Test note delete view with non-existent note."""
        url = reverse('note_delete', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_success_messages(self):
        """Test that success messages are displayed."""
        # Test create success message
        url = reverse('note_create')
        data = {
            'title': 'Message Test Note',
            'content': 'Testing success messages.'
        }
        response = self.client.post(url, data, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Note created successfully!')

        # Test update success message
        note = StickyNote.objects.get(title='Message Test Note')
        url = reverse('note_update', kwargs={'pk': note.pk})
        data = {
            'title': 'Updated Message Test Note',
            'content': 'Updated content for testing messages.'
        }
        response = self.client.post(url, data, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Note updated successfully!')

        # Test delete success message
        url = reverse('note_delete', kwargs={'pk': note.pk})
        response = self.client.post(url, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Note deleted successfully!')


class StickyNoteURLTests(TestCase):
    """Test cases for URL patterns."""

    def setUp(self):
        """Set up test data."""
        self.note = StickyNote.objects.create(
            title="URL Test Note",
            content="Testing URL patterns."
        )

    def test_note_list_url(self):
        """Test note list URL pattern."""
        url = reverse('note_list')
        self.assertEqual(url, '/')

    def test_note_detail_url(self):
        """Test note detail URL pattern."""
        url = reverse('note_detail', kwargs={'pk': self.note.pk})
        self.assertEqual(url, f'/note/{self.note.pk}/')

    def test_note_create_url(self):
        """Test note create URL pattern."""
        url = reverse('note_create')
        self.assertEqual(url, '/create/')

    def test_note_update_url(self):
        """Test note update URL pattern."""
        url = reverse('note_update', kwargs={'pk': self.note.pk})
        self.assertEqual(url, f'/note/{self.note.pk}/edit/')

    def test_note_delete_url(self):
        """Test note delete URL pattern."""
        url = reverse('note_delete', kwargs={'pk': self.note.pk})
        self.assertEqual(url, f'/note/{self.note.pk}/delete/')


class StickyNoteIntegrationTests(TestCase):
    """Integration tests for the sticky notes application."""

    def setUp(self):
        """Set up test client."""
        self.client = Client()

    def test_complete_note_lifecycle(self):
        """Test complete lifecycle: create, read, update, delete."""
        # 1. Create a note
        create_url = reverse('note_create')
        create_data = {
            'title': 'Integration Test Note',
            'content': 'This note tests the complete lifecycle.'
        }
        response = self.client.post(create_url, create_data)

        # Should redirect to detail view
        note = StickyNote.objects.get(title='Integration Test Note')
        self.assertRedirects(
            response, reverse('note_detail', kwargs={'pk': note.pk}))

        # 2. Read the note
        detail_url = reverse('note_detail', kwargs={'pk': note.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Integration Test Note')

        # 3. Update the note
        update_url = reverse('note_update', kwargs={'pk': note.pk})
        update_data = {
            'title': 'Updated Integration Test Note',
            'content': 'This note has been updated during integration testing.'
        }
        response = self.client.post(update_url, update_data)
        self.assertRedirects(
            response, reverse('note_detail', kwargs={'pk': note.pk}))

        # Verify update
        updated_note = StickyNote.objects.get(pk=note.pk)
        self.assertEqual(updated_note.title, 'Updated Integration Test Note')

        # 4. Delete the note
        delete_url = reverse('note_delete', kwargs={'pk': note.pk})
        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse('note_list'))

        # Verify deletion
        self.assertEqual(StickyNote.objects.filter(pk=note.pk).count(), 0)

    def test_navigation_flow(self):
        """Test navigation between different views."""
        # Start at list view
        list_url = reverse('note_list')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, 200)

        # Navigate to create view
        create_url = reverse('note_create')
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 200)

        # Create a note and check redirect
        create_data = {
            'title': 'Navigation Test Note',
            'content': 'Testing navigation flow.'
        }
        response = self.client.post(create_url, create_data)
        note = StickyNote.objects.get(title='Navigation Test Note')
        self.assertRedirects(
            response, reverse('note_detail', kwargs={'pk': note.pk}))

        # From detail, navigate to edit
        update_url = reverse('note_update', kwargs={'pk': note.pk})
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 200)

    def test_error_handling(self):
        """Test error handling for edge cases."""
        # Test accessing non-existent note
        response = self.client.get(reverse('note_detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse('note_update', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse('note_delete', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)
