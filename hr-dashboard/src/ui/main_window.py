from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QStyle
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from ui.pages.dashboard_page import DashboardPage
from ui.pages.employees_page import EmployeesPage
from ui.pages.analytics_page import AnalyticsPage
from ui.pages.settings_page import SettingsPage
from ui.sidebar import Sidebar
from services import settings_service
from widgets.animated_stacked_widget import AnimatedStackedWidget

class HRDashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HR Dashboard")
        self.resize(1200, 800)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top bar
        top_bar = QWidget()
        top_bar.setFixedHeight(50)
        top_bar.setStyleSheet("background-color: #34495e;")
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(10, 0, 10, 0)
        main_layout.addWidget(top_bar)

        self.logo_label = QLabel()
        self.logo_label.setStyleSheet("color: #ecf0f1; font-size: 18px; font-weight: bold;")
        top_bar_layout.addWidget(self.logo_label)
        top_bar_layout.addStretch()
        self.load_logo() # Load initial logo

        # Content area
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        main_layout.addWidget(content_widget)

        # Pages
        settings_page = SettingsPage()
        settings_page.logo_changed.connect(self.update_logo)

        self.pages = {
            "Dashboard": DashboardPage(),
            "Employees": EmployeesPage(),
            "Analytics": AnalyticsPage(),
            "Settings": settings_page
        }

        # Sidebar
        sidebar_icons = {
            "Dashboard": self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon),
            "Employees": self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon),
            "Analytics": self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay),
            "Settings": self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView)
        }
        self.sidebar = Sidebar(self, pages=sidebar_icons)
        content_layout.addWidget(self.sidebar)

        # Page stack
        self.stack = AnimatedStackedWidget()
        for page in self.pages.values():
            self.stack.addWidget(page)
        self.stack.setInitialIndex(0) # Set initial page without animation
        content_layout.addWidget(self.stack)

    def set_page(self, page_name):
        page = self.pages.get(page_name)
        if page:
            self.stack.setCurrentWidget(page)

    def load_logo(self):
        logo_path = settings_service.get_setting('logo_path')
        self.update_logo(logo_path)

    def update_logo(self, path):
        if path:
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                self.logo_label.setPixmap(pixmap.scaledToHeight(40, Qt.TransformationMode.SmoothTransformation))
            else:
                self.logo_label.setText("HR Dashboard (Logo not found)")
        else:
            self.logo_label.setText("HR Dashboard")
