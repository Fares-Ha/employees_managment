import sys
from PyQt6.QtWidgets import QApplication
from core.database import init_db
from core.theme import set_dark_palette
from ui.main_window import HRDashboardWindow

if __name__ == "__main__":
    init_db()  # auto initialize DB on startup
    app = QApplication(sys.argv)
    set_dark_palette(app)
    win = HRDashboardWindow()
    win.show()
    sys.exit(app.exec())
