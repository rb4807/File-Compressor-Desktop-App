from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QPushButton, QHBoxLayout, QLineEdit, QButtonGroup
from PySide6.QtCore import Qt, Signal, QThread, Signal

import os
from components.file_drop import FileDropArea
from components.compression_slider import CompressionSlider
from components.message import show_error_message, show_success_message
from components.loader import trigger_loader
from core.ImageCompressor.ImageCompressor import ImageCompressor
from theme.theme import theme_manager, get_current_theme, get_app_primary_color, get_app_primary_hover_color

class ImageCompressionWorker(QThread):
    """Worker thread for image compression to prevent UI freezing"""
    finished = Signal(str)  # Emits output path on success
    error = Signal(str)     # Emits error message on failure
    
    def __init__(self, image_path, quality, resize, output_format, colors, output_path):
        super().__init__()
        self.image_path = image_path
        self.quality = quality
        self.resize = resize
        self.output_format = output_format
        self.colors = colors
        self.output_path = output_path
        
    def run(self):
        try:
            # Call the backend processor
            processor = ImageCompressor(image_path=self.image_path)
            processed_data = processor.process_image(
                output_format=self.output_format, 
                quality=self.quality,
                resize=self.resize,
                colors=self.colors
            )
            
            # Save the result
            with open(self.output_path, 'wb') as f:
                f.write(processed_data)
                
            self.finished.emit(self.output_path)
        except Exception as e:
            self.error.emit(str(e))

class ImageView(QWidget):
    compression_complete = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.image_path = None
        self.compression_worker = None
        
        # Connect to theme manager
        theme_manager.theme_changed.connect(self.on_theme_changed)
        
        self.setup_ui()
        self.setup_connections()
        self.apply_theme()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)
        
        # Title frame - matching PDFView exactly
        title_frame = QFrame()
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)
        
        self.title = QLabel("Image Compression")
        title_layout.addWidget(self.title)
        
        self.desc = QLabel("Compress JPG or PNG images without losing quality")
        title_layout.addWidget(self.desc)
        
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
        
        self.comp_level_label = QLabel("Compression Level:")
        comp_level_layout.addWidget(self.comp_level_label)
        
        self.comp_slider = CompressionSlider()
        comp_level_layout.addWidget(self.comp_slider)

        # Slider labels - matching PDFView exactly
        slider_labels = QFrame()
        slider_labels_layout = QHBoxLayout(slider_labels)
        slider_labels_layout.setContentsMargins(0, 0, 0, 0)
        
        self.min_label = QLabel("Smaller File")
        slider_labels_layout.addWidget(self.min_label)
        
        slider_labels_layout.addStretch()
        
        self.max_label = QLabel("Better Quality")
        slider_labels_layout.addWidget(self.max_label)
        
        comp_level_layout.addWidget(slider_labels)
        options_layout.addWidget(comp_level_frame)
        
        # Resize options
        resize_frame = QFrame()
        resize_layout = QVBoxLayout(resize_frame)
        resize_layout.setContentsMargins(0, 0, 0, 0)
        resize_layout.setSpacing(5)
        
        self.resize_label = QLabel("Resize Image (width × height):")
        resize_layout.addWidget(self.resize_label)
        
        resize_inputs = QFrame()
        resize_inputs_layout = QHBoxLayout(resize_inputs)
        resize_inputs_layout.setContentsMargins(0, 0, 0, 0)
        resize_inputs_layout.setSpacing(10)
        
        self.width_input = QLineEdit("800")
        self.width_input.setPlaceholderText("Width")
        self.width_input.setFixedWidth(80)
        
        self.times_label = QLabel("×")
        self.times_label.setAlignment(Qt.AlignCenter)
        
        self.height_input = QLineEdit("600")
        self.height_input.setPlaceholderText("Height")
        self.height_input.setFixedWidth(80)
        
        resize_inputs_layout.addWidget(self.width_input)
        resize_inputs_layout.addWidget(self.times_label)
        resize_inputs_layout.addWidget(self.height_input)
        resize_inputs_layout.addStretch()
        
        resize_layout.addWidget(resize_inputs)
        options_layout.addWidget(resize_frame)
        
        # Output format
        format_frame = QFrame()
        format_layout = QVBoxLayout(format_frame)
        format_layout.setContentsMargins(0, 0, 0, 0)
        format_layout.setSpacing(5)
        
        self.format_label = QLabel("Output Format:")
        format_layout.addWidget(self.format_label)
        
        format_options = QFrame()
        format_options_layout = QHBoxLayout(format_options)
        format_options_layout.setContentsMargins(0, 0, 0, 0)
        format_options_layout.setSpacing(15)
        
        self.format_group = QButtonGroup(self)
        
        self.jpg_btn = QPushButton("JPG")
        self.jpg_btn.setCheckable(True)
        self.jpg_btn.setChecked(True)
        
        self.png_btn = QPushButton("PNG")
        self.png_btn.setCheckable(True)
        
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
        self.compress_btn.setCursor(Qt.PointingHandCursor)
        self.compress_btn.setEnabled(False)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setCursor(Qt.PointingHandCursor)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.compress_btn)
        
        layout.addWidget(btn_frame)

    def setup_connections(self):
        """Set up signal connections"""
        self.drop_area.files_dropped.connect(self.handle_file_dropped)
        self.compress_btn.clicked.connect(self.process_image)
        self.cancel_btn.clicked.connect(self.close)
        
    def on_theme_changed(self, is_dark_mode):
        """Handle theme changes from the theme manager"""
        self.apply_theme()
        
    def apply_theme(self):
        """Apply the current theme to all UI elements"""
        theme = get_current_theme()
        primary_color = get_app_primary_color()
        primary_hover = get_app_primary_hover_color()
        
        # Title styling
        self.title.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                font-weight: bold;
                color: {theme.TEXT_PRIMARY};
            }}
        """)
        
        # Description styling
        self.desc.setStyleSheet(f"""
            QLabel {{
                font-size: 16px;
                color: {theme.TEXT_SECONDARY};
            }}
        """)
        
        # Compression level label styling
        self.comp_level_label.setStyleSheet(f"""
            QLabel {{
                font-size: 15px; 
                color: {theme.TEXT_PRIMARY}; 
                font-weight: bold;
            }}
        """)
        
        # Slider labels styling
        self.min_label.setStyleSheet(f"""
            QLabel {{
                font-size: 13px; 
                color: {theme.TEXT_MUTED};
            }}
        """)
        
        self.max_label.setStyleSheet(f"""
            QLabel {{
                font-size: 13px; 
                color: {theme.TEXT_MUTED};
            }}
        """)
        
        # Resize label styling
        self.resize_label.setStyleSheet(f"""
            QLabel {{
                font-size: 15px; 
                color: {theme.TEXT_PRIMARY}; 
                font-weight: bold;
            }}
        """)
        
        # Times label styling
        self.times_label.setStyleSheet(f"""
            QLabel {{
                font-size: 14px; 
                color: {theme.TEXT_PRIMARY};
            }}
        """)
        
        # Input fields styling
        input_style = f"""
            QLineEdit {{
                padding: 8px;
                border: 1px solid {theme.BORDER_PRIMARY};
                border-radius: 4px;
                font-size: 14px;
                color: {theme.TEXT_PRIMARY};
                background-color: {theme.SURFACE_BG};
            }}
        """
        self.width_input.setStyleSheet(input_style)
        self.height_input.setStyleSheet(input_style)
        
        # Format label styling
        self.format_label.setStyleSheet(f"""
            QLabel {{
                font-size: 15px; 
                color: {theme.TEXT_PRIMARY}; 
                font-weight: bold;
            }}
        """)
        
        # Format button styling
        format_button_style = f"""
            QPushButton {{
                background-color: {theme.SURFACE_BG};
                color: {theme.TEXT_PRIMARY};
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-size: 14px;
            }}
            QPushButton:checked {{
                background-color: {primary_color};
                color: white;
            }}
        """
        self.jpg_btn.setStyleSheet(format_button_style)
        self.png_btn.setStyleSheet(format_button_style)
        
        # Compress button styling
        self.compress_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {primary_color};
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 5px;
                font-size: 15px;
                min-width: 180px;
            }}
            QPushButton:hover {{
                background-color: {primary_hover};
            }}
            QPushButton:disabled {{
                background-color: #b2dfdb;
            }}
        """)
        
        # Cancel button styling
        self.cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme.SURFACE_BG};
                color: {theme.TEXT_PRIMARY};
                border: 1px solid {theme.BORDER_PRIMARY};
                padding: 12px 24px;
                border-radius: 5px;
                font-size: 15px;
                min-width: 180px;
            }}
            QPushButton:hover {{
                background-color: {theme.BORDER_PRIMARY};
            }}
        """)
        
    def handle_file_dropped(self, file_path):
        """Handle when a file is dropped or selected"""
        self.image_path = file_path
        self.compress_btn.setEnabled(True)
        
    def process_image(self):
        """Process the image with the selected settings"""
        if not self.image_path:
            return
            
        # Show loader
        trigger_loader('show', self, "Compressing image...")
        
        # Disable UI controls during compression
        self.compress_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)
        
        try:
            # Get all the parameters from the UI
            quality = self.comp_slider.value()
            
            # Get resize dimensions
            try:
                width = int(self.width_input.text())
                height = int(self.height_input.text())
                resize = (width, height)
            except ValueError:
                resize = None  # Don't resize if invalid dimensions
            
            # Get output format
            output_format = 'jpg' if self.jpg_btn.isChecked() else 'png'
            
            # Static color value as per requirements
            colors = 128
            
            # Get output path
            output_path = self.get_output_path()
            
            # Create and start worker thread
            self.compression_worker = ImageCompressionWorker(
                self.image_path, quality, resize, output_format, colors, output_path
            )
            self.compression_worker.finished.connect(self.on_compression_success)
            self.compression_worker.error.connect(self.on_compression_error)
            self.compression_worker.start()
            
        except Exception as e:
            self.on_compression_error(str(e))
    
    def on_compression_success(self, output_path):
        """Handle successful compression"""
        # Hide loader
        trigger_loader('hide')
        
        # Re-enable UI controls
        self.compress_btn.setEnabled(True)
        self.cancel_btn.setEnabled(True)
        
        # Emit completion signal and show success message
        self.compression_complete.emit(output_path)
        show_success_message("Image compression successful!", f"Compressed image saved to:\n{output_path}")
        
        # Clean up worker
        if self.compression_worker:
            self.compression_worker.deleteLater()
            self.compression_worker = None
    
    def on_compression_error(self, error_message):
        """Handle compression error"""
        # Hide loader
        trigger_loader('hide')
        
        # Re-enable UI controls
        self.compress_btn.setEnabled(True)
        self.cancel_btn.setEnabled(True)
        
        # Show error message
        show_error_message(error_message, "Image compression failed")
        
        # Clean up worker
        if self.compression_worker:
            self.compression_worker.deleteLater()
            self.compression_worker = None
    
    def get_output_path(self):
        """Generate output path based on input path and selected format"""
        base, _ = os.path.splitext(self.image_path)
        ext = '.jpg' if self.jpg_btn.isChecked() else '.png'
        return f"{base}_compressed{ext}"
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Hide loader if visible
        trigger_loader('hide')
        
        # Stop worker thread if running
        if self.compression_worker and self.compression_worker.isRunning():
            self.compression_worker.terminate()
            self.compression_worker.wait()
        
        super().closeEvent(event)