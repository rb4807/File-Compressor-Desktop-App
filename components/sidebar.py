from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Signal
from components.buttons import NavButton
from components.toggle import AnimatedToggle
from icons.icons import IconLabel
from theme.theme import get_current_theme, theme_manager

class Sidebar(QFrame):
    theme_changed = Signal(bool)  
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
        # Connect to global theme manager
        theme_manager.theme_changed.connect(self.on_global_theme_changed)
        self.theme_changed.connect(theme_manager.set_dark_mode)
        
        # Apply initial theme
        self.apply_theme()
        
    def setup_ui(self):
        self.setFixedWidth(300)
        
        sidebar_layout = QVBoxLayout(self)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        self.setup_logo(sidebar_layout)
        self.setup_navigation(sidebar_layout)
        self.setup_theme_toggle(sidebar_layout)
    
    def setup_logo(self, layout):
        self.logo_frame = QFrame()
        self.logo_frame.setFixedHeight(120)
        
        logo_layout = QHBoxLayout(self.logo_frame)
        logo_layout.setContentsMargins(24, 0, 24, 0)
        logo_layout.setSpacing(16)
        
        app_icon = IconLabel("logo", 48)
        app_icon.setStyleSheet("border: none; background: transparent;")
        logo_layout.addWidget(app_icon)
        
        self.app_title = QLabel("Make It Tiny")
        logo_layout.addWidget(self.app_title)
        logo_layout.addStretch()
        
        layout.addWidget(self.logo_frame)
    
    def setup_navigation(self, layout):
        self.nav_frame = QFrame()
        nav_layout = QVBoxLayout(self.nav_frame)
        nav_layout.setContentsMargins(20, 32, 20, 24)
        nav_layout.setSpacing(8)
        
        self.nav_buttons = [
            NavButton("Home", "home"),
            NavButton("Image Compression", "image"),
            NavButton("PDF Compression", "pdf_compress"),
            NavButton("PDF to Image", "pdf_to_image"),
            # NavButton("Image to PDF", "image_to_pdf")
        ]
        
        for btn in self.nav_buttons:
            nav_layout.addWidget(btn)
        
        nav_layout.addStretch()
        layout.addWidget(self.nav_frame)
    
    def setup_theme_toggle(self, layout):
        self.theme_frame = QFrame()
        theme_layout = QHBoxLayout(self.theme_frame)
        theme_layout.setContentsMargins(24, 20, 24, 20)
        
        # Theme icon and label container
        theme_info_layout = QHBoxLayout()
        theme_info_layout.setSpacing(8)
        
        self.theme_icon = QLabel("☀️")
        self.theme_label = QLabel("Light Mode")
        
        theme_info_layout.addWidget(self.theme_icon)
        theme_info_layout.addWidget(self.theme_label)
        
        self.theme_toggle = AnimatedToggle()
        # Connect the toggle signal to our theme change handler
        self.theme_toggle.toggled.connect(self.on_theme_toggle)
        
        theme_layout.addLayout(theme_info_layout)
        theme_layout.addStretch()
        theme_layout.addWidget(self.theme_toggle)
        
        layout.addWidget(self.theme_frame)
    
    def on_theme_toggle(self, checked):
        """Handle theme toggle state change"""
        # This will trigger the global theme change
        self.theme_changed.emit(checked)
    
    def on_global_theme_changed(self, is_dark_mode):
        """Handle global theme changes"""
        # Update toggle state without triggering signal
        self.theme_toggle.blockSignals(True)
        self.theme_toggle.setChecked(is_dark_mode)
        self.theme_toggle.blockSignals(False)
        
        # Apply theme
        self.apply_theme()
    
    def apply_theme(self):
        """Apply the current theme to all components"""
        theme = get_current_theme()
        is_dark = theme_manager.is_dark_mode
        
        # Update theme icon and label
        if is_dark:
            self.theme_icon.setText("🌙")
            self.theme_label.setText("Dark Mode")
        else:
            self.theme_icon.setText("☀️")
            self.theme_label.setText("Light Mode")
        
        # Apply styles
        self.apply_sidebar_styles(theme)
        self.apply_logo_styles(theme)
        self.apply_navigation_styles(theme)
        self.apply_theme_toggle_styles(theme)
    
    def apply_sidebar_styles(self, theme):
        """Apply sidebar background and border styles"""
        self.setStyleSheet(f"""
            QFrame {{ 
                background-color: {theme.APP_BG}; 
                border: none; 
                border-right: 1px solid {theme.BORDER_PRIMARY};
                color: {theme.TEXT_PRIMARY};
            }}
        """)
    
    def apply_logo_styles(self, theme):
        """Apply logo section styles"""
        self.logo_frame.setStyleSheet(f"""
            QFrame {{
                background: {theme.LOGO_GRADIENT};
                border: none;
            }}
        """)
        
        self.app_title.setStyleSheet(f"""
            QLabel {{
                color: {theme.TEXT_ON_PRIMARY};
                font-size: 22px;
                font-weight: 700;
                line-height: 1.2;
                border: none;
                background: transparent;
            }}
        """)
    
    def apply_navigation_styles(self, theme):
        """Apply navigation section styles"""
        self.nav_frame.setStyleSheet(f"""
            QFrame {{ 
                background: transparent; 
                border: none;
                color: {theme.TEXT_SECONDARY};
            }}
        """)
    
    def apply_theme_toggle_styles(self, theme):
        """Apply theme toggle section styles"""
        self.theme_frame.setStyleSheet(f"""
            QFrame {{ 
                border-top: 1px solid {theme.BORDER_PRIMARY}; 
                background: transparent;
                border-left: none;
                border-right: none;
                border-bottom: none;
                color: {theme.TEXT_TERTIARY};
            }}
        """)
        
        self.theme_icon.setStyleSheet(f"""
            QLabel {{
                color: {theme.TEXT_TERTIARY};
                font-size: 16px;
                border: none;
                background: transparent;
            }}
        """)
        
        self.theme_label.setStyleSheet(f"""
            QLabel {{
                color: {theme.TEXT_TERTIARY};
                font-size: 14px;
                font-weight: 500;
                border: none;
                background: transparent;
            }}
        """)
    
    def set_active_button(self, index):
        """Set the active navigation button"""
        for i, btn in enumerate(self.nav_buttons):
            btn.set_active(i == index)
    
    def set_dark_mode(self, dark_mode):
        """Programmatically set the theme mode"""
        theme_manager.set_dark_mode(dark_mode)