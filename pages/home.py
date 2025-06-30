from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from components.cards import CompressionCard
from theme.theme import theme_manager, get_current_theme

class HomeView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent 
        
        # Connect to theme manager
        theme_manager.theme_changed.connect(self.on_theme_changed)
        
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        """Setup the UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)
        
        # Welcome section
        self.welcome_frame = QFrame()
        self.welcome_frame.setFrameStyle(QFrame.NoFrame)
        welcome_layout = QVBoxLayout(self.welcome_frame)
        welcome_layout.setContentsMargins(0, 0, 0, 0)
        welcome_layout.setSpacing(16)
        
        self.welcome_title = QLabel("Welcome to Make It Tiny")
        welcome_layout.addWidget(self.welcome_title)
        
        self.welcome_desc = QLabel("Compress your files without quality loss. Select a compression type below to get started.")
        self.welcome_desc.setWordWrap(True)
        welcome_layout.addWidget(self.welcome_desc)
        
        layout.addWidget(self.welcome_frame)
        
        # Compression options
        self.options_frame = QFrame()
        self.options_frame.setFrameStyle(QFrame.NoFrame)
        options_layout = QHBoxLayout(self.options_frame)
        options_layout.setContentsMargins(0, 0, 0, 0)
        options_layout.setSpacing(32)
        
        # Create cards
        self.image_card = CompressionCard("Image Compression", 
                                        "Compress JPG, PNG, WEBP images without quality loss",
                                        "image")
        self.pdf_card = CompressionCard("PDF Compression", 
                                      "Reduce PDF file size while preserving quality",
                                      "pdf")
        self.pdf_to_img_card = CompressionCard("PDF to Image", 
                                            "Extract images from PDF files or convert pages to images",
                                            "pdf_to_image")
        
        options_layout.addWidget(self.image_card)
        options_layout.addWidget(self.pdf_card)
        options_layout.addWidget(self.pdf_to_img_card)
        
        layout.addWidget(self.options_frame, alignment=Qt.AlignCenter)
        layout.addStretch()
        
        # Connect card clicks to switch views
        self.image_card.mousePressEvent = lambda e: self.switch_view(1)
        self.pdf_card.mousePressEvent = lambda e: self.switch_view(2)
        self.pdf_to_img_card.mousePressEvent = lambda e: self.switch_view(3)
    
    def apply_theme(self):
        """Apply the current theme to all components"""
        theme = get_current_theme()
        
        # Main widget styling
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {theme.CONTENT_BG};
                border: none;
            }}
        """)
        
        # Welcome frame styling
        self.welcome_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {theme.CONTENT_BG};
                border: none;
                margin: 0px;
                padding: 0px;
            }}
        """)
        
        # Options frame styling
        self.options_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {theme.CONTENT_BG};
                border: none;
                margin: 0px;
                padding: 0px;
            }}
        """)
        
        # Welcome title styling
        self.welcome_title.setStyleSheet(f"""
            QLabel {{
                font-size: 32px;
                font-weight: 700;
                color: {theme.TEXT_PRIMARY};
                background-color: transparent;
                border: none;
                margin: 0px;
                padding: 0px;
            }}
        """)
        
        # Welcome description styling
        self.welcome_desc.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                color: {theme.TEXT_SECONDARY};
                background-color: transparent;
                border: none;
                line-height: 1.5;
                margin: 0px;
                padding: 0px;
            }}
        """)
        
        # Apply theme to cards if they have theme support
        cards = [self.image_card, self.pdf_card, self.pdf_to_img_card]
        for card in cards:
            if hasattr(card, 'apply_theme'):
                card.apply_theme()
            elif hasattr(card, 'on_theme_changed'):
                card.on_theme_changed(theme_manager.is_dark_mode())
    
    def on_theme_changed(self, is_dark_mode):
        """Handle theme changes"""
        self.apply_theme()
    
    def switch_view(self, index):
        """Switch to the corresponding view using parent window's method"""
        if hasattr(self.parent_window, 'switch_view'):
            self.parent_window.switch_view(index)