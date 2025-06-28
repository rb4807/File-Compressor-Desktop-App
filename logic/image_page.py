from pathlib import Path
from PySide6.QtCore import Signal, QObject
from core.ImageCompressor.ImageCompressor import ImageCompressor

class ImageCompressionLogic(QObject):
    compression_complete = Signal(str)
    status_update = Signal(str, str)  # message, color
    
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.image_path = None
        self.setup_connections()
        
    def setup_connections(self):
        """Connect signals and slots"""
        self.ui.drop_area.files_dropped.connect(self.handle_files_dropped)
        self.ui.compress_btn.clicked.connect(self.compress_image)
        self.ui.cancel_btn.clicked.connect(self.reset_ui)
        
    def handle_files_dropped(self, file_paths):
        """Handle dropped files or files selected via browse"""
        if file_paths:
            self.image_path = file_paths[0]  # Take first file if multiple
            self.ui.compress_btn.setEnabled(True)
            self.status_update.emit(f"Selected: {Path(self.image_path).name}", "#009688")
            
    def compress_image(self):
        """Compress the selected image with the given parameters"""
        if not self.image_path:
            self.status_update.emit("No image selected!", "#f44336")
            return
            
        try:
            # Get output format
            output_format = 'jpg' if self.ui.jpg_btn.isChecked() else 'png'
            
            # Get quality from slider (convert from 0-100 to 1-100)
            quality = self.ui.comp_slider.value()
            
            # Get resize dimensions
            try:
                width = int(self.ui.width_input.text()) if self.ui.width_input.text() else None
                height = int(self.ui.height_input.text()) if self.ui.height_input.text() else None
                resize = (width, height) if width and height else None
            except ValueError:
                resize = None
                self.status_update.emit("Invalid dimensions - using original size", "#ff9800")
                
            # Static colors value
            colors = 128
            
            # Process the image
            processor = ImageCompressor(image_path=self.image_path)
            processed_data = processor.process_image(
                output_format=output_format,
                quality=quality,
                resize=resize,
                colors=colors
            )
            
            # Save the result with appropriate extension
            output_path = Path(self.image_path).with_name(
                f"{Path(self.image_path).stem}_compressed.{output_format}"
            )
            
            with open(output_path, 'wb') as f:
                f.write(processed_data)
                
            self.status_update.emit(f"Compression complete! Saved to: {output_path.name}", "#4caf50")
            
        except Exception as e:
            self.status_update.emit(f"Error: {str(e)}", "#f44336")
            
    def reset_ui(self):
        """Reset the UI to initial state"""
        self.image_path = None
        self.ui.compress_btn.setEnabled(False)
        self.ui.comp_slider.setValue(70)  # Reset to default quality
        self.ui.width_input.setText("800")
        self.ui.height_input.setText("600")
        self.ui.jpg_btn.setChecked(True)
        self.status_update.emit("", "")