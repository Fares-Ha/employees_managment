from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtWidgets import QWidget

def slide_in_widget(widget: QWidget, direction="right", duration=350):
    parent = widget.parentWidget()
    if not parent:
        widget.show()
        return
    geo = widget.geometry()
    start_geo = QRect(geo)
    if direction == "right":
        start_geo.moveLeft(parent.width())
    elif direction == "left":
        start_geo.moveLeft(-geo.width())
    elif direction == "up":
        start_geo.moveTop(-geo.height())
    elif direction == "down":
        start_geo.moveTop(parent.height())
    widget.setGeometry(start_geo)
    widget.show()
    anim = QPropertyAnimation(widget, b"geometry")
    anim.setDuration(duration)
    anim.setStartValue(start_geo)
    anim.setEndValue(geo)
    anim.setEasingCurve(QEasingCurve.Type.OutCubic)
    anim.start()
    widget._slide_anim = anim


def scale_in_widget(widget: QWidget, duration=350):
    widget.setWindowOpacity(0)
    widget.setMinimumSize(1, 1)
    widget.show()
    anim = QPropertyAnimation(widget, b"windowOpacity")
    anim.setDuration(duration)
    anim.setStartValue(0)
    anim.setEndValue(1)
    anim.setEasingCurve(QEasingCurve.Type.OutBack)
    anim.start()
    widget._scale_anim = anim
