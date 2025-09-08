from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from services.staff_service import get_all_staff
from widgets.kpi_box import KPIBox

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # KPI Boxes
        self.kpi_layout = QHBoxLayout()
        self.total_staff_box = KPIBox("Total Staff", 0)
        self.min_salary_box = KPIBox("Minimum Salary", 0)
        self.max_salary_box = KPIBox("Maximum Salary", 0)
        self.avg_salary_box = KPIBox("Average Salary", 0)
        self.kpi_layout.addWidget(self.total_staff_box)
        self.kpi_layout.addWidget(self.min_salary_box)
        self.kpi_layout.addWidget(self.max_salary_box)
        self.kpi_layout.addWidget(self.avg_salary_box)
        self.layout.addLayout(self.kpi_layout)

        self.canvas = FigureCanvas(Figure(figsize=(6, 4)))
        self.layout.addWidget(self.canvas)
        self.ax = self.canvas.figure.subplots()

        self.update_dashboard()

    def update_dashboard(self):
        self.plot_chart()
        self.update_kpis()

    def plot_chart(self):
        staff = get_all_staff()
        # Example: show staff per first letter of first name
        counts = {}
        for s in staff:
            first_letter = s["first_name"][0].upper()
            counts[first_letter] = counts.get(first_letter, 0) + 1

        self.ax.clear()
        self.ax.bar(counts.keys(), counts.values())
        self.ax.set_title("Staff Distribution by First Name Letter")
        self.canvas.draw()

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
