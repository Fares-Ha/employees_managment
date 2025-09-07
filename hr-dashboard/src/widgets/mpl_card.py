from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class MplCard(QWidget):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        lbl = QLabel(title)
        layout.addWidget(lbl)
        self.fig, self.ax = plt.subplots(figsize=(4,3))
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)
