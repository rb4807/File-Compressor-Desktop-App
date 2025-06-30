from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, Signal, QThread, Signal
import os

from components.compression_slider import CompressionSlider
from components.file_drop import FileDropArea
from components.message import show_error_message, show_success_message
from components.loader import trigger_loader  
from core.PdfCompressor.PdfCompressor import PdfCompressor
from theme.theme import theme_manager, get_current_theme, get_app_primary_color, get_app_primary_hover_color

class PDFCompressionWorker(QThread):
    """Worker thread for PDF compression to prevent UI freezing"""
    finished = Signal(str)  # Emits output path on success
    error = Signal(str)     # Emits error message on failure
    
    def __init__(self, pdf_path, quality, output_path):
        super().__init__()
        self.pdf_path = pdf_path
        self.quality = quality
        self.output_path = output_path
        
    def run(self):
        try:
            # Call the backend processor
            processor = PdfCompressor()
            compressed_pdf = processor.process_pdf(
                pdf_path=self.pdf_path,
                output_format='pdf', 
                quality=self.quality
            )
            
            # Save the result
            processor.save_output(compressed_pdf, self.output_path)
            
            self.finished.emit(self.output_path)
        except Exception as e:
            self.error.emit(str(e))

class PDFView(QWidget):
    compression_complete = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.pdf_path = None
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
        
        # Title frame
        title_frame = QFrame()
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)
        
        self.title = QLabel("PDF Compression")
        title_layout.addWidget(self.title)
        
        self.desc = QLabel("Reduce PDF file size while preserving text and image quality")
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
        
        # Compression level
        comp_level_frame = QFrame()
        comp_level_layout = QVBoxLayout(comp_level_frame)
        comp_level_layout.setContentsMargins(0, 0, 0, 0)
        comp_level_layout.setSpacing(5)
        
        self.comp_level_label = QLabel("Compression Level:")
        comp_level_layout.addWidget(self.comp_level_label)
        
        self.comp_slider = CompressionSlider()
        comp_level_layout.addWidget(self.comp_slider)
        
        # Slider labels
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
        
        layout.addWidget(options_frame)
        layout.addStretch()
        
        # Action buttons
        btn_frame = QFrame()
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(15)
        
        self.compress_btn = QPushButton("Compress PDF")
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
        self.compress_btn.clicked.connect(self.process_pdf)
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
        self.pdf_path = file_path
        self.compress_btn.setEnabled(True)
        
    def process_pdf(self):
        """Process the PDF with the selected settings"""
        if not self.pdf_path:
            return
            
        # Show loader
        trigger_loader('show', self, "Compressing PDF...")
        
        # Disable UI controls during compression
        self.compress_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)
        
        try:
            # Get all the parameters from the UI
            quality = self.comp_slider.value()
            
            # Get output path
            output_path = self.get_output_path()
            
            # Create and start worker thread
            self.compression_worker = PDFCompressionWorker(
                self.pdf_path, quality, output_path
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
        show_success_message("PDF compression successful!", f"Compressed PDF saved to:\n{output_path}")
        
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
        show_error_message(error_message, "PDF compression failed")
        
        # Clean up worker
        if self.compression_worker:
            self.compression_worker.deleteLater()
            self.compression_worker = None
            
    def get_output_path(self):
        """Generate output path based on input path"""
        base, ext = os.path.splitext(self.pdf_path)
        return f"{base}_compressed.pdf"
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Hide loader if visible
        trigger_loader('hide')
        
        # Stop worker thread if running
        if self.compression_worker and self.compression_worker.isRunning():
            self.compression_worker.terminate()
            self.compression_worker.wait()
        
        super().closeEvent(event)