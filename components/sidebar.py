from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from components.buttons import NavButton
from components.toggle import AnimatedToggle
from icons.icons import IconLabel

class Sidebar(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QFrame { background-color: #f9fafb; border: none; border-right: 1px solid #e5e7eb; }")
        self.setFixedWidth(300)
        
        sidebar_layout = QVBoxLayout(self)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        self.setup_logo(sidebar_layout)
        self.setup_navigation(sidebar_layout)
        self.setup_theme_toggle(sidebar_layout)
    
    def setup_logo(self, layout):
        logo_frame = QFrame()
        logo_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #10b981, stop:1 #059669);
                border: none;
            }
        """)
        logo_frame.setFixedHeight(120)
        
        logo_layout = QHBoxLayout(logo_frame)
        logo_layout.setContentsMargins(24, 0, 24, 0)
        logo_layout.setSpacing(16)
        
        app_icon = IconLabel("logo", 48)
        app_icon.setStyleSheet("border: none; background: transparent;")
        logo_layout.addWidget(app_icon)
        
        self.app_title = QLabel("Make It Tiny")
        self.app_title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 22px;
                font-weight: 700;
                line-height: 1.2;
                border: none;
                background: transparent;
            }
        """)
        logo_layout.addWidget(self.app_title)
        logo_layout.addStretch()
        
        layout.addWidget(logo_frame)
    
    def setup_navigation(self, layout):
        nav_frame = QFrame()
        nav_frame.setStyleSheet("QFrame { background: transparent; border: none; }")
        nav_layout = QVBoxLayout(nav_frame)
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
        layout.addWidget(nav_frame)
    
    def setup_theme_toggle(self, layout):
        theme_frame = QFrame()
        theme_frame.setStyleSheet("""
            QFrame { 
                border-top: 1px solid #e5e7eb; 
                background: transparent;
                border-left: none;
                border-right: none;
                border-bottom: none;
            }
        """)
        theme_layout = QHBoxLayout(theme_frame)
        theme_layout.setContentsMargins(24, 20, 24, 20)
        
        self.theme_label = QLabel("Dark Mode")
        self.theme_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #4b5563;
                font-weight: 500;
                border: none;
                background: transparent;
            }
        """)
        self.theme_toggle = AnimatedToggle()
        
        theme_layout.addWidget(self.theme_label)
        theme_layout.addStretch()
        theme_layout.addWidget(self.theme_toggle)
        
        layout.addWidget(theme_frame)
    
    def set_active_button(self, index):
        for i, btn in enumerate(self.nav_buttons):
            btn.set_active(i == index)