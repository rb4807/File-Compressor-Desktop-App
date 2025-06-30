from PySide6.QtWidgets import QMessageBox

def show_success_message(text, informative_text):
    """Show success message when compression is complete"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(text)
    msg.setInformativeText(informative_text)
    msg.setWindowTitle("Success")
    msg.exec_()
        
def show_error_message(error, text):
    """Show error message when compression fails"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(text)
    msg.setInformativeText(error)
    msg.setWindowTitle("Error")
    msg.exec_()