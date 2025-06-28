from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QSlider, QPushButton, QComboBox, QHBoxLayout
from PySide6.QtCore import Qt
from components.compression_slider import CompressionSlider
from components.file_drop import FileDropArea

class PDFToImgView(QWidget):
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
        
        title = QLabel("PDF to Image Conversion")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #333333;
            }
        """)
        title_layout.addWidget(title)
        
        desc = QLabel("Extract images from PDF or convert pages to images")
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
        
        # Image format
        format_frame = QFrame()
        format_layout = QVBoxLayout(format_frame)
        format_layout.setContentsMargins(0, 0, 0, 0)
        format_layout.setSpacing(5)
        
        format_label = QLabel("Output Image Format:")
        format_label.setStyleSheet("font-size: 15px; color: #333333; font-weight: bold;")
        format_layout.addWidget(format_label)
        
        format_options = QFrame()
        format_options_layout = QHBoxLayout(format_options)
        format_options_layout.setContentsMargins(0, 0, 0, 0)
        format_options_layout.setSpacing(15)
        
        jpg_btn = QPushButton("JPG")
        jpg_btn.setCheckable(True)
        jpg_btn.setChecked(True)
        jpg_btn.setStyleSheet("""
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
        
        png_btn = QPushButton("PNG")
        png_btn.setCheckable(True)
        png_btn.setStyleSheet(jpg_btn.styleSheet())
        
        webp_btn = QPushButton("WEBP")
        webp_btn.setCheckable(True)
        webp_btn.setStyleSheet(jpg_btn.styleSheet())
        
        format_options_layout.addWidget(jpg_btn)
        format_options_layout.addWidget(png_btn)
        format_options_layout.addWidget(webp_btn)
        format_options_layout.addStretch()
        
        format_layout.addWidget(format_options)
        options_layout.addWidget(format_frame)
        
        # Page range
        page_range_frame = QFrame()
        page_range_layout = QVBoxLayout(page_range_frame)
        page_range_layout.setContentsMargins(0, 0, 0, 0)
        page_range_layout.setSpacing(5)
        
        page_range_label = QLabel("Page Range:")
        page_range_label.setStyleSheet("font-size: 15px; color: #333333; font-weight: bold;")
        page_range_layout.addWidget(page_range_label)
        
        page_range_combo = QComboBox()
        page_range_combo.addItems(["All pages", "Current page", "Custom range"])
        page_range_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        page_range_layout.addWidget(page_range_combo)
        options_layout.addWidget(page_range_frame)
        
        # DPI setting
        dpi_frame = QFrame()
        dpi_layout = QVBoxLayout(dpi_frame)
        dpi_layout.setContentsMargins(0, 0, 0, 0)
        dpi_layout.setSpacing(5)
        
        dpi_label = QLabel("Image Quality (DPI):")
        dpi_label.setStyleSheet("font-size: 15px; color: #333333; font-weight: bold;")
        dpi_layout.addWidget(dpi_label)
        
        self.dpi_slider = CompressionSlider()
        dpi_layout.addWidget(self.dpi_slider)
        
        # Slider labels
        slider_labels = QFrame()
        slider_labels_layout = QHBoxLayout(slider_labels)
        slider_labels_layout.setContentsMargins(0, 0, 0, 0)
        
        min_label = QLabel("Lower Quality")
        min_label.setStyleSheet("font-size: 13px; color: #666666;")
        slider_labels_layout.addWidget(min_label)
        
        slider_labels_layout.addStretch()
        
        max_label = QLabel("Higher Quality")
        max_label.setStyleSheet("font-size: 13px; color: #666666;")
        slider_labels_layout.addWidget(max_label)
        
        dpi_layout.addWidget(slider_labels)
        options_layout.addWidget(dpi_frame)
        
        layout.addWidget(options_frame)
        layout.addStretch()
        
        # Action buttons
        btn_frame = QFrame()
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(15)
        
        convert_btn = QPushButton("Convert to Images")
        convert_btn.setStyleSheet("""
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
        convert_btn.setCursor(Qt.PointingHandCursor)
        
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
        btn_layout.addWidget(convert_btn)
        
        layout.addWidget(btn_frame)