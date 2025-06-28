from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QSlider, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from components.compression_slider import CompressionSlider
from components.file_drop import FileDropArea

class PDFView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)
        
        # Title frame
        title_frame = QFrame()
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)
        
        title = QLabel("PDF Compression")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #333333;
            }
        """)
        title_layout.addWidget(title)
        
        desc = QLabel("Reduce PDF file size while preserving text and image quality")
        desc.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #666666;
            }
        """)
        title_layout.addWidget(desc)
        
        layout.addWidget(title_frame)
        
        # Drop area
        drop_area = FileDropArea("Drop PDF Files Here", "or click to browse PDF documents", 'pdf')
        layout.addWidget(drop_area)
        
        # Options frame
        options_frame = QFrame()
        options_layout = QVBoxLayout(options_frame)
        options_layout.setContentsMargins(20, 20, 20, 20)
        options_layout.setSpacing(15)
        
        # Compression level
        comp_level_frame = QFrame()
        comp_level_layout = QVBoxLayout(comp_level_frame)
        comp_level_layout.setContentsMargins(0, 0, 0, 0)
        comp_level_layout.setSpacing(5)
        
        comp_level_label = QLabel("Compression Level:")
        comp_level_label.setStyleSheet("font-size: 15px; color: #333333; font-weight: bold;")
        comp_level_layout.addWidget(comp_level_label)
        
        self.comp_slider = CompressionSlider()
        comp_level_layout.addWidget(self.comp_slider)
        
        # Slider labels
        slider_labels = QFrame()
        slider_labels_layout = QHBoxLayout(slider_labels)
        slider_labels_layout.setContentsMargins(0, 0, 0, 0)
        
        min_label = QLabel("Smaller File")
        min_label.setStyleSheet("font-size: 13px; color: #666666;")
        slider_labels_layout.addWidget(min_label)
        
        slider_labels_layout.addStretch()
        
        max_label = QLabel("Better Quality")
        max_label.setStyleSheet("font-size: 13px; color: #666666;")
        slider_labels_layout.addWidget(max_label)
        
        comp_level_layout.addWidget(slider_labels)
        options_layout.addWidget(comp_level_frame)
        
        layout.addWidget(options_frame)
        layout.addStretch()
        
        # Action buttons
        btn_frame = QFrame()
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(15)
        
        compress_btn = QPushButton("Compress PDF")
        compress_btn.setStyleSheet("""
            QPushButton {
                background-color: #009688;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 5px;
                font-size: 15px;
                min-width: 180px;
            }
            QPushButton:hover {
                background-color: #00796b;
            }
        """)
        compress_btn.setCursor(Qt.PointingHandCursor)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f5f5f5;
                color: #333333;
                border: 1px solid #e0e0e0;
                padding: 12px 24px;
                border-radius: 5px;
                font-size: 15px;
                min-width: 180px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        
        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(compress_btn)
        
        layout.addWidget(btn_frame)