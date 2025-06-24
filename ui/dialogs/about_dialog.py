# down_allocation_app/ui/dialogs/about_dialog.py

from PyQt6.QtWidgets import QMessageBox, QDialog
from PyQt6.QtCore import Qt

class AboutDialog(QMessageBox):
    def __init__(self, parent=None, version="1.0.0"):
        super().__init__(parent)
        self.setWindowTitle("About Automatic Down Allocation System")
        self.setTextFormat(Qt.TextFormat.RichText) # Enable HTML formatting
        self.setIcon(QMessageBox.Icon.Information)

        self.setText(
            f"<h3>Automatic Down Allocation System v{version}</h3>"
            "<p>This application assists in calculating down allocation based on various inputs and panel/size data.</p>"
            "<p>Developed by: Your Name/Organization</p>"
            "<p>Contact: your.email@example.com</p>"
            "<p>2023-2024</p>"
        )
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.setFixedSize(450, 250) # Set a fixed size for consistency
