from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QFile, QTextStream
import os

def load_qss(app: QApplication, qss_file_path: str):
    """Loads a QSS file and applies it to the QApplication."""
    file = QFile(qss_file_path)
    if not file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        print(f"Warning: Could not open QSS file: {qss_file_path}")
        return
    
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())
    file.close()

def set_dark_theme(app: QApplication):
    app.setStyle("Fusion")
    load_qss(app, os.path.join(os.path.dirname(__file__), "modern_dark.qss"))

def set_light_theme(app: QApplication):
    app.setStyle("Fusion")
    load_qss(app, os.path.join(os.path.dirname(__file__), "modern_light.qss"))

def get_accent_color_dark():
    return "#169cf0" # Accent color from modern_dark.qss

def get_accent_color_light():
    return "#169cf0" # Accent color from modern_light.qss

