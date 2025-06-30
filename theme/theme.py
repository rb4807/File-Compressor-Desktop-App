from PySide6.QtGui import QColor

def get_app_secondary_color():
    return QColor("#6b7280")

# theme.py
from PySide6.QtGui import QColor
from PySide6.QtCore import QObject, Signal

class ThemeManager(QObject):
    theme_changed = Signal(bool)  # True for dark mode, False for light mode
    
    def __init__(self):
        super().__init__()
        self._is_dark_mode = False
    
    @property
    def is_dark_mode(self):
        return self._is_dark_mode
    
    def set_dark_mode(self, dark_mode):
        if self._is_dark_mode != dark_mode:
            self._is_dark_mode = dark_mode
            self.theme_changed.emit(dark_mode)
    
    def toggle_theme(self):
        self.set_dark_mode(not self._is_dark_mode)

# Global theme manager instance
theme_manager = ThemeManager()

# Primary Colors
def get_app_primary_color():
    return "#10b981"

def get_app_primary_hover_color():
    return "#059669"

def get_app_primary_dark_color():
    return "#065f46"

def get_app_primary_darker_color():
    return "#047857"

# Light Theme Colors
class LightTheme:
    # Background Colors
    APP_BG = "#f9fafb"
    CONTENT_BG = "#ffffff"
    SURFACE_BG = "#ffffff"
    
    # Border Colors
    BORDER_PRIMARY = "#e5e7eb"
    BORDER_SECONDARY = "#d1d5db"
    
    # Text Colors
    TEXT_PRIMARY = "#1f2937"      # Main text
    TEXT_SECONDARY = "#374151"    # Secondary text
    TEXT_TERTIARY = "#4b5563"     # Subtle text
    TEXT_MUTED = "#6b7280"        # Muted text
    TEXT_ON_PRIMARY = "#ffffff"   # Text on primary color
    
    # Interactive Colors
    HOVER_BG = "rgba(16, 185, 129, 0.1)"
    PRESSED_BG = "rgba(16, 185, 129, 0.15)"
    ACTIVE_BG = "rgba(16, 185, 129, 0.1)"
    
    # Gradients
    LOGO_GRADIENT = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #10b981, stop:1 #059669)"

# Dark Theme Colors
class DarkTheme:
    # Background Colors
    APP_BG = "#1f2937"
    CONTENT_BG = "#111827"
    SURFACE_BG = "#1f2937"
    
    # Border Colors
    BORDER_PRIMARY = "#374151"
    BORDER_SECONDARY = "#4b5563"
    
    # Text Colors
    TEXT_PRIMARY = "#f9fafb"      # Main text
    TEXT_SECONDARY = "#e5e7eb"    # Secondary text  
    TEXT_TERTIARY = "#d1d5db"     # Subtle text
    TEXT_MUTED = "#d5d6d6"        # Muted text
    TEXT_ON_PRIMARY = "#ffffff"   # Text on primary color
    
    # Interactive Colors
    HOVER_BG = "rgba(16, 185, 129, 0.15)"
    PRESSED_BG = "rgba(16, 185, 129, 0.2)"
    ACTIVE_BG = "rgba(16, 185, 129, 0.15)"
    
    # Gradients
    LOGO_GRADIENT = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #065f46, stop:1 #047857)"

def get_current_theme():
    """Get the current theme based on the theme manager state"""
    return DarkTheme if theme_manager.is_dark_mode else LightTheme

# Convenience functions for commonly used colors
def get_text_primary():
    return get_current_theme().TEXT_PRIMARY

def get_text_secondary():
    return get_current_theme().TEXT_SECONDARY

def get_text_tertiary():
    return get_current_theme().TEXT_TERTIARY

def get_app_bg():
    return get_current_theme().APP_BG

def get_border_primary():
    return get_current_theme().BORDER_PRIMARY

def get_hover_bg():
    return get_current_theme().HOVER_BG

def get_pressed_bg():
    return get_current_theme().PRESSED_BG

def get_active_bg():
    return get_current_theme().ACTIVE_BG

def get_logo_gradient():
    return get_current_theme().LOGO_GRADIENT