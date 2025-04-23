import sqlite3
import os
from datetime import datetime

class JournalDatabase:
    def __init__(self):
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Set the database path
        self.db_path = os.path.join(current_dir, 'journal_entries.db')
        self.initialize_db()
    
    def initialize_db(self):
        """Create the database and tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create table for journal entries
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_text TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL,
            therapy_analysis TEXT,
            mood_analysis TEXT,
            cbt_analysis TEXT,
            humanistic_analysis TEXT,
            psychodynamic_analysis TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_entry(self, entry_text, therapy_analysis, mood_analysis, cbt_analysis=None, humanistic_analysis=None, psychodynamic_analysis=None):
        """Save a new journal entry with its analyses"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
        INSERT INTO journal_entries (entry_text, created_at, therapy_analysis, mood_analysis, cbt_analysis, humanistic_analysis, psychodynamic_analysis)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (entry_text, created_at, therapy_analysis, mood_analysis, cbt_analysis, humanistic_analysis, psychodynamic_analysis))
        
        entry_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return entry_id
    
    def get_all_entries(self):
        """Get all journal entries ordered by date (newest first)"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # This enables column access by name
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, entry_text, created_at, therapy_analysis, mood_analysis, cbt_analysis, humanistic_analysis, psychodynamic_analysis
        FROM journal_entries
        ORDER BY created_at DESC
        ''')
        
        entries = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return entries
    
    def get_entry_by_id(self, entry_id):
        """Get a specific journal entry by ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, entry_text, created_at, therapy_analysis, mood_analysis, cbt_analysis, humanistic_analysis, psychodynamic_analysis
        FROM journal_entries
        WHERE id = ?
        ''', (entry_id,))
        
        entry = cursor.fetchone()
        
        conn.close()
        
        return dict(entry) if entry else None
        
    def clear_all_entries(self):
        """Delete all journal entries from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM journal_entries')
        
        conn.commit()
        conn.close()
