import sys
from PyQt6.QtWidgets import QApplication
from core.database import init_db
from core.theme import set_dark_theme, set_light_theme
# import icons_rc # Import the generated resource file
from ui.main_window import HRDashboardWindow

if __name__ == "__main__":
    init_db()  # auto initialize DB on startup
    app = QApplication(sys.argv)
    # Load theme from DB
    from services.settings_service import get_settings
    settings = get_settings()
    theme = settings["theme"] if settings and "theme" in settings.keys() else "dark"

    if theme == "light":
        set_light_theme(app)
    else:
        set_dark_theme(app)

    win = HRDashboardWindow()
    win.show()
    sys.exit(app.exec())
