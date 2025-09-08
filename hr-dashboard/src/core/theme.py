from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication

def set_dark_palette(app: QApplication):
    app.setStyle("Fusion")
    pal = QPalette()
    pal.setColor(QPalette.ColorRole.Window, QColor(30, 32, 35))
    pal.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    pal.setColor(QPalette.ColorRole.Base, QColor(22, 24, 27))
    pal.setColor(QPalette.ColorRole.AlternateBase, QColor(40, 43, 48))
    pal.setColor(QPalette.ColorRole.ToolTipBase, QColor(30, 32, 35))
    pal.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
    pal.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
    pal.setColor(QPalette.ColorRole.Button, QColor(40, 43, 48))
    pal.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    pal.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
    pal.setColor(QPalette.ColorRole.Highlight, QColor(80, 140, 255))
    pal.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    app.setPalette(pal)

def set_light_palette(app: QApplication):
    app.setStyle("Fusion")
    pal = QPalette()
    pal.setColor(QPalette.ColorRole.Window, QColor(250, 250, 250))
    pal.setColor(QPalette.ColorRole.WindowText, QColor(20, 20, 20))
    pal.setColor(QPalette.ColorRole.Base, QColor(245, 245, 245))
    pal.setColor(QPalette.ColorRole.Button, QColor(235, 235, 235))
    pal.setColor(QPalette.ColorRole.ButtonText, QColor(20, 20, 20))
    pal.setColor(QPalette.ColorRole.Highlight, QColor(30, 120, 240))
    pal.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    app.setPalette(pal)
