from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QPixmap, QPainter, QColor
from PyQt6.QtCore import Qt

class KpiBox(QWidget):
    def __init__(self, title, value, icon_path, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 120)
        self.setObjectName("KpiBox")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        self.icon_label = QLabel()
        self.icon_label.setFixedSize(32, 32)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.icon_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("Title")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        self.value_label = QLabel(str(value))
        self.value_label.setObjectName("Value")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.value_label)

        self.svg_renderer = QSvgRenderer(icon_path)
        self.set_icon_color("#000000")  # Default color

    def set_value(self, value):
        self.value_label.setText(str(value))

    def set_icon_color(self, color):
        pixmap = QPixmap(self.svg_renderer.defaultSize())
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        self.svg_renderer.render(painter)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), QColor(color))
        painter.end()
        self.icon_label.setPixmap(pixmap)