from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from widgets.kpi_card import KPICard
from widgets.mpl_card import MplCard
from services import kpi_service

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # KPI Cards
        kpi_layout = QHBoxLayout()
        self.layout.addLayout(kpi_layout)

        total_employees = kpi_service.get_total_employees()
        avg_salary = kpi_service.get_average_salary()

        self.total_employees_card = KPICard("Total Employees", str(total_employees))
        kpi_layout.addWidget(self.total_employees_card)

        self.avg_salary_card = KPICard("Average Salary", f"${avg_salary:,.2f}")
        kpi_layout.addWidget(self.avg_salary_card)

        kpi_layout.addStretch()

        # Charts
        chart_layout = QGridLayout()
        self.layout.addLayout(chart_layout)

        self.salary_dist_card = MplCard("Salary Distribution (Bar)")
        self.plot_salary_distribution_bar()
        chart_layout.addWidget(self.salary_dist_card, 0, 0)

        self.salary_dist_pie_card = MplCard("Salary Distribution (Pie)")
        self.plot_salary_distribution_pie()
        chart_layout.addWidget(self.salary_dist_pie_card, 0, 1)

    def plot_salary_distribution_bar(self):
        distribution = kpi_service.get_salary_distribution()
        ax = self.salary_dist_card.ax
        ax.clear()
        ax.bar(distribution.keys(), distribution.values())
        ax.set_title("Salary Distribution")
        ax.set_ylabel("Number of Employees")
        self.salary_dist_card.canvas.draw()

    def plot_salary_distribution_pie(self):
        distribution = kpi_service.get_salary_distribution()
        ax = self.salary_dist_pie_card.ax
        ax.clear()

        # Filter out zero values to avoid cluttering the pie chart
        filtered_dist = {k: v for k, v in distribution.items() if v > 0}

        ax.pie(filtered_dist.values(), labels=filtered_dist.keys(), autopct='%1.1f%%', startangle=90)
        ax.set_title("Salary Distribution")
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        self.salary_dist_pie_card.canvas.draw()
