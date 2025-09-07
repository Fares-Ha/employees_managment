from core.database import get_connection

def get_setting(key):
    """
    Retrieves a setting from the database.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key=?", (key,))
    row = c.fetchone()
    conn.close()
    return row['value'] if row else None

def set_setting(key, value):
    """
    Updates a setting in the database.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE settings SET value=? WHERE key=?", (value, key))
    conn.commit()
    conn.close()

def get_all_settings():
    """
    Retrieves all settings from the database as a dictionary.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT key, value FROM settings")
    rows = c.fetchall()
    conn.close()
    return {row['key']: row['value'] for row in rows}
