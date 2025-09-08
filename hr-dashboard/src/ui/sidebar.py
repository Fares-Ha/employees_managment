
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSizePolicy
from PyQt6.QtGui import QIcon, QColor, QPalette
from PyQt6.QtCore import Qt
from core.translations import translator

class Sidebar(QWidget):
    def __init__(self, parent, pages=None):
        super().__init__(parent)
        self.parent = parent
        self.pages = pages or {}
        self.active_button = None

        self.setObjectName("Sidebar")
        self.setFixedWidth(210)
        # Styling is now handled by global QSS only

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 20, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        # Add logo at top (image, runtime changeable)
        from PyQt6.QtGui import QPixmap
        import os
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    # self.logo_label.setStyleSheet("background: transparent; margin-bottom: 18px; border-radius: 12px;")
        self.layout.addWidget(self.logo_label)
        # Load logo from settings or default
        self.buttons = {}
        import functools
        for page_name, icon_path in self.pages.items():
            btn = QPushButton(f"  {translator.tr(page_name)}")
            btn.setCheckable(True)
            if icon_path:
                btn.setIcon(QIcon(icon_path))
            btn.clicked.connect(functools.partial(self.set_active, page_name))
            self.layout.addWidget(btn)
            self.buttons[page_name] = btn

        self.layout.addStretch()

        # Set first button as active by default
        if self.buttons:
            first_page = list(self.buttons.keys())[0]
            self.set_active(first_page)

        self.set_logo()
        translator.language_changed.connect(self.update_translations)
    def set_logo(self, logo_path=None):
        """Set the sidebar logo image. If logo_path is None, load from settings or default asset."""
        from PyQt6.QtGui import QPixmap
        import os
        if logo_path is None:
            # Try to load from settings, else use default
            try:
                from services.settings_service import get_logo_path
                logo_path = get_logo_path()
            except Exception:
                logo_path = None
        if not logo_path or not os.path.exists(logo_path):
            logo_path = os.path.join(os.path.dirname(__file__), '../assets/default_logo.png')
        pixmap = QPixmap(logo_path)
        if not pixmap.isNull():
            self.logo_label.setPixmap(pixmap.scaledToHeight(64))
        else:
            self.logo_label.setText("HR Dashboard")
            # self.logo_label.setStyleSheet("color: #ecf0f1; font-size: 18px; font-weight: bold;")
        # Do NOT recreate or add sidebar buttons here!

    def update_translations(self):
        # Update sidebar button text
        for page_name, btn in self.buttons.items():
            btn.setText(f"  {translator.tr(page_name)}")

    def set_active(self, page_name, *args, **kwargs):
        if self.active_button:
            self.active_button.setChecked(False)
        btn = self.buttons[page_name]
        btn.setChecked(True)
        self.active_button = btn

        # Show the corresponding page
        if self.parent and hasattr(self.parent, 'set_page'):
            self.parent.set_page(page_name)
