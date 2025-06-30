from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QFrame
from pages.home import HomeView
from pages.image import ImageView
from pages.pdf import PDFView
from pages.img_to_pdf import ImgToPDFView
from pages.pdf_to_img import PDFToImgView
from components.sidebar import Sidebar
from theme.theme import theme_manager, get_current_theme

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Make It Tiny")
        self.setMinimumSize(1500, 500)
        
        # Connect to global theme manager
        theme_manager.theme_changed.connect(self.on_theme_changed)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Create sidebar
        self.sidebar = Sidebar()
        self.main_layout.addWidget(self.sidebar)
        
        # Main content area - removed border styling
        self.content_area = QFrame()
        self.content_area.setFrameStyle(QFrame.NoFrame)  # Remove frame
        content_layout = QVBoxLayout(self.content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Stacked widget for different views
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setContentsMargins(0, 0, 0, 0)
        
        # Create views
        self.views = [
            HomeView(self),
            ImageView(),
            PDFView(),
            PDFToImgView(),
            # ImgToPDFView()
        ]
        
        for view in self.views:
            self.stacked_widget.addWidget(view)
        
        content_layout.addWidget(self.stacked_widget)
        self.main_layout.addWidget(self.content_area)
        
        # Connect navigation
        self.sidebar.nav_buttons[0].clicked.connect(lambda: self.switch_view(0))
        self.sidebar.nav_buttons[1].clicked.connect(lambda: self.switch_view(1))
        self.sidebar.nav_buttons[2].clicked.connect(lambda: self.switch_view(2))
        self.sidebar.nav_buttons[3].clicked.connect(lambda: self.switch_view(3))
        # self.sidebar.nav_buttons[4].clicked.connect(lambda: self.switch_view(4))
        
        # Apply initial theme
        self.apply_theme()
        
        # Set initial view
        self.switch_view(0)
    
    def on_theme_changed(self, is_dark_mode):
        """Handle theme changes from the theme manager"""
        self.apply_theme()
        
        # Notify all views about theme change
        for view in self.views:
            if hasattr(view, 'on_theme_changed'):
                view.on_theme_changed(is_dark_mode)
    
    def apply_theme(self):
        """Apply the current theme to the main window"""
        theme = get_current_theme()
        
        # Main window styles - clean without borders
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {theme.APP_BG};
                border: none;
            }}
        """)
        
        # Content area styles - removed border
        self.content_area.setStyleSheet(f"""
            QFrame {{
                background-color: {theme.CONTENT_BG};
                border: none;
                margin: 0px;
                padding: 0px;
            }}
        """)
        
        # Clean stacked widget styling
        self.stacked_widget.setStyleSheet(f"""
            QStackedWidget {{
                background-color: {theme.CONTENT_BG};
                border: none;
                margin: 0px;
                padding: 0px;
            }}
        """)
    
    def switch_view(self, index):
        self.stacked_widget.setCurrentIndex(index)
        self.sidebar.set_active_button(index)