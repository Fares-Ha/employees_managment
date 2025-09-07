from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from services.staff_service import get_all_staff

class AnalyticsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.kpi_label = QLabel()
        self.layout.addWidget(self.kpi_label)

        self.update_kpis()

    def update_kpis(self):
        staff = get_all_staff()
        total = len(staff)
        self.kpi_label.setText(f"Total Staff: {total}")
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from services.staff_service import get_all_staff

class AnalyticsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.kpi_label = QLabel()
        self.layout.addWidget(self.kpi_label)

        self.update_kpis()

    def update_kpis(self):
        staff = get_all_staff()
        total = len(staff)
        self.kpi_label.setText(f"Total Staff: {total}")
