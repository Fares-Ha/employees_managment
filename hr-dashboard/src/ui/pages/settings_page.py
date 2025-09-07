from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                             QComboBox, QFileDialog, QFormLayout)
from PyQt6.QtCore import pyqtSignal, Qt
from services import settings_service
from core.theme import set_dark_palette, set_light_palette
from PyQt6.QtWidgets import QApplication

class SettingsPage(QWidget):
    logo_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        form_layout = QFormLayout()
        form_layout.setSpacing(20)
        self.layout.addLayout(form_layout)

        # Theme selection
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        current_theme = settings_service.get_setting('theme')
        if current_theme == 'light':
            self.theme_combo.setCurrentIndex(1)
        else:
            self.theme_combo.setCurrentIndex(0)
        self.theme_combo.currentIndexChanged.connect(self.on_theme_changed)
        form_layout.addRow(QLabel("Theme:"), self.theme_combo)

        # Logo selection
        self.logo_button = QPushButton("Select Logo File")
        self.logo_button.clicked.connect(self.on_change_logo)

        self.logo_path_label = QLabel(settings_service.get_setting('logo_path') or "No logo selected")

        logo_layout = QHBoxLayout()
        logo_layout.addWidget(self.logo_path_label)
        logo_layout.addWidget(self.logo_button)
        form_layout.addRow(QLabel("Application Logo:"), logo_layout)

    def on_theme_changed(self, index):
        theme = self.theme_combo.currentText().lower()
        settings_service.set_setting('theme', theme)

        app = QApplication.instance()
        if theme == 'light':
            set_light_palette(app)
        else:
            set_dark_palette(app)

    def on_change_logo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Logo", "", "Images (*.png *.jpg *.bmp)")
        if file_path:
            settings_service.set_setting('logo_path', file_path)
            self.logo_path_label.setText(file_path)
            self.logo_changed.emit(file_path)
