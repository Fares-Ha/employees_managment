from PyQt6.QtWidgets import QStackedWidget, QWidget
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, pyqtProperty

class AnimatedStackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_direction = 'horizontal'
        self.m_speed = 500
        self.m_animation_type = QEasingCurve.Type.OutCubic
        self.m_now = 0
        self.m_next = 0
        self.m_wrap = False
        self.m_pnow = QPoint(0, 0)
        self.m_active = False

    def setDirection(self, direction):
        self.m_direction = direction

    def setSpeed(self, speed):
        self.m_speed = speed

    def setAnimation(self, animation_type):
        self.m_animation_type = animation_type

    def setWrap(self, wrap):
        self.m_wrap = wrap

    def slideInNext(self):
        now = self.currentIndex()
        if self.m_wrap and now == self.count() - 1:
            self.slideInIdx(0)
        else:
            self.slideInIdx(now + 1)

    def slideInPrev(self):
        now = self.currentIndex()
        if self.m_wrap and now == 0:
            self.slideInIdx(self.count() - 1)
        else:
            self.slideInIdx(now - 1)

    def slideInIdx(self, idx):
        if idx > self.count() - 1:
            idx = self.count() - 1
        if idx < 0:
            idx = 0

        # Prevent animation if the page is already active
        if idx == self.currentIndex():
            return

        if self.m_active:
            return

        self.m_active = True
        self.m_next = idx
        self.m_now = self.currentIndex()

        self.m_pnow = self.widget(self.m_now).pos()

        if self.m_direction == 'horizontal':
            offset_x = self.frameRect().width()
            offset_y = 0
        else:
            offset_x = 0
            offset_y = self.frameRect().height()

        self.widget(self.m_next).show()

        if self.m_now < self.m_next:
            self.widget(self.m_next).move(offset_x, offset_y)
            pnext = QPoint(0,0)
            pnow = QPoint(-offset_x, -offset_y)
        else:
            self.widget(self.m_next).move(-offset_x, -offset_y)
            pnext = QPoint(0,0)
            pnow = QPoint(offset_x, offset_y)

        anim_now = QPropertyAnimation(self.widget(self.m_now), b"pos")
        anim_now.setDuration(self.m_speed)
        anim_now.setEasingCurve(self.m_animation_type)
        anim_now.setEndValue(pnow)

        anim_next = QPropertyAnimation(self.widget(self.m_next), b"pos")
        anim_next.setDuration(self.m_speed)
        anim_next.setEasingCurve(self.m_animation_type)
        anim_next.setEndValue(pnext)

        anim_group = [anim_now, anim_next]
        for anim in anim_group:
            anim.start()

        anim_now.finished.connect(self._on_animation_finished)

    def _on_animation_finished(self):
        self.widget(self.m_now).hide()
        self.widget(self.m_now).move(self.m_pnow)
        self.setCurrentIndex(self.m_next)
        self.m_active = False

    def setCurrentWidget(self, widget):
        self.slideInIdx(self.indexOf(widget))

    # The default setCurrentIndex is overridden for the animation.
    # To set the initial index without animation, we need a separate method.
    def setInitialIndex(self, index):
        super().setCurrentIndex(index)
