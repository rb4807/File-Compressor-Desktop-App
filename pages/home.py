# pages/home.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from components.cards import CompressionCard

class HomeView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent 
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)
        
        # Welcome section
        welcome_frame = QFrame()
        welcome_layout = QVBoxLayout(welcome_frame)
        welcome_layout.setContentsMargins(0, 0, 0, 0)
        welcome_layout.setSpacing(16)
        
        welcome_title = QLabel("Welcome to Make It Tiny")
        welcome_title.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: 700;
                color: #1f2937;
                margin: 0px;
            }
        """)
        welcome_layout.addWidget(welcome_title)
        
        welcome_desc = QLabel("Compress your files without quality loss. Select a compression type below to get started.")
        welcome_desc.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #6b7280;
                line-height: 1.5;
                margin: 0px;
            }
        """)
        welcome_layout.addWidget(welcome_desc)
        
        layout.addWidget(welcome_frame)
        
        # Compression options
        options_frame = QFrame()
        options_layout = QHBoxLayout(options_frame)
        options_layout.setContentsMargins(0, 0, 0, 0)
        options_layout.setSpacing(32)
        
        # Create cards
        self.image_card = CompressionCard("Image Compression", 
                                        "Compress JPG, PNG, WEBP images without quality loss",
                                        "image")
        self.pdf_card = CompressionCard("PDF Compression", 
                                      "Reduce PDF file size while preserving quality",
                                      "pdf")
        # self.img_to_pdf_card = CompressionCard("Image to PDF", 
        #                                      "Convert images to high-quality PDF documents",
        #                                      "image_to_pdf")
        self.pdf_to_img_card = CompressionCard("PDF to Image", 
                                            "Extract images from PDF files or convert pages to images",
                                            "pdf_to_image")
        
        options_layout.addWidget(self.image_card)
        options_layout.addWidget(self.pdf_card)
        # options_layout.addWidget(self.img_to_pdf_card)
        options_layout.addWidget(self.pdf_to_img_card)
        
        layout.addWidget(options_frame, alignment=Qt.AlignCenter)
        layout.addStretch()
        
        # Connect card clicks to switch views
        self.image_card.mousePressEvent = lambda e: self.switch_view(1)
        self.pdf_card.mousePressEvent = lambda e: self.switch_view(2)
        self.pdf_to_img_card.mousePressEvent = lambda e: self.switch_view(3)
        # self.img_to_pdf_card.mousePressEvent = lambda e: self.switch_view(4)
    
    def switch_view(self, index):
        """Switch to the corresponding view using parent window's method"""
        if hasattr(self.parent_window, 'switch_view'):
            self.parent_window.switch_view(index)