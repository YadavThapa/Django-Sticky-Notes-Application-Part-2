#!/usr/bin/env python
"""Clean up whitespace and formatting issues in Python files."""

import os


def clean_python_file(file_path):
    """Clean whitespace issues in a Python file."""
    if not os.path.exists(file_path):
        return False, "File not found"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        lines = content.split('\n')
        cleaned_lines = [line.rstrip() for line in lines]

        while cleaned_lines and cleaned_lines[-1] == '':
            cleaned_lines.pop()

        cleaned_content = '\n'.join(cleaned_lines) + '\n'

        if cleaned_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            return True, "Cleaned"
        else:
            return True, "Already clean"

    except (OSError, IOError, UnicodeDecodeError):
        return False, "Error processing file"


def main():
    """Clean all Python files in the project."""
    python_files = [
        'scripts/create_database_backup.py',
        'scripts/create_simple_backup.py',
        'scripts/export_json.py',
        'scripts/quality_check.py',
        'sticky_notes_app/models.py',
        'sticky_notes_app/views.py',
        'sticky_notes_app/forms.py',
        'sticky_notes_app/admin.py',
        'sticky_notes_app/apps.py',
        'sticky_notes_app/tests.py',
        'sticky_notes_config/settings.py',
        'sticky_notes_config/urls.py',
        'sticky_notes_config/wsgi.py',
        'sticky_notes_config/asgi.py',
        'manage.py'
    ]

    print("🧹 Cleaning Python files...\n")

    cleaned_count = 0
    error_count = 0

    for file_path in python_files:
        success, message = clean_python_file(file_path)
        if success:
            if message == "Cleaned":
                print(f"✅ {file_path}: {message}")
                cleaned_count += 1
            else:
                print(f"✓ {file_path}: {message}")
        else:
            print(f"❌ {file_path}: {message}")
            error_count += 1

    print("\n📊 Summary:")
    print(f"   🧹 Files cleaned: {cleaned_count}")
    already_clean = len(python_files) - cleaned_count - error_count
    print(f"   ✓ Already clean: {already_clean}")
    print(f"   ❌ Errors: {error_count}")

    if cleaned_count > 0:
        print(f"\n🎉 Successfully cleaned {cleaned_count} files!")
    else:
        print("\n✨ All files were already clean!")


if __name__ == '__main__':
    main()
