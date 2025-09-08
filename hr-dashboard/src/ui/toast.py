from PyQt6.QtWidgets import QLabel, QVBoxLayout, QDialog, QHBoxLayout, QApplication
from PyQt6.QtCore import Qt, QTimer

class Toast(QDialog):
    def __init__(self, message, parent=None, duration=2000):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setModal(False)
        self.setFixedSize(320, 50)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)
        label = QLabel(message)
        label.setStyleSheet("color: white; font-size: 16px; font-weight: 500;")
        layout.addWidget(label)
        self.setStyleSheet("background: rgba(40,40,40,0.92); border-radius: 12px;")
        QTimer.singleShot(duration, self.close)

    def showEvent(self, event):
        super().showEvent(event)
        # Center at bottom of parent or screen
        parent = self.parentWidget() or QApplication.activeWindow()
        if parent:
            geo = parent.geometry()
            x = geo.x() + (geo.width() - self.width()) // 2
            y = geo.y() + geo.height() - self.height() - 40
            self.move(x, y)
        else:
            screen = QApplication.primaryScreen().geometry()
            x = (screen.width() - self.width()) // 2
            y = screen.height() - self.height() - 40
            self.move(x, y)
