from PyQt6.QtWidgets import (
    QMainWindow, QStackedWidget, QDockWidget, QWidget
)
from PyQt6.QtCore import Qt
from ui.pages.dashboard_page import DashboardPage
from ui.pages.employees_page import EmployeesPage
from ui.pages.analytics_page import AnalyticsPage
from ui.sidebar import Sidebar

class HRDashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HR Dashboard")
        self.resize(1200, 800)

        # Pages
        self.pages = {
            "Dashboard": DashboardPage(),
            "Employees": EmployeesPage(),
            "Analytics": AnalyticsPage()
        }

        self.stack = QStackedWidget()
        for page in self.pages.values():
            self.stack.addWidget(page)
        self.setCentralWidget(self.stack)

        # Sidebar
        sidebar_icons = {
            "Dashboard": "assets/icons/dashboard.png",
            "Employees": "assets/icons/employees.png",
            "Analytics": "assets/icons/analytics.png"
        }
        self.sidebar_widget = Sidebar(self, pages=sidebar_icons)

        # Wrap Sidebar in QDockWidget
        self.sidebar = QDockWidget()
        self.sidebar.setTitleBarWidget(QWidget())  # Remove default title bar
        self.sidebar.setWidget(self.sidebar_widget)
        self.sidebar.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.sidebar)

    def set_page(self, page_name):
        page = self.pages.get(page_name)
        if page:
            self.stack.setCurrentWidget(page)
