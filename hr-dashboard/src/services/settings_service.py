from core.database import get_connection

def get_settings():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM settings WHERE id=1")
    row = c.fetchone()
    conn.close()
    return row

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
