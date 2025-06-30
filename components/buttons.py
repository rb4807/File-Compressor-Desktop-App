from PySide6.QtWidgets import QPushButton, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from icons.icons import IconLabel
from theme.theme import get_app_primary_color, get_current_theme, theme_manager

class NavButton(QPushButton):
    def __init__(self, text, icon_type=None, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self._is_active = False
        
        # Create layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(12)
        
        # Add icon if provided
        if icon_type:
            self.icon = IconLabel(icon_type, 18)
            layout.addWidget(self.icon)
        else:
            self.icon = None
        
        # Add text label
        self.label = QLabel(text)
        layout.addWidget(self.label)
        layout.addStretch()
        
        self.setFixedHeight(48)
        
        # Connect to theme changes
        theme_manager.theme_changed.connect(self.apply_theme)
        
        # Apply initial theme
        self.apply_theme()
    
    def apply_theme(self):
        """Apply the current theme to the button"""
        theme = get_current_theme()
        
        if self._is_active:
            self.apply_active_style(theme)
        else:
            self.apply_inactive_style(theme)
    
    def apply_inactive_style(self, theme):
        """Apply inactive button styling"""
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                text-align: left;
                padding: 0px;
                border-radius: 8px;
                margin: 2px 0px;
            }}
            QPushButton:hover {{
                background-color: {theme.HOVER_BG};
            }}
            QPushButton:pressed {{
                background-color: {theme.PRESSED_BG};
            }}
        """)
        
        self.label.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                color: {theme.TEXT_SECONDARY};
                font-weight: 500;
                background: transparent;
                border: none;
            }}
        """)
    
    def apply_active_style(self, theme):
        """Apply active button styling"""
        primary_color = get_app_primary_color()
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme.ACTIVE_BG};
                border: none;
                text-align: left;
                padding: 0px;
                border-radius: 8px;
                margin: 2px 0px;
                border-left: 3px solid {primary_color};
            }}
            QPushButton:hover {{
                background-color: {theme.HOVER_BG};
            }}
        """)
        
        self.label.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                color: {primary_color};
                font-weight: 600;
                background: transparent;
                border: none;
            }}
        """)
    
    def set_active(self, active=True):
        """Set the active state of the button"""
        self._is_active = active
        self.apply_theme()
    
    def apply_light_theme(self):
        """Legacy method for compatibility - use apply_theme instead"""
        if not theme_manager.is_dark_mode:
            self.apply_theme()
    
    def apply_dark_theme(self):
        """Legacy method for compatibility - use apply_theme instead"""
        if theme_manager.is_dark_mode:
            self.apply_theme()