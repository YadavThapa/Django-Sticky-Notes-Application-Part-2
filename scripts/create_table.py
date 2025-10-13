"""Script to create the sticky notes database table."""
import os
import sqlite3

# Change to the project directory
os.chdir(r'c:\Users\hemja\OneDrive\Desktop\sticky_note_new')

# Connect to the database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Create the table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sticky_notes_stickynote (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(200) NOT NULL,
        content TEXT NOT NULL,
        created_at DATETIME NOT NULL DEFAULT (datetime('now')),
        updated_at DATETIME NOT NULL DEFAULT (datetime('now'))
    )
''')

conn.commit()
conn.close()
print("Database table created successfully!")