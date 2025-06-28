from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QSlider, QHBoxLayout
from PySide6.QtCore import Qt

class CompressionSlider(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 0)  # Top margin for value display
        layout.setSpacing(5)
        
        # Main container for slider and labels
        container = QFrame()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(5)
        # Value display (always on top)
        self.value_display = QLabel("70%", self)
        self.value_display.setAlignment(Qt.AlignCenter)
        self.value_display.setFixedSize(40, 20)
        self.value_display.setStyleSheet("""
            QLabel {
                background-color: #009688;
                color: white;
                font-weight: bold;
                font-size: 11px;
                border-radius: 3px;
            }
        """)
        self.value_display.raise_()  # Ensure it's on top
        
        # Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 100)
        self.slider.setValue(70)
        self.slider.setStyleSheet("""
            QSlider {
                height: 20px;
            }
            QSlider::groove:horizontal {
                height: 4px;
                background: #e0e0e0;
                border-radius: 2px;
                margin: 0 10px;
            }
            QSlider::handle:horizontal {
                width: 14px;
                height: 14px;
                margin: -5px -8px;
                background: #009688;
                border-radius: 7px;
            }
            QSlider::sub-page:horizontal {
                background: #009688;
                border-radius: 2px;
            }
        """)
        container_layout.addWidget(self.slider)
        
        # Numeric labels (1 and 100)
        numeric_labels = QFrame()
        numeric_layout = QHBoxLayout(numeric_labels)
        numeric_layout.setContentsMargins(10, 0, 10, 0)
        
        min_label = QLabel("1")
        min_label.setStyleSheet("font-size: 12px; color: #666666;")
        numeric_layout.addWidget(min_label)
        
        numeric_layout.addStretch()
        
        max_label = QLabel("100")
        max_label.setStyleSheet("font-size: 12px; color: #666666;")
        numeric_layout.addWidget(max_label)
        
        container_layout.addWidget(numeric_labels)
        layout.addWidget(container)
        
        # Connect signals
        self.slider.valueChanged.connect(self.update_value_position)
        self.update_value_position(70)  # Initial position
        
    def update_value_position(self, value):
        """Update the position of the value display"""
        self.value_display.setText(f"{value}%")
        
        # Calculate handle position
        slider_width = self.slider.width()
        handle_pos = self.slider.style().sliderPositionFromValue(
            self.slider.minimum(),
            self.slider.maximum(),
            value,
            slider_width - 20  # Account for margins
        )
        
        # Get slider position relative to our widget
        slider_pos = self.slider.pos()
        
        # Position the value display centered above the handle
        x_pos = slider_pos.x() + handle_pos - (self.value_display.width() // 2) + 10
        y_pos = 0  # Top of the widget
        
        self.value_display.move(x_pos, y_pos)
        
    def value(self):
        return self.slider.value()
        
    def setValue(self, value):
        value = max(1, min(100, value))
        self.slider.setValue(value)
        self.update_value_position(value)