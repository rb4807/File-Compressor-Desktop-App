from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QRectF, Property
from PySide6.QtGui import QColor, QPainter

from theme.theme import get_app_base_color

class AnimatedToggle(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setFixedSize(QSize(60, 34))
        self.setCursor(Qt.PointingHandCursor)

        # Modern colors with better contrast
        self._bg_color = QColor("#e5e7eb")
        self._circle_color = QColor("#ffffff")
        self._active_color = get_app_base_color()
        self._border_color = QColor("#d1d5db")
        
        # Animation
        self._circle_position = 3
        self.animation = QPropertyAnimation(self, b"circle_position")
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.setDuration(250)
        
        self.toggled.connect(self.start_animation)
    
    def get_circle_position(self):
        return self._circle_position
    
    def set_circle_position(self, pos):
        self._circle_position = pos
        self.update()
    
    circle_position = Property(int, get_circle_position, set_circle_position)
        
    def start_animation(self):
        self.animation.stop()
        if self.isChecked():
            self.animation.setEndValue(30)
        else:
            self.animation.setEndValue(3)
        self.animation.start()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        
        # Draw background with subtle border
        bg_rect = QRectF(0, 0, self.width(), self.height())
        if self.isChecked():
            painter.setBrush(self._active_color)
        else:
            painter.setBrush(self._bg_color)
        painter.drawRoundedRect(bg_rect, 17, 17)
        
        # Draw circle with shadow effect
        circle_rect = QRectF(self._circle_position, 3, 28, 28)
        painter.setBrush(self._circle_color)
        painter.drawEllipse(circle_rect)
        
    def sizeHint(self):
        return QSize(60, 34)