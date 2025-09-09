from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QRect, QParallelAnimationGroup
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

def slide_and_fade_in_widget(widget: QWidget, direction="right", duration=400):
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
    widget.setWindowOpacity(0)
    widget.show()

    anim_slide = QPropertyAnimation(widget, b"geometry")
    anim_slide.setDuration(duration)
    anim_slide.setStartValue(start_geo)
    anim_slide.setEndValue(geo)
    anim_slide.setEasingCurve(QEasingCurve.Type.OutCubic)

    anim_fade = QPropertyAnimation(widget, b"windowOpacity")
    anim_fade.setDuration(duration)
    anim_fade.setStartValue(0)
    anim_fade.setEndValue(1)
    anim_fade.setEasingCurve(QEasingCurve.Type.InOutQuad)

    anim_group = QParallelAnimationGroup()
    anim_group.addAnimation(anim_slide)
    anim_group.addAnimation(anim_fade)
    anim_group.start()

    widget._slide_fade_anim = anim_group
