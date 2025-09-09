
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSizePolicy
from PyQt6.QtGui import QIcon, QColor, QPalette, QPixmap, QPainter
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import Qt
from core.translations import translator
from services.settings_service import get_settings

class Sidebar(QWidget):
    def __init__(self, parent, pages=None):
        super().__init__(parent)
        self.parent = parent
        self.pages = pages or {}
        self.active_button = None

        self.setObjectName("Sidebar")
        self.setFixedWidth(210)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 20, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.logo_label)

        self.buttons = {}
        import functools
        self.svg_contents = {}
        for page_name, icon_path in self.pages.items():
            btn = QPushButton(f"  {translator.tr(page_name)}")
            btn.setCheckable(True)
            if icon_path:
                with open(icon_path, 'r') as f:
                    self.svg_contents[page_name] = f.read()
            btn.clicked.connect(functools.partial(self.set_active, page_name))
            self.layout.addWidget(btn)
            self.buttons[page_name] = btn

        self.layout.addStretch()

        if self.buttons:
            first_page = list(self.buttons.keys())[0]
            self.set_active(first_page)

        self.set_logo()
        translator.language_changed.connect(self.update_translations)

        # Initial icon color update
        settings = get_settings()
        theme = settings["theme"] if settings and "theme" in settings.keys() else "dark"
        self.update_icon_colors(theme)

    def set_button_icon(self, button, page_name, color):
        svg_content = self.svg_contents.get(page_name)
        if svg_content:
            renderer = QSvgRenderer(svg_content.encode('utf-8'))
            pixmap = QPixmap(renderer.defaultSize())
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            renderer.render(painter)
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
            painter.fillRect(pixmap.rect(), QColor(color))
            painter.end()
            button.setIcon(QIcon(pixmap))

    def update_icon_colors(self, theme):
        print(theme)
        from core.theme import get_accent_color_dark, get_accent_color_light
        if theme == "light":
            color = get_accent_color_light()
        else:
            color = get_accent_color_dark()

        for page_name, btn in self.buttons.items():
            self.set_button_icon(btn, page_name, color)

    def set_logo(self, logo_path=None):
        from PyQt6.QtGui import QPixmap
        import os
        if logo_path is None:
            try:
                from services.settings_service import get_logo_path
                logo_path = get_logo_path()
            except Exception:
                logo_path = None
        if not logo_path or not os.path.exists(logo_path):
            logo_path = os.path.join(os.path.dirname(__file__), '../assets/default_logo.png')
            print (logo_path)
        pixmap = QPixmap(logo_path)
        if not pixmap.isNull():
            self.logo_label.setPixmap(pixmap.scaledToHeight(64))
        else:
            self.logo_label.setText("HR Dashboard")

    def update_translations(self):
        for page_name, btn in self.buttons.items():
            btn.setText(f"  {translator.tr(page_name)}")

    def set_active(self, page_name, *args, **kwargs):
        if self.active_button:
            self.active_button.setChecked(False)
        btn = self.buttons[page_name]
        btn.setChecked(True)
        self.active_button = btn

        if self.parent and hasattr(self.parent, 'set_page'):
            self.parent.set_page(page_name)
