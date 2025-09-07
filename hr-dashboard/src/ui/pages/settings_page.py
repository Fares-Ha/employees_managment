from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from core.theme import set_dark_palette, set_light_palette
from PyQt6.QtWidgets import QApplication

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.theme_btn = QPushButton("Toggle Theme")
        self.logo_btn = QPushButton("Change Logo")
        self.layout.addWidget(self.theme_btn)
        self.layout.addWidget(self.logo_btn)

        self.theme_btn.clicked.connect(self.toggle_theme)
        self.logo_btn.clicked.connect(self.change_logo)
        self.is_dark = True

    def toggle_theme(self):
        app = QApplication.instance()
        if self.is_dark:
            set_light_palette(app)
            self.is_dark = False
        else:
            set_dark_palette(app)
            self.is_dark = True

    def change_logo(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Logo", "", "Images (*.png *.jpg *.bmp)")
        if file:
            print("Logo changed to:", file)
