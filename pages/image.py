from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFrame, QLabel, QSlider, 
                              QPushButton, QHBoxLayout, QLineEdit, QButtonGroup)
from PySide6.QtCore import Qt, Signal
from components.file_drop import FileDropArea
from components.compression_slider import CompressionSlider

class ImageView(QWidget):
    compression_complete = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.image_path = None
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)
        
        # Title frame - matching PDFView exactly
        title_frame = QFrame()
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)
        
        title = QLabel("Image Compression")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #333333;
            }
        """)
        title_layout.addWidget(title)
        
        desc = QLabel("Compress JPG or PNG images without losing quality")
        desc.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #666666;
            }
        """)
        title_layout.addWidget(desc)
        
        layout.addWidget(title_frame)
        
        # Drop area
        self.drop_area = FileDropArea("Drop Images Here", "or click to browse files (JPG, PNG)", 'image')
        layout.addWidget(self.drop_area)
        
        # Options frame - matching PDFView exactly
        options_frame = QFrame()
        options_layout = QVBoxLayout(options_frame)
        options_layout.setContentsMargins(20, 20, 20, 20)
        options_layout.setSpacing(15)
        
        # Compression level - matching PDFView exactly
        comp_level_frame = QFrame()
        comp_level_layout = QVBoxLayout(comp_level_frame)
        comp_level_layout.setContentsMargins(0, 0, 0, 0)
        comp_level_layout.setSpacing(5)
        
        comp_level_label = QLabel("Compression Level:")
        comp_level_label.setStyleSheet("font-size: 15px; color: #333333; font-weight: bold;")
        comp_level_layout.addWidget(comp_level_label)
        
        self.comp_slider = CompressionSlider()
        comp_level_layout.addWidget(self.comp_slider)

        # Slider labels - matching PDFView exactly
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
        
        # Resize options
        resize_frame = QFrame()
        resize_layout = QVBoxLayout(resize_frame)
        resize_layout.setContentsMargins(0, 0, 0, 0)
        resize_layout.setSpacing(5)
        
        resize_label = QLabel("Resize Image (width × height):")
        resize_label.setStyleSheet("font-size: 15px; color: #333333; font-weight: bold;")
        resize_layout.addWidget(resize_label)
        
        resize_inputs = QFrame()
        resize_inputs_layout = QHBoxLayout(resize_inputs)
        resize_inputs_layout.setContentsMargins(0, 0, 0, 0)
        resize_inputs_layout.setSpacing(10)
        
        self.width_input = QLineEdit("800")
        self.width_input.setPlaceholderText("Width")
        self.width_input.setFixedWidth(80)
        self.width_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                font-size: 14px;
                color: black;
            }
        """)
        
        times_label = QLabel("×")
        times_label.setStyleSheet("font-size: 14px; color: #333333;")
        times_label.setAlignment(Qt.AlignCenter)
        
        self.height_input = QLineEdit("600")
        self.height_input.setPlaceholderText("Height")
        self.height_input.setFixedWidth(80)
        self.height_input.setStyleSheet(self.width_input.styleSheet())
        
        resize_inputs_layout.addWidget(self.width_input)
        resize_inputs_layout.addWidget(times_label)
        resize_inputs_layout.addWidget(self.height_input)
        resize_inputs_layout.addStretch()
        
        resize_layout.addWidget(resize_inputs)
        options_layout.addWidget(resize_frame)
        
        # Output format
        format_frame = QFrame()
        format_layout = QVBoxLayout(format_frame)
        format_layout.setContentsMargins(0, 0, 0, 0)
        format_layout.setSpacing(5)
        
        format_label = QLabel("Output Format:")
        format_label.setStyleSheet("font-size: 15px; color: #333333; font-weight: bold;")
        format_layout.addWidget(format_label)
        
        format_options = QFrame()
        format_options_layout = QHBoxLayout(format_options)
        format_options_layout.setContentsMargins(0, 0, 0, 0)
        format_options_layout.setSpacing(15)
        
        self.format_group = QButtonGroup(self)
        
        self.jpg_btn = QPushButton("JPG")
        self.jpg_btn.setCheckable(True)
        self.jpg_btn.setChecked(True)
        self.jpg_btn.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                color: #333333;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:checked {
                background-color: #009688;
                color: white;
            }
        """)
        
        self.png_btn = QPushButton("PNG")
        self.png_btn.setCheckable(True)
        self.png_btn.setStyleSheet(self.jpg_btn.styleSheet())
        
        self.format_group.addButton(self.jpg_btn, 0)
        self.format_group.addButton(self.png_btn, 1)
        
        format_options_layout.addWidget(self.jpg_btn)
        format_options_layout.addWidget(self.png_btn)
        format_options_layout.addStretch()
        
        format_layout.addWidget(format_options)
        options_layout.addWidget(format_frame)
        
        layout.addWidget(options_frame)
        layout.addStretch()
        
        # Action buttons - matching PDFView exactly
        btn_frame = QFrame()
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(15)
        
        self.compress_btn = QPushButton("Compress Images")
        self.compress_btn.setStyleSheet("""
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
            QPushButton:disabled {
                background-color: #b2dfdb;
            }
        """)
        self.compress_btn.setCursor(Qt.PointingHandCursor)
        self.compress_btn.setEnabled(False)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet("""
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
        self.cancel_btn.setCursor(Qt.PointingHandCursor)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.compress_btn)
        
        layout.addWidget(btn_frame)