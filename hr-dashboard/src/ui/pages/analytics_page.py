from PyQt6.QtWidgets import QWidget, QVBoxLayout
from widgets.mpl_card import MplCard
from services import kpi_service

class AnalyticsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.employees_by_year_card = MplCard("Employees by Year of Birth")
        self.layout.addWidget(self.employees_by_year_card)

        self.plot_employees_by_year()

    def plot_employees_by_year(self):
        data = kpi_service.get_employees_by_dob_year()

        # Sort the data by year
        sorted_years = sorted(data.keys())
        counts = [data[year] for year in sorted_years]

        ax = self.employees_by_year_card.ax
        ax.clear()
        ax.plot(sorted_years, counts, marker='o')
        ax.set_title("Employee Distribution by Year of Birth")
        ax.set_xlabel("Year of Birth")
        ax.set_ylabel("Number of Employees")
        ax.grid(True)

        # Rotate x-axis labels for better readability if there are many years
        if len(sorted_years) > 10:
            self.employees_by_year_card.fig.autofmt_xdate()

        self.employees_by_year_card.canvas.draw()
