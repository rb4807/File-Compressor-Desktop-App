from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QPen, QColor

class LoaderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(250, 150)  
        self.setup_ui()
        self.setup_animation()
        
    def setup_ui(self):
        # Remove any background styling to let paintEvent handle it
        self.setStyleSheet("background: transparent;")
        
        # Add shadow effect
        self.setGraphicsEffect(self.create_shadow_effect())
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignCenter)
        
        # Animated dots container
        self.dots_frame = QFrame()
        self.dots_frame.setFixedHeight(40)
        self.dots_frame.setStyleSheet("background: transparent; border: none;")
        layout.addWidget(self.dots_frame)
        
        # Status label
        self.status_label = QLabel("Compressing files...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #009688;
                font-weight: bold;
                background: transparent;
                border: none;
                margin: 5px 0px;
            }
        """)
        layout.addWidget(self.status_label)
        
        # Progress indicator
        self.progress_label = QLabel("Please wait...")
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #666666;
                background: transparent;
                border: none;
                margin: 0px;
            }
        """)
        layout.addWidget(self.progress_label)
        
    def create_shadow_effect(self):
        """Create a shadow effect for the modal"""
        from PySide6.QtWidgets import QGraphicsDropShadowEffect
        from PySide6.QtGui import QColor
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 80))
        return shadow
        
    def setup_animation(self):
        # Rotation angle for spinning animation
        self._rotation = 0
        
        # Timer for animation
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.setInterval(100)  # Update every 100ms
        
    def update_animation(self):
        self._rotation = (self._rotation + 30) % 360
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw modal background with border
        rect = self.rect()
        
        # Draw white background with rounded corners
        painter.setBrush(QColor(230, 230, 230))
        painter.setPen(QPen(QColor(224, 224, 224), 2))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 15, 15)
        
        # Draw spinning loader in the dots frame area
        dots_rect = self.dots_frame.geometry()
        center_x = dots_rect.x() + dots_rect.width() // 2
        center_y = dots_rect.y() + dots_rect.height() // 2
        
        # Draw compression-themed spinning icon
        painter.translate(center_x, center_y)
        painter.rotate(self._rotation)
        
        # Draw file compression icon (stylized) - larger for better visibility
        pen = QPen(QColor(0, 150, 136), 3)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        
        # Draw folder/file icon with compression arrows
        painter.drawRect(-15, -10, 30, 20)
        painter.drawLine(-10, -15, 0, -10)  # Top arrow
        painter.drawLine(0, -10, 10, -15)   # Top arrow
        painter.drawLine(-10, 15, 0, 10)    # Bottom arrow  
        painter.drawLine(0, 10, 10, 15)     # Bottom arrow
        
        painter.resetTransform()
        
    def start_animation(self):
        self.animation_timer.start()
        
    def stop_animation(self):
        self.animation_timer.stop()


class LoaderOverlay(QWidget):
    """Overlay widget that covers the entire parent widget with modal backdrop"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        # Semi-transparent dark backdrop for modal effect
        self.setStyleSheet("background-color: rgba(0, 0, 0, 120);")
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.loader = LoaderWidget()
        layout.addWidget(self.loader)
        
        self.hide()
        
    def showEvent(self, event):
        super().showEvent(event)
        self.loader.start_animation()
        
    def hideEvent(self, event):
        super().hideEvent(event)
        self.loader.stop_animation()
        
    def resizeEvent(self, event):
        # Make sure overlay covers the entire parent
        if self.parent():
            self.resize(self.parent().size())
        super().resizeEvent(event)


# Global loader management
_loader_overlay = None

def trigger_loader(action, parent_widget=None, message="Compressing files..."):
    """
    Global function to show/hide loader
    
    Args:
        action (str): 'show' or 'hide'
        parent_widget (QWidget): Widget to overlay the loader on
        message (str): Custom message to display
    """
    global _loader_overlay
    
    if action == 'show':
        if parent_widget is None:
            raise ValueError("parent_widget is required when showing loader")
            
        # Create new overlay if it doesn't exist or parent changed
        if _loader_overlay is None or _loader_overlay.parent() != parent_widget:
            _loader_overlay = LoaderOverlay(parent_widget)
            
        # Update message
        _loader_overlay.loader.status_label.setText(message)
        
        # Position and show overlay
        _loader_overlay.resize(parent_widget.size())
        _loader_overlay.show()
        _loader_overlay.raise_()
        
    elif action == 'hide':
        if _loader_overlay:
            _loader_overlay.hide()
    else:
        raise ValueError("action must be 'show' or 'hide'")


def set_loader_message(message):
    """Update the loader message while it's showing"""
    global _loader_overlay
    if _loader_overlay and _loader_overlay.isVisible():
        _loader_overlay.loader.status_label.setText(message)