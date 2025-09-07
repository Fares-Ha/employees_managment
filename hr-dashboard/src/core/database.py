import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "hr_dashboard.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create staff table
    c.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        dob TEXT,
        emirates_id TEXT,
        passport_number TEXT,
        emirates_id_front TEXT,
        emirates_id_back TEXT,
        passport_img TEXT,
        salary REAL
    )
    """)

    # Create settings table
    c.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    # Insert default settings if they don't exist
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ('theme', 'dark'))
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ('logo_path', ''))

    conn.commit()
    conn.close()