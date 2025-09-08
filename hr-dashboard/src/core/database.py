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
        salary REAL,
        position TEXT
    )
    """)
    # Add position column if it does not exist (safe migration)
    try:
        c.execute("ALTER TABLE staff ADD COLUMN position TEXT")
    except Exception:
        pass
    # Settings table for theme, logo, etc.
    c.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY,
        theme TEXT DEFAULT 'dark',
        logo_path TEXT
    )
    """)
    # Add new columns if they do not exist (safe migration)
    try:
        c.execute("ALTER TABLE settings ADD COLUMN custom_palette_light TEXT")
    except Exception:
        pass
    try:
        c.execute("ALTER TABLE settings ADD COLUMN custom_palette_dark TEXT")
    except Exception:
        pass
    # Ensure a default row exists
    c.execute("INSERT OR IGNORE INTO settings (id, theme, logo_path) VALUES (1, 'dark', NULL)")
    conn.commit()
    conn.close()