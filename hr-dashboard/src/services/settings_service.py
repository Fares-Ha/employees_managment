import json
def get_logo_path():
    row = get_settings()
    if row and 'logo_path' in row.keys() and row['logo_path']:
        return row['logo_path']
    return None
def update_language(language):
    conn = get_connection()
    c = conn.cursor()
    # Ensure the language column exists
    try:
        c.execute("ALTER TABLE settings ADD COLUMN language TEXT")
    except Exception:
        pass
    c.execute("UPDATE settings SET language=? WHERE id=1", (language,))
    conn.commit()
    conn.close()
from core.database import get_connection

def get_settings():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM settings WHERE id=1")
    row = c.fetchone()
    conn.close()
    return row

def save_custom_palette(mode, palette_dict):
    """Save a palette dict (role: #RRGGBB) for 'light' or 'dark' mode as JSON string."""
    conn = get_connection()
    c = conn.cursor()
    col = 'custom_palette_light' if mode == 'light' else 'custom_palette_dark'
    c.execute(f"UPDATE settings SET {col}=? WHERE id=1", (json.dumps(palette_dict),))
    conn.commit()
    conn.close()

def load_custom_palette(mode):
    """Load a palette dict (role: #RRGGBB) for 'light' or 'dark' mode from JSON string."""
    row = get_settings()
    col = 'custom_palette_light' if mode == 'light' else 'custom_palette_dark'
    if row and col in row.keys() and row[col]:
        try:
            return json.loads(row[col])
        except Exception:
            return None
    return None

def update_theme(theme_name):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE settings SET theme=? WHERE id=1", (theme_name,))
    conn.commit()
    conn.close()

def update_logo(logo_path):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE settings SET logo_path=? WHERE id=1", (logo_path,))
    conn.commit()
    conn.close()
