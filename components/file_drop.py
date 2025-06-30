from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QFileDialog, QHBoxLayout
from PySide6.QtCore import Qt, Signal
from components.message import show_error_message
from icons.icons import IconLabel
import os

class FileDropArea(QFrame):
    files_dropped = Signal(str)
    
    def __init__(self, title, description, file_type, parent=None):
        super().__init__(parent)
        self.file_type = file_type.lower()
        self.original_title = title
        self.original_description = description
        self.selected_file = None
        self.setAcceptDrops(True)
        self.setFrameShape(QFrame.StyledPanel)

        self.default_style = """
            FileDropArea {
                background-color: #f9fafb;
                border: 2px dashed #d1d5db;
                border-radius: 12px;
            }
        """
        self.hover_style = """
            FileDropArea {
                border: 2px dashed #10b981;
                background-color: #f0fdf4;
            }
        """
        self.selected_style = """
            FileDropArea {
                background-color: #f0f9ff;
                border: 2px solid #0ea5e9;
                border-radius: 12px;
            }
        """
        self.setStyleSheet(self.default_style)
        self.setup_ui()

    def setup_ui(self):
        """Setup the UI - will be updated when file is selected"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        # Use consistent margins and spacing for both states
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        
        self.show_initial_state()

    def show_initial_state(self):
        """Show the initial drop area state"""
        self.clear_layout()
        # Keep consistent margins and spacing
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(15)

        # Icon - reduced size to match the selected state better
        self.icon_label = IconLabel("upload", 48)
        self.main_layout.addWidget(self.icon_label, 0, Qt.AlignCenter)

        # Title - reduced font size
        self.title_label = QLabel(self.original_title)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 600;
                color: #1f2937;
                margin: 0px;
            }
        """)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        # Description
        self.desc_label = QLabel(self.original_description)
        self.desc_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #6b7280;
                margin: 0px;
            }
        """)
        self.desc_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.desc_label)

        # Browse button - reduced padding to match selected state buttons
        self.browse_btn = QPushButton("Browse Files")
        self.browse_btn.setCursor(Qt.PointingHandCursor)
        self.browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        self.browse_btn.clicked.connect(self.open_file_dialog)
        
        # Add button in a container with top margin to match selected state
        button_frame = QFrame()
        button_frame.setStyleSheet("""
            QFrame {
                background-color: transparent;  
            }
        """)
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(0, 10, 0, 0)
        button_layout.addWidget(self.browse_btn, 0, Qt.AlignCenter)
        
        self.main_layout.addWidget(button_frame, 0, Qt.AlignCenter)

    def show_selected_state(self):
        """Show the selected file state"""
        self.clear_layout()
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(15)

        # File icon
        success_label = IconLabel(icon_type="success_tick", size=48)
        self.main_layout.addWidget(success_label, 0, Qt.AlignCenter)

        # File name
        file_name = os.path.basename(self.selected_file) if self.selected_file else "Unknown file"
        file_name_label = QLabel(file_name)
        file_name_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 600;
                color: #0ea5e9;
                margin: 0px;
                background-color: transparent;
            }
        """)
        file_name_label.setAlignment(Qt.AlignCenter)
        file_name_label.setWordWrap(True)  # Allow long filenames to wrap
        self.main_layout.addWidget(file_name_label)

        # Status
        status_label = QLabel("File Selected")
        status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #059669;
                font-weight: 500;
                margin: 0px;
                background-color: transparent;
            }
        """)
        status_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(status_label)

        # Buttons
        button_frame = QFrame()
        button_frame.setStyleSheet("""
            QFrame {
                background-color: transparent;  
            }
        """)
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(0, 10, 0, 0)
        button_layout.setSpacing(10)

        # Change button
        change_btn = QPushButton("Change File")
        change_btn.setCursor(Qt.PointingHandCursor)
        change_btn.setStyleSheet("""
            QPushButton {
                background-color: #78a0f0;
                color: #ffffff;
                border: 1px solid #78a0f0;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #4463a1;
                border: 1px solid #4463a1;
                color: #ffffff;
            }
        """)
        change_btn.clicked.connect(self.open_file_dialog)
        button_layout.addWidget(change_btn)

        # Remove button
        remove_btn = QPushButton("Remove")
        remove_btn.setCursor(Qt.PointingHandCursor)
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                color: #ffffff;
                border: 1px solid #dc2626;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #fecaca;
                border: 1px solid #fecaca;
                color: #ffffff;
            }
        """)
        remove_btn.clicked.connect(self.remove_file)
        button_layout.addWidget(remove_btn)

        self.main_layout.addWidget(button_frame, 0, Qt.AlignCenter)

    def clear_layout(self):
        """Clear all widgets from the layout"""
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet(self.hover_style)

    def dragLeaveEvent(self, event):
        if self.selected_file:
            self.setStyleSheet(self.selected_style)
        else:
            self.setStyleSheet(self.default_style)

    def dropEvent(self, event):
        """Handle dropped files"""
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.handle_file_selection(file_path)

    def open_file_dialog(self):
        """Open file dialog"""
        if self.file_type == 'pdf':
            file_filter = "PDF Files (*.pdf)"
        elif self.file_type == 'image':
            file_filter = "Image Files (*.jpg *.jpeg *.png)"
        else:
            file_filter = "All Files (*)"
            
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", file_filter)
        if file_path:
            self.handle_file_selection(file_path)

    def handle_file_selection(self, file_path):
        """Handle file selection"""
        ext = os.path.splitext(file_path)[1].lower()
        
        if self.file_type == 'pdf' and ext != '.pdf':
            show_error_message("Only PDF files are allowed.", "Invalid File")
            return
        elif self.file_type == 'image' and ext not in ['.jpg', '.jpeg', '.png']:
            show_error_message("Only JPG and PNG image files are allowed.", "Invalid File")
            return
        
        # Update state
        self.selected_file = file_path
        self.show_selected_state()
        self.setStyleSheet(self.selected_style)
        
        # Emit signal
        self.files_dropped.emit(file_path)

    def remove_file(self):
        """Remove selected file"""
        self.selected_file = None
        self.show_initial_state()
        self.setStyleSheet(self.default_style)

    def get_selected_file(self):
        return self.selected_file

    def has_file(self):
        return self.selected_file is not None