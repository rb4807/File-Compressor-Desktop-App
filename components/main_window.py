from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QFrame
from pages.home import HomeView
from pages.image import ImageView
from pages.pdf import PDFView
from pages.img_to_pdf import ImgToPDFView
from pages.pdf_to_img import PDFToImgView
from components.sidebar import Sidebar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Compressor Pro")
        self.setMinimumSize(1500, 500)
        self.setStyleSheet("QMainWindow { background-color: #ffffff; }")
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Main content area
        self.content_area = QFrame()
        self.content_area.setStyleSheet("background-color: #f9fafb;")
        
        content_layout = QVBoxLayout(self.content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Stacked widget for different views
        self.stacked_widget = QStackedWidget()
        
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
        main_layout.addWidget(self.content_area)
        
        # Connect navigation
        self.sidebar.nav_buttons[0].clicked.connect(lambda: self.switch_view(0))
        self.sidebar.nav_buttons[1].clicked.connect(lambda: self.switch_view(1))
        self.sidebar.nav_buttons[2].clicked.connect(lambda: self.switch_view(2))
        self.sidebar.nav_buttons[3].clicked.connect(lambda: self.switch_view(3))
        # self.sidebar.nav_buttons[4].clicked.connect(lambda: self.switch_view(4))
        
        # Set initial view
        self.switch_view(0)
    
    def switch_view(self, index):
        self.stacked_widget.setCurrentIndex(index)
        self.sidebar.set_active_button(index)