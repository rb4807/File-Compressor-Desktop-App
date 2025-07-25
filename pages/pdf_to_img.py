from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QPushButton, QHBoxLayout, QButtonGroup
from PySide6.QtCore import Qt, Signal, QThread
import os

from components.compression_slider import CompressionSlider
from components.file_drop import FileDropArea
from components.message import show_error_message, show_success_message
from components.loader import trigger_loader
from core.PdfCompressor.PdfCompressor import PdfCompressor
from theme.theme import theme_manager, get_current_theme, get_app_primary_color, get_app_primary_hover_color

class PDFToImgWorker(QThread):
    """Worker thread for PDF to image conversion to prevent UI freezing"""
    finished = Signal(str)  # Emits output path on success
    error = Signal(str)     # Emits error message on failure
    
    def __init__(self, pdf_path, output_format, quality, output_path):
        super().__init__()
        self.pdf_path = pdf_path
        self.output_format = output_format
        self.quality = quality
        self.output_path = output_path
        
    def run(self):
        try:
            # Read the PDF file
            with open(self.pdf_path, 'rb') as f:
                pdf_data = f.read()
            
            # Call the backend processor
            processor = PdfCompressor()
            images_zip = processor.process_pdf(
                pdf_data=pdf_data,
                output_format=self.output_format,
                quality=self.quality
            )
            
            # Save the result
            processor.save_output(images_zip, self.output_path)
            
            self.finished.emit(self.output_path)
        except Exception as e:
            self.error.emit(str(e))

class PDFToImgView(QWidget):
    conversion_complete = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.pdf_path = None
        self.conversion_worker = None
        
        # Connect to theme manager
        theme_manager.theme_changed.connect(self.on_theme_changed)
        
        self.setup_ui()
        self.setup_connections()
        self.apply_theme()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)
        
        # Title frame
        title_frame = QFrame()
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)
        
        self.title = QLabel("PDF to Image Conversion")
        title_layout.addWidget(self.title)
        
        self.desc = QLabel("Extract images from PDF or convert pages to images")
        title_layout.addWidget(self.desc)
        
        layout.addWidget(title_frame)
        
        # Drop area
        self.drop_area = FileDropArea("Drop PDF Files Here", "or click to browse PDF documents", 'pdf')
        layout.addWidget(self.drop_area)
        
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
        
        self.format_label = QLabel("Output Image Format:")
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
        
        # Quality setting
        quality_frame = QFrame()
        quality_layout = QVBoxLayout(quality_frame)
        quality_layout.setContentsMargins(0, 0, 0, 0)
        quality_layout.setSpacing(5)
        
        self.quality_label = QLabel("Image Quality:")
        quality_layout.addWidget(self.quality_label)
        
        self.quality_slider = CompressionSlider()
        quality_layout.addWidget(self.quality_slider)
        
        # Slider labels
        slider_labels = QFrame()
        slider_labels_layout = QHBoxLayout(slider_labels)
        slider_labels_layout.setContentsMargins(0, 0, 0, 0)
        
        self.min_label = QLabel("Lower Quality")
        slider_labels_layout.addWidget(self.min_label)
        
        slider_labels_layout.addStretch()
        
        self.max_label = QLabel("Higher Quality")
        slider_labels_layout.addWidget(self.max_label)
        
        quality_layout.addWidget(slider_labels)
        options_layout.addWidget(quality_frame)
        
        layout.addWidget(options_frame)
        layout.addStretch()
        
        # Action buttons
        btn_frame = QFrame()
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(15)
        
        self.convert_btn = QPushButton("Convert to Images")
        self.convert_btn.setCursor(Qt.PointingHandCursor)
        self.convert_btn.setEnabled(False)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setCursor(Qt.PointingHandCursor)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.convert_btn)
        
        layout.addWidget(btn_frame)

    def setup_connections(self):
        """Set up signal connections"""
        self.drop_area.files_dropped.connect(self.handle_file_dropped)
        self.convert_btn.clicked.connect(self.process_pdf)
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
        
        # Format label styling
        self.format_label.setStyleSheet(f"""
            QLabel {{
                font-size: 15px; 
                color: {theme.TEXT_PRIMARY}; 
                font-weight: bold;
            }}
        """)
        
        # Quality label styling
        self.quality_label.setStyleSheet(f"""
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
        
        # Convert button styling
        self.convert_btn.setStyleSheet(f"""
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
        self.pdf_path = file_path
        self.convert_btn.setEnabled(True)
        
    def process_pdf(self):
        """Process the PDF with the selected settings"""
        if not self.pdf_path:
            return
            
        # Show loader
        trigger_loader('show', self, "Compressing images...")
        
        # Disable UI controls during conversion
        self.convert_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)
        
        try:
            # Get all the parameters from the UI
            quality = self.quality_slider.value()
            output_format = 'jpg' if self.jpg_btn.isChecked() else 'png'
            
            # Get output path
            output_path = self.get_output_path(output_format)
            
            # Create and start worker thread
            self.conversion_worker = PDFToImgWorker(
                self.pdf_path, output_format, quality, output_path
            )
            self.conversion_worker.finished.connect(self.on_conversion_success)
            self.conversion_worker.error.connect(self.on_conversion_error)
            self.conversion_worker.start()
            
        except Exception as e:
            self.on_conversion_error(str(e))
    
    def on_conversion_success(self, output_path):
        """Handle successful conversion"""
        # Hide loader
        trigger_loader('hide')
        
        # Re-enable UI controls
        self.convert_btn.setEnabled(True)
        self.cancel_btn.setEnabled(True)
        
        # Emit completion signal and show success message
        self.conversion_complete.emit(output_path)
        show_success_message("PDF conversion successful!", f"Images saved to:\n{output_path}")
        
        # Clean up worker
        if self.conversion_worker:
            self.conversion_worker.deleteLater()
            self.conversion_worker = None
    
    def on_conversion_error(self, error_message):
        """Handle conversion error"""
        # Hide loader
        trigger_loader('hide')
        
        # Re-enable UI controls
        self.convert_btn.setEnabled(True)
        self.cancel_btn.setEnabled(True)
        
        # Show error message
        show_error_message(error_message, "PDF conversion failed")
        
        # Clean up worker
        if self.conversion_worker:
            self.conversion_worker.deleteLater()
            self.conversion_worker = None
            
    def get_output_path(self, output_format: str) -> str:
        """Generate output path based on input path and format"""
        base, _ = os.path.splitext(self.pdf_path)
        return f"{base}_converted_{output_format}.zip"
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Hide loader if visible
        trigger_loader('hide')
        
        # Stop worker thread if running
        if self.conversion_worker and self.conversion_worker.isRunning():
            self.conversion_worker.terminate()
            self.conversion_worker.wait()
        
        super().closeEvent(event)