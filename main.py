import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from components.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    
    flags = window.windowFlags()
    flags &= ~Qt.WindowMinimizeButtonHint  # Disable maximize
    flags &= ~Qt.WindowMaximizeButtonHint  # Disable maximize
    flags |= Qt.WindowCloseButtonHint      # Ensure close is enabled
    window.setWindowFlags(flags)
    window.showMaximized()
    
    sys.exit(app.exec())