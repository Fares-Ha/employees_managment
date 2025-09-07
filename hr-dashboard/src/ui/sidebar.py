from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSizePolicy
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

class Sidebar(QWidget):
    def __init__(self, parent, pages=None):
        super().__init__(parent)
        self.parent = parent
        self.pages = pages or {}
        self.active_button = None

        self.setFixedWidth(200)
        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
            }
            QPushButton {
                color: #ecf0f1;
                border: none;
                padding: 10px;
                text-align: left;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton:checked {
                background-color: #1abc9c;
            }
        """)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 20, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.buttons = {}
        for page_name, icon in self.pages.items():
            btn = QPushButton(f"  {page_name}")
            btn.setCheckable(True)
            if icon:
                btn.setIcon(icon)
            btn.clicked.connect(lambda checked, name=page_name: self.set_active(name))
            self.layout.addWidget(btn)
            self.buttons[page_name] = btn

        self.layout.addStretch()

        # Set first button as active by default
        if self.buttons:
            first_page = list(self.buttons.keys())[0]
            self.set_active(first_page)

    def set_active(self, page_name):
        if self.active_button:
            self.active_button.setChecked(False)
        btn = self.buttons[page_name]
        btn.setChecked(True)
        self.active_button = btn

        # Show the corresponding page
        if self.parent and hasattr(self.parent, 'set_page'):
            self.parent.set_page(page_name)
