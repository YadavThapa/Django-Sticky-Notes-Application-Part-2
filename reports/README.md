# Reports Directory Organization

This directory contains organized backup files and reports for the Sticky Notes Django application.

## Directory Structure

```
reports/
├── database_backups/           # All database backup files
│   ├── json_exports/          # Custom JSON format backups
│   ├── django_native/         # Django native dumpdata backups  
│   └── sqlite_files/          # Direct SQLite database file backups
├── html_reports/              # Generated HTML reports
├── archive/                   # Older/legacy backup files
└── README.md                  # This documentation file
```

## Backup Types

### 📊 JSON Exports (`database_backups/json_exports/`)
- **Format**: Clean, readable JSON
- **Contents**: Sticky notes + user data + timestamps
- **Use Case**: Easy data analysis and reading
- **Files**:
  - `my_database_backup.json` - Latest simple backup
  - `my_json_backup.json` - Custom JSON export
  - `comprehensive_database_backup_2025-10-04.json` - Full backup with metadata
  - `test_export.json` - Test backup

### ⚙️ Django Native (`database_backups/django_native/`)
- **Format**: Django fixture format
- **Contents**: Complete database dump
- **Use Case**: Full database restoration with `loaddata`
- **Files**:
  - `django_dumpdata.json` - Latest Django dump
  - `django_native_backup_2025-10-04.json` - Native backup
  - `database_backup_2025-10-04.json` - Standard backup

### 💾 SQLite Files (`database_backups/sqlite_files/`)
- **Format**: Direct SQLite database file
- **Contents**: Complete database with indexes
- **Use Case**: Direct database replacement
- **Files**:
  - `sqlite_database_backup_2025-10-04.sqlite3` - Database file backup

### 📄 HTML Reports (`html_reports/`)
- **Format**: HTML files
- **Contents**: Database analysis and reports
- **Use Case**: Visual data review
- **Files**:
  - `database_report.html` - Database analysis report
  - `test_report.html` - Test results report

### 📦 Archive (`archive/`)
- **Contents**: Older backup files and miscellaneous files
- **Purpose**: Keep old backups without cluttering main directories
- **Files**:
  - Legacy backup files
  - Development artifacts
  - Historical data

## Creating New Backups

### Quick JSON Backup:
```bash
python scripts/create_simple_backup.py
# Creates: database_backups/json_exports/my_database_backup.json
```

### Custom JSON Export:
```bash
python scripts/export_json.py reports/database_backups/json_exports/backup_name.json
```

### Django Native Backup:
```bash
python manage.py dumpdata --indent 2 -o reports/database_backups/django_native/backup_name.json
```

### SQLite File Backup:
```bash
copy db.sqlite3 reports/database_backups/sqlite_files/backup_name.sqlite3
```

## File Naming Convention

- **Date Format**: YYYY-MM-DD
- **Time Format**: HH-MM-SS (if needed)
- **Examples**:
  - `backup_2025-10-04.json`
  - `database_export_2025-10-04_14-30-15.json`
  - `sqlite_backup_2025-10-04.sqlite3`

## Maintenance

- **Weekly**: Move older files to archive
- **Monthly**: Clean up archive directory
- **Before major changes**: Create comprehensive backup in all formats

---
*Last Updated: October 4, 2025*
*Django Version: 5.2.6*