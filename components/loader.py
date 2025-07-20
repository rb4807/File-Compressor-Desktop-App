from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QPen, QColor
from theme.theme import get_current_theme, get_app_primary_color

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
        self.status_label = QLabel("Processing...")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Progress indicator
        self.progress_label = QLabel("Please wait...")
        self.progress_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progress_label)
        
        # Apply initial theme
        self.apply_theme()
        
    def apply_theme(self):
        """Apply the current theme to the loader"""
        theme = get_current_theme()
        primary_color = get_app_primary_color()
        
        # Status label styling
        self.status_label.setStyleSheet(f"""
            QLabel {{
                font-size: 16px;
                color: {primary_color};
                font-weight: bold;
                background: transparent;
                border: none;
                margin: 5px 0px;
            }}
        """)
        
        # Progress label styling
        self.progress_label.setStyleSheet(f"""
            QLabel {{
                font-size: 13px;
                color: {getattr(theme, 'TEXT_SECONDARY', '#666666')};
                background: transparent;
                border: none;
                margin: 0px;
            }}
        """)
        
    def create_shadow_effect(self):
        """Create a shadow effect for the modal"""
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
        theme = get_current_theme()
        
        # Use getattr with fallback values for theme attributes
        bg_color = getattr(theme, 'SURFACE_BG', '#E6E6E6')
        border_color = getattr(theme, 'BORDER_PRIMARY', '#E0E0E0')
        
        # Draw background with rounded corners
        painter.setBrush(QColor(bg_color))
        painter.setPen(QPen(QColor(border_color), 2))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 15, 15)
        
        # Draw spinning loader in the dots frame area
        dots_rect = self.dots_frame.geometry()
        center_x = dots_rect.x() + dots_rect.width() // 2
        center_y = dots_rect.y() + dots_rect.height() // 2
        
        # Draw compression-themed spinning icon
        painter.translate(center_x, center_y)
        painter.rotate(self._rotation)
        
        # Draw file compression icon (stylized)
        pen = QPen(QColor(get_app_primary_color()), 3)
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
        self.apply_theme()
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.loader = LoaderWidget()
        layout.addWidget(self.loader)
        
        self.hide()
        
    def apply_theme(self):
        """Apply the current theme to the overlay"""
        # Fallback to dark semi-transparent overlay if theme doesn't specify
        overlay_color = "rgba(0, 0, 0, 120)"
        try:
            theme = get_current_theme()
            if hasattr(theme, 'OVERLAY_BG'):
                overlay_color = theme.OVERLAY_BG
        except:
            pass
            
        self.setStyleSheet(f"background-color: {overlay_color};")
        
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

def trigger_loader(action, parent_widget=None, message="Processing..."):
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