from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class KPICard(QWidget):
    def __init__(self, title: str, value: str, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 100)
        self.setStyleSheet("""
            QWidget {
                background-color: #34495e;
                border-radius: 5px;
            }
        """)

        layout = QVBoxLayout(self)

        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("color: #ecf0f1; font-size: 14px;")
        layout.addWidget(self.title_label)

        self.value_label = QLabel(value)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_label.setStyleSheet("color: #ecf0f1; font-size: 24px; font-weight: bold;")
        layout.addWidget(self.value_label)
