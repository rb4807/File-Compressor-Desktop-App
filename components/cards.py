from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsDropShadowEffect
from icons.icons import IconLabel

class CompressionCard(QFrame):
    def __init__(self, title, description, icon_type=None, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            CompressionCard {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e5e7eb;
            }
            CompressionCard:hover {
                border: 1px solid #10b981;
                background-color: #f9fafb;
            }
        """)
        self.setCursor(Qt.PointingHandCursor)
        
        # Enhanced shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        layout.setAlignment(Qt.AlignCenter)
        
        if icon_type:
            icon_label = IconLabel(icon_type, 48)
            layout.addWidget(icon_label, 0, Qt.AlignCenter)
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 600;
                color: #1f2937;
                margin: 0px;
                background: transparent;                      
            }
        """)
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)
        
        self.desc_label = QLabel(description)
        self.desc_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #6b7280;
                text-align: center;
                line-height: 1.4;
                margin: 0px;
                background: transparent;
            }
        """)
        self.desc_label.setWordWrap(True)
        layout.addWidget(self.desc_label)
        
        self.setFixedSize(240, 220)