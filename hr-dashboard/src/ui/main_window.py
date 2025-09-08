from PyQt6.QtWidgets import (
    QMainWindow, QStackedWidget, QDockWidget, QWidget
)
from PyQt6.QtCore import Qt
from ui.pages.dashboard_page import DashboardPage
from ui.pages.employees_page import EmployeesPage
from ui.sidebar import Sidebar

class HRDashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HR Dashboard")
        self.resize(1200, 800)

        # Pages
        from ui.pages.settings_page import SettingsPage

        self.pages = {
            "Dashboard": DashboardPage(),
            "Employees": EmployeesPage(),
            "Settings": SettingsPage()
        }

        # Connect staff_changed signal to refresh dashboard
        employees_page = self.pages["Employees"]
        dashboard_page = self.pages["Dashboard"]
        employees_page.staff_changed.connect(dashboard_page.refresh_dashboard)

        self.stack = QStackedWidget()
        for page in self.pages.values():
            self.stack.addWidget(page)
        self.setCentralWidget(self.stack)

        # Sidebar
        sidebar_icons = {
            "Dashboard": "assets/icons/dashboard.png",
            "Employees": "assets/icons/employees.png",
            "Settings": "assets/icons/settings.png"
        }
        self.sidebar_widget = Sidebar(self, pages=sidebar_icons)

        # Wrap Sidebar in QDockWidget
        self.sidebar = QDockWidget()
        self.sidebar.setTitleBarWidget(QWidget())  # Remove default title bar
        self.sidebar.setWidget(self.sidebar_widget)
        self.sidebar.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.sidebar)

    def set_page(self, page_name):
        from ui.animations_extra import slide_in_widget
        page = self.pages.get(page_name)
        if page:
            current = self.stack.currentWidget()
            if current is not page:
                # Set geometry for animation
                page.setGeometry(self.stack.geometry())
                self.stack.setCurrentWidget(page)
                slide_in_widget(page, direction="right", duration=400)
