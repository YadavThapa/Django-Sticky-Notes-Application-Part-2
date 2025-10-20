#!/usr/bin/env python
"""
Code quality checker for the Sticky Notes application.
Checks for common Python and Django code quality issues.
"""

import os
import sys


def check_file_syntax(file_path):
    """Check if a Python file has valid syntax."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            compile(f.read(), file_path, 'exec')
        return True, "✅ Syntax OK"
    except SyntaxError as e:
        return False, f"❌ Syntax Error: {e}"
    except (IOError, UnicodeDecodeError) as e:
        return False, f"❌ Error: {e}"


def check_file_endings(file_path):
    """Check if file ends with newline."""
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            if content and not content.endswith(b'\n'):
                return False, "❌ Missing newline at end of file"
        return True, "✅ File ending OK"
    except IOError as e:
        return False, f"❌ Error reading file: {e}"


def main():
    """Main function to check code quality."""
    print("🔍 Sticky Notes Application - Code Quality Check\n")

    # List of Python files to check
    python_files = [
        'models.py',
        'views.py',
        'forms.py',
        'urls.py',
        'settings.py',
        'admin.py',
        'apps.py',
        'wsgi.py',
        'asgi.py',
        'tests.py',
        'manage.py'
    ]

    all_passed = True

    for file_name in python_files:
        if os.path.exists(file_name):
            print(f"Checking {file_name}:")

            # Check syntax
            syntax_ok, syntax_msg = check_file_syntax(file_name)
            print(f"  Syntax: {syntax_msg}")

            # Check file endings
            ending_ok, ending_msg = check_file_endings(file_name)
            print(f"  Format: {ending_msg}")

            if not (syntax_ok and ending_ok):
                all_passed = False

            print()
        else:
            print(f"⚠️  {file_name} not found, skipping...")

    # Overall result
    if all_passed:
        print("🎉 All checks passed! Code quality is excellent.")
        return 0
    else:
        print("⚠️  Some issues found. Please review the results above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
