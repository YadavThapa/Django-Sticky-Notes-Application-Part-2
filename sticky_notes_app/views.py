"""Views for the sticky notes application."""
from django.contrib import messages
from django.db import DatabaseError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import TemplateDoesNotExist
from .forms import StickyNoteForm
from .models import StickyNote


def note_list(request):
    """Display all sticky notes"""
    try:
        notes = StickyNote.objects.all()
        print(f"DEBUG: Found {notes.count()} notes")  # Debug output

        context = {
            'notes': notes,
        }

        return render(request, 'sticky_notes/note_list.html', context)

    except DatabaseError as e:
        # Handle database errors
        print(f"Database error in note_list view: {e}")
        return HttpResponse(f"<h1>Database Error</h1><p>{e}</p>")

    except TemplateDoesNotExist as e:
        # Handle template-related errors
        print(f"Template error in note_list view: {e}")
        return HttpResponse(f"<h1>Template Error</h1><p>{e}</p>")

    except OSError as e:
        # Handle OS-related errors (file operations, etc.)
        print(f"OS error in note_list view: {e}")
        return HttpResponse(
            "<h1>System Error</h1><p>A system error occurred</p>"
        )

    except RuntimeError as e:
        # Handle runtime errors
        print(f"Runtime error in note_list view: {e}")
        return HttpResponse(
            "<h1>Application Error</h1>"
            "<p>An application error occurred</p>"
        )

    except (ValueError, TypeError) as e:
        # Handle value and type errors
        print(f"Unexpected error in note_list view: {e}")
        return HttpResponse(
            f"<h1>Unexpected Error</h1>"
            f"<p>Error: {e}</p>"
            f"<p>Type: {type(e).__name__}</p>"
        )


def note_detail(request, pk):
    """Display a single note"""
    note = get_object_or_404(StickyNote, pk=pk)
    return render(request, 'sticky_notes/note_detail.html', {'note': note})


def note_create(request):
    """Create a new note"""
    if request.method == 'POST':
        form = StickyNoteForm(request.POST)
        if form.is_valid():
            note = form.save()
            messages.success(request, 'Note created successfully!')
            return redirect('note_detail', pk=note.pk)
    else:
        form = StickyNoteForm()
    return render(request, 'sticky_notes/note_form.html', {
        'form': form,
        'title': 'Create New Note'
    })


def note_update(request, pk):
    """Update an existing note"""
    note = get_object_or_404(StickyNote, pk=pk)
    if request.method == 'POST':
        form = StickyNoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated successfully!')
            return redirect('note_detail', pk=note.pk)
    else:
        form = StickyNoteForm(instance=note)
    return render(request, 'sticky_notes/note_form.html', {
        'form': form,
        'note': note,
        'title': 'Edit Note'
    })


def note_delete(request, pk):
    """Delete a note"""
    note = get_object_or_404(StickyNote, pk=pk)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully!')
        return redirect('note_list')
    return render(
        request,
        'sticky_notes/note_confirm_delete.html',
        {'note': note}
    )
