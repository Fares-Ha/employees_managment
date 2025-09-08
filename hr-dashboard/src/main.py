import sys
from PyQt6.QtWidgets import QApplication
from core.database import init_db
from core.theme import set_dark_palette
from ui.main_window import HRDashboardWindow

if __name__ == "__main__":
    init_db()  # auto initialize DB on startup
    app = QApplication(sys.argv)
    # Load theme and palette from DB
    from services.settings_service import get_settings, load_custom_palette
    from core.theme import set_dark_palette, set_light_palette
    from PyQt6.QtGui import QPalette, QColor
    import os
    settings = get_settings()
    theme = settings["theme"] if settings and "theme" in settings.keys() else "dark"
    custom_palette = None
    pal_dict = load_custom_palette(theme)
    if pal_dict:
        pal = QPalette()
        for role_str, color_str in pal_dict.items():
            try:
                role = getattr(QPalette.ColorRole, role_str)
                pal.setColor(role, QColor(color_str))
            except Exception:
                pass
        custom_palette = pal
    if custom_palette:
        app.setPalette(custom_palette)
    else:
        if theme == "light":
            set_light_palette(app)
        else:
            set_dark_palette(app)
    # Load QSS for the theme
    qss_path = os.path.join(os.path.dirname(__file__), "core", "admintory_light_table.qss" if theme == "light" else "modern_dark.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    win = HRDashboardWindow()
    win.show()
    sys.exit(app.exec())
