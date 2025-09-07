from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from services.staff_service import get_all_staff

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.canvas = FigureCanvas(Figure(figsize=(6, 4)))
        self.layout.addWidget(self.canvas)
        self.ax = self.canvas.figure.subplots()

        self.plot_chart()

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
