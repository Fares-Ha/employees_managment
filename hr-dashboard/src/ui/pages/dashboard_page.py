from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from services.staff_service import get_all_staff
from widgets.kpi_box import KpiBox
import os

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # KPI Boxes
        self.kpi_layout = QHBoxLayout()
        self.total_staff_box = KpiBox("Total Staff", 0, os.path.join(os.path.dirname(__file__), "..", "..", "assets", "icons", "users.svg"))
        self.min_salary_box = KpiBox("Minimum Salary", 0, os.path.join(os.path.dirname(__file__), "..", "..", "assets", "icons", "trending-down.svg"))
        self.max_salary_box = KpiBox("Maximum Salary", 0, os.path.join(os.path.dirname(__file__), "..", "..", "assets", "icons", "trending-up.svg"))
        self.avg_salary_box = KpiBox("Average Salary", 0, os.path.join(os.path.dirname(__file__), "..", "..", "assets", "icons", "dollar-sign.svg"))
        self.kpi_layout.addWidget(self.total_staff_box)
        self.kpi_layout.addWidget(self.min_salary_box)
        self.kpi_layout.addWidget(self.max_salary_box)
        self.kpi_layout.addWidget(self.avg_salary_box)
        self.layout.addLayout(self.kpi_layout)

        

        self.update_dashboard()

        from services.settings_service import get_settings
        settings = get_settings()
        theme = settings["theme"] if settings and "theme" in settings.keys() else "dark"
        self.update_icon_colors(theme)

    def update_dashboard(self):
        self.update_kpis()

    def update_kpis(self):
        staff = get_all_staff()
        if not staff:
            self.total_staff_box.set_value(0)
            self.min_salary_box.set_value(0)
            self.max_salary_box.set_value(0)
            self.avg_salary_box.set_value(0)
            return

        total_staff = len(staff)
        salaries = [s['salary'] for s in staff if s['salary'] is not None]

        min_salary = min(salaries) if salaries else 0
        max_salary = max(salaries) if salaries else 0
        avg_salary = sum(salaries) / len(salaries) if salaries else 0

        self.total_staff_box.set_value(total_staff)
        self.min_salary_box.set_value(f"${min_salary:,.2f}")
        self.max_salary_box.set_value(f"${max_salary:,.2f}")
        self.avg_salary_box.set_value(f"${avg_salary:,.2f}")

    def refresh_dashboard(self):
        self.update_dashboard()

    def update_icon_colors(self, theme):
        from core.theme import get_accent_color_dark, get_accent_color_light
        if theme == "light":
            color = get_accent_color_light()
        else:
            color = get_accent_color_dark()

        self.total_staff_box.set_icon_color(color)
        self.min_salary_box.set_icon_color(color)
        self.max_salary_box.set_icon_color(color)
        self.avg_salary_box.set_icon_color(color)
