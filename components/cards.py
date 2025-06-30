from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsDropShadowEffect
from icons.icons import IconLabel
from theme.theme import get_current_theme, theme_manager, get_app_primary_color

class CompressionCard(QFrame):
    def __init__(self, title, description, icon_type=None, parent=None):
        super().__init__(parent)
        self.title = title
        self.description = description
        self.icon_type = icon_type
        
        self.setup_ui()
        
        # Connect to global theme manager
        theme_manager.theme_changed.connect(self.on_theme_changed)
        
        # Apply initial theme
        self.apply_theme()
    
    def setup_ui(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.setCursor(Qt.PointingHandCursor)
        
        # Enhanced shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        layout.setAlignment(Qt.AlignCenter)
        
        if self.icon_type:
            self.icon_label = IconLabel(self.icon_type, 48)
            layout.addWidget(self.icon_label, 0, Qt.AlignCenter)
        
        self.title_label = QLabel(self.title)
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)
        
        self.desc_label = QLabel(self.description)
        self.desc_label.setWordWrap(True)
        layout.addWidget(self.desc_label)
        
        self.setFixedSize(240, 220)
    
    def on_theme_changed(self, is_dark_mode):
        """Handle theme changes from the theme manager"""
        self.apply_theme()
    
    def apply_theme(self):
        """Apply the current theme to the card"""
        theme = get_current_theme()
        
        # Base card styles
        self.setStyleSheet(f"""
            CompressionCard {{
                background-color: {theme.SURFACE_BG};
                border-radius: 12px;
                border: 1px solid {theme.BORDER_PRIMARY};
            }}
            CompressionCard:hover {{
                border: 1px solid {get_app_primary_color()};
                background-color: {theme.APP_BG};
            }}
        """)
        
        # Title label styles
        self.title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: 600;
                color: {theme.TEXT_PRIMARY};
                margin: 0px;
                background: transparent;                      
            }}
        """)
        
        # Description label styles
        self.desc_label.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                color: {theme.TEXT_MUTED};
                text-align: center;
                line-height: 1.4;
                margin: 0px;
                background: transparent;
            }}
        """)
        
        # Update icon if needed (alternative approach if IconLabel doesn't support color changes)
        if hasattr(self, 'icon_label'):
            # Option 1: Recreate the icon with the new color
            # You might need to modify your IconLabel class to accept color parameters
            pass
            
            # Option 2: If icons are SVG, you could set a stylesheet
            self.icon_label.setStyleSheet(f"""
                background: transparent;
                color: {theme.TEXT_PRIMARY};
            """)