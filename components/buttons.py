from PySide6.QtWidgets import QPushButton, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from icons.icons import IconLabel

class NavButton(QPushButton):
    def __init__(self, text, icon_type=None, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(12)
        
        if icon_type:
            self.icon = IconLabel(icon_type, 18)
            layout.addWidget(self.icon)
        
        self.label = QLabel(text)
        self.label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #4b5563;
                font-weight: 500;
            }
        """)
        layout.addWidget(self.label)
        layout.addStretch()
        
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                text-align: left;
                padding: 0px;
                border-radius: 8px;
                margin: 2px 0px;
            }
            QPushButton:hover {
                background-color: rgba(16, 185, 129, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(16, 185, 129, 0.15);
            }
        """)
        
        self.setFixedHeight(48)
    
    def set_active(self, active=True):
        if active:
            self.setStyleSheet("""
                QPushButton {
                    background-color: rgba(16, 185, 129, 0.1);
                    border: none;
                    text-align: left;
                    padding: 0px;
                    border-radius: 8px;
                    margin: 2px 0px;
                    border-left: 3px solid #10b981;
                }
                QPushButton:hover {
                    background-color: rgba(16, 185, 129, 0.15);
                }
            """)
            self.label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #10b981;
                    font-weight: 600;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    text-align: left;
                    padding: 0px;
                    border-radius: 8px;
                    margin: 2px 0px;
                }
                QPushButton:hover {
                    background-color: rgba(16, 185, 129, 0.1);
                }
                QPushButton:pressed {
                    background-color: rgba(16, 185, 129, 0.15);
                }
            """)
            self.label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #4b5563;
                    font-weight: 500;
                }
            """)