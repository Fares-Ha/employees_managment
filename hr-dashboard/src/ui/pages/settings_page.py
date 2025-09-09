
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from core.theme import set_dark_theme, set_light_theme
from PyQt6.QtWidgets import QApplication
from core.translations import translator

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)


        from PyQt6.QtWidgets import QComboBox, QMessageBox, QHBoxLayout
        # Theme selector
        self.theme_box = QComboBox()
        self.theme_box.addItems([translator.tr("Light"), translator.tr("Dark")])
        self.theme_label = QLabel(translator.tr("Theme"))
        self.layout.addWidget(self.theme_label)
        self.layout.addWidget(self.theme_box)
        # Logo
        self.logo_label = QLabel(translator.tr("Logo"))
        self.layout.addWidget(self.logo_label)
        self.logo_btn = QPushButton(translator.tr("Change Logo"))
        self.layout.addWidget(self.logo_btn)
        # Language selection
        self.language_box = QComboBox()
        self.language_box.addItems([translator.tr("English"), translator.tr("Arabic")])
        self.language_box.currentIndexChanged.connect(self.change_language)
        self.language_label = QLabel(translator.tr("Language"))
        self.layout.addWidget(self.language_label)
        self.layout.addWidget(self.language_box)
        # Backup/Restore
        backup_layout = QHBoxLayout()
        self.backup_btn = QPushButton(translator.tr("Backup Data"))
        self.restore_btn = QPushButton(translator.tr("Restore Data"))
        self.backup_label = QLabel(translator.tr("Backup"))
        self.layout.addWidget(self.backup_label)
        backup_layout.addWidget(self.backup_btn)
        backup_layout.addWidget(self.restore_btn)
        self.layout.addLayout(backup_layout)
        # Connect signals
        self.theme_box.currentIndexChanged.connect(self.select_theme)
        self.logo_btn.clicked.connect(self.change_logo)
        self.backup_btn.clicked.connect(self.backup_data)
        self.restore_btn.clicked.connect(self.restore_data)
        # Load preferences
        from services.settings_service import get_settings, update_theme
        settings = get_settings()
        theme = settings["theme"] if settings and "theme" in settings.keys() else "dark"
        self.theme_box.setCurrentIndex(1 if theme == "dark" else 0)
        # if theme == "light":
        #     set_light_palette(QApplication.instance())
        # Language preference (default English)
        lang = settings["language"] if settings and "language" in settings.keys() and settings["language"] else "English"
        self.language_box.setCurrentText(lang)
        translator.set_language(lang)
        translator.language_changed.connect(self.update_translations)

    def update_translations(self):
        self.theme_label.setText(translator.tr("Theme"))
        self.theme_box.setItemText(0, translator.tr("Light"))
        self.theme_box.setItemText(1, translator.tr("Dark"))
        self.logo_btn.setText(translator.tr("Change Logo"))
        self.language_label.setText(translator.tr("Language"))
        self.backup_btn.setText(translator.tr("Backup Data"))
        self.restore_btn.setText(translator.tr("Restore Data"))
        # Update language combo box items
        self.language_box.setItemText(0, translator.tr("English"))
        self.language_box.setItemText(1, translator.tr("Arabic"))

    def change_language(self):
        lang = self.language_box.currentText()
        # Map translated language name back to English/Arabic
        if lang not in ("English", "Arabic"):
            if translator.get_language() == "Arabic" and lang == translator.tr("English"):
                lang = "English"
            elif translator.get_language() == "Arabic" and lang == translator.tr("Arabic"):
                lang = "Arabic"
        from services.settings_service import update_language
        update_language(lang)
        translator.set_language(lang)
        # from PyQt6.QtWidgets import QMessageBox
        # QMessageBox.information(self, translator.tr("Language Changed"), translator.tr("Language set to", lang=lang))

    def backup_data(self):
        import shutil, os
        from core.database import DB_PATH
        file, _ = QFileDialog.getSaveFileName(self, translator.tr("Backup Database"), "hr_dashboard_backup.db", translator.tr("DB Files (*.db)"))
        if file:
            shutil.copy2(DB_PATH, file)
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self, translator.tr("Backup Complete"), translator.tr("Database backed up to {file}", file=file))

    def restore_data(self):
        import shutil, os
        from core.database import DB_PATH
        file, _ = QFileDialog.getOpenFileName(self, translator.tr("Restore Database"), "", translator.tr("DB Files (*.db)"))
        if file:
            shutil.copy2(file, DB_PATH)
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self, translator.tr("Restore Complete"), translator.tr("Database restored from {file}. Please restart the app.", file=file))


    def select_theme(self):
        app = QApplication.instance()
        import os
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "core"))
        from services.settings_service import update_theme
        idx = self.theme_box.currentIndex()
        if idx == 0:
            # Light
            set_light_theme(app)
            update_theme("light")
            
        else:
            # Dark
            set_dark_theme(app)
            update_theme("dark")
            


    def change_logo(self):
        file, _ = QFileDialog.getOpenFileName(self, translator.tr("Select Logo"), "", translator.tr("Images (*.png *.jpg *.bmp)"))
        if file:
            from services.settings_service import update_logo
            update_logo(file)
            # Find sidebar and update logo
            main_window = self.window()
            if hasattr(main_window, 'sidebar_widget'):
                main_window.sidebar_widget.set_logo(file)
