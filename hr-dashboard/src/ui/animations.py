from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import QWidget

def fade_in_widget(widget: QWidget, duration=350):
    widget.setWindowOpacity(0)
    widget.show()
    anim = QPropertyAnimation(widget, b"windowOpacity")
    anim.setDuration(duration)
    anim.setStartValue(0)
    anim.setEndValue(1)
    anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
    anim.start()
    widget._fade_anim = anim  # Prevent garbage collection


def fade_out_widget(widget: QWidget, duration=350):
    anim = QPropertyAnimation(widget, b"windowOpacity")
    anim.setDuration(duration)
    anim.setStartValue(1)
    anim.setEndValue(0)
    anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
    def on_finished():
        widget.hide()
        widget.setWindowOpacity(1)
    anim.finished.connect(on_finished)
    anim.start()
    widget._fade_anim = anim
