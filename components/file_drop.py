from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QFileDialog, QHBoxLayout
from PySide6.QtCore import Qt, Signal
from components.message import show_error_message
from icons.icons import IconLabel
import os
from theme.theme import get_current_theme, theme_manager, get_app_primary_color, get_app_primary_hover_color

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

        # Connect to theme manager
        theme_manager.theme_changed.connect(self.update_styles)
        
        # Initialize styles
        self.update_styles()
        self.setup_ui()

    def update_styles(self):
        """Update all styles based on current theme"""
        theme = get_current_theme()
        primary_color = get_app_primary_color()
        primary_hover = get_app_primary_hover_color()
        
        self.default_style = f"""
            FileDropArea {{
                background-color: {theme.SURFACE_BG};
                border: 2px dashed {theme.BORDER_SECONDARY};
                border-radius: 12px;
            }}
        """
        self.hover_style = f"""
            FileDropArea {{
                border: 2px dashed {primary_color};
                background-color: {theme.APP_BG};
            }}
        """
        self.selected_style = f"""
            FileDropArea {{
                background-color: {theme.APP_BG};
                border: 2px solid {primary_color};
                border-radius: 12px;
            }}
        """
        
        # Apply current style
        if self.selected_file:
            self.setStyleSheet(self.selected_style)
        else:
            self.setStyleSheet(self.default_style)
        
        # Update label styles if they exist
        if hasattr(self, 'title_label'):
            self.title_label.setStyleSheet(f"""
                QLabel {{
                    font-size: 18px;
                    font-weight: 600;
                    color: {theme.TEXT_PRIMARY};
                    margin: 0px;
                    background: transparent;
                }}
            """)
        
        if hasattr(self, 'desc_label'):
            self.desc_label.setStyleSheet(f"""
                QLabel {{
                    font-size: 14px;
                    color: {theme.TEXT_MUTED};
                    margin: 0px;
                    background: transparent;
                }}
            """)

    def setup_ui(self):
        """Setup the UI - will be updated when file is selected"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        
        self.show_initial_state()

    def show_initial_state(self):
        """Show the initial drop area state"""
        self.clear_layout()
        theme = get_current_theme()
        primary_color = get_app_primary_color()
        primary_hover = get_app_primary_hover_color()
        
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(15)

        # Icon
        self.icon_label = IconLabel("upload", 48)
        self.icon_label.setStyleSheet(f"background: transparent; color: {theme.TEXT_PRIMARY};")
        self.main_layout.addWidget(self.icon_label, 0, Qt.AlignCenter)

        # Title
        self.title_label = QLabel(self.original_title)
        self.title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: 600;
                color: {theme.TEXT_PRIMARY};
                margin: 0px;
                background: transparent;
            }}
        """)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        # Description
        self.desc_label = QLabel(self.original_description)
        self.desc_label.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                color: {theme.TEXT_MUTED};
                margin: 0px;
                background: transparent;
            }}
        """)
        self.desc_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.desc_label)

        # Browse button
        self.browse_btn = QPushButton("Browse Files")
        self.browse_btn.setCursor(Qt.PointingHandCursor)
        self.browse_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {primary_color};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {primary_hover};
            }}
        """)
        self.browse_btn.clicked.connect(self.open_file_dialog)
        
        # Add button in a container
        button_frame = QFrame()
        button_frame.setStyleSheet("background-color: transparent;")
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(0, 10, 0, 0)
        button_layout.addWidget(self.browse_btn, 0, Qt.AlignCenter)
        
        self.main_layout.addWidget(button_frame, 0, Qt.AlignCenter)

    def show_selected_state(self):
        """Show the selected file state"""
        self.clear_layout()
        theme = get_current_theme()
        primary_color = get_app_primary_color()
        
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(15)

        # File icon
        success_label = IconLabel(icon_type="success_tick", size=48)
        success_label.setStyleSheet(f"background: transparent; color: {primary_color};")
        self.main_layout.addWidget(success_label, 0, Qt.AlignCenter)

        # File name
        file_name = os.path.basename(self.selected_file) if self.selected_file else "Unknown file"
        file_name_label = QLabel(file_name)
        file_name_label.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: 600;
                color: {primary_color};
                margin: 0px;
                background-color: transparent;
            }}
        """)
        file_name_label.setAlignment(Qt.AlignCenter)
        file_name_label.setWordWrap(True)
        self.main_layout.addWidget(file_name_label)

        # Status
        status_label = QLabel("File Selected")
        status_label.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                color: {primary_color};
                font-weight: 500;
                margin: 0px;
                background-color: transparent;
            }}
        """)
        status_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(status_label)

        # Buttons
        button_frame = QFrame()
        button_frame.setStyleSheet("background-color: transparent;")
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(0, 10, 0, 0)
        button_layout.setSpacing(10)

        # Change button
        change_btn = QPushButton("Change File")
        change_btn.setCursor(Qt.PointingHandCursor)
        change_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme.SURFACE_BG};
                color: {theme.TEXT_PRIMARY};
                border: 1px solid {theme.BORDER_SECONDARY};
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {theme.APP_BG};
                border: 1px solid {primary_color};
            }}
        """)
        change_btn.clicked.connect(self.open_file_dialog)
        button_layout.addWidget(change_btn)

        # Remove button
        remove_btn = QPushButton("Remove")
        remove_btn.setCursor(Qt.PointingHandCursor)
        remove_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme.SURFACE_BG};
                color: #dc2626;
                border: 1px solid #dc2626;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: #fee2e2;
                border: 1px solid #fee2e2;
            }}
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