from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QComboBox, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from components.file_drop import FileDropArea

class ImgToPDFView(QWidget):
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
        
        title = QLabel("Image to PDF Conversion")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #333333;
            }
        """)
        title_layout.addWidget(title)
        
        desc = QLabel("Convert one or multiple images to a PDF document")
        desc.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #666666;
            }
        """)
        title_layout.addWidget(desc)
        
        layout.addWidget(title_frame)
        
        # Drop area
        drop_area = FileDropArea("Drop Images Here", "or click to browse image files (JPG, PNG, WEBP)")
        layout.addWidget(drop_area)
        
        # Options frame
        options_frame = QFrame()
        options_layout = QVBoxLayout(options_frame)
        options_layout.setContentsMargins(20, 20, 20, 20)
        options_layout.setSpacing(15)
        
        # Page size
        page_size_frame = QFrame()
        page_size_layout = QVBoxLayout(page_size_frame)
        page_size_layout.setContentsMargins(0, 0, 0, 0)
        page_size_layout.setSpacing(5)
        
        page_size_label = QLabel("PDF Page Size:")
        page_size_label.setStyleSheet("font-size: 15px; color: #333333; font-weight: bold;")
        page_size_layout.addWidget(page_size_label)
        
        page_size_combo = QComboBox()
        page_size_combo.addItems(["Auto", "Letter", "A4", "A3", "Legal"])
        page_size_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        page_size_layout.addWidget(page_size_combo)
        options_layout.addWidget(page_size_frame)
        
        # Orientation
        orientation_frame = QFrame()
        orientation_layout = QVBoxLayout(orientation_frame)
        orientation_layout.setContentsMargins(0, 0, 0, 0)
        orientation_layout.setSpacing(5)
        
        orientation_label = QLabel("Orientation:")
        orientation_label.setStyleSheet("font-size: 15px; color: #333333; font-weight: bold;")
        orientation_layout.addWidget(orientation_label)
        
        orientation_group = QFrame()
        orientation_group_layout = QHBoxLayout(orientation_group)
        orientation_group_layout.setContentsMargins(0, 0, 0, 0)
        orientation_group_layout.setSpacing(15)
        
        portrait_btn = QPushButton("Portrait")
        portrait_btn.setCheckable(True)
        portrait_btn.setChecked(True)
        portrait_btn.setStyleSheet("""
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
        
        landscape_btn = QPushButton("Landscape")
        landscape_btn.setCheckable(True)
        landscape_btn.setStyleSheet(portrait_btn.styleSheet())
        
        orientation_group_layout.addWidget(portrait_btn)
        orientation_group_layout.addWidget(landscape_btn)
        orientation_group_layout.addStretch()
        
        orientation_layout.addWidget(orientation_group)
        options_layout.addWidget(orientation_frame)
        
        layout.addWidget(options_frame)
        layout.addStretch()
        
        # Action buttons
        btn_frame = QFrame()
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(15)
        
        convert_btn = QPushButton("Convert to PDF")
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