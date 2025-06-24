# down_allocation_app/ui/dialogs/help_dialog.py

from PyQt6.QtWidgets import QMessageBox, QDialog
from PyQt6.QtCore import Qt

class HelpDialog(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Help")
        self.setTextFormat(Qt.TextFormat.RichText) # Enable HTML formatting
        self.setIcon(QMessageBox.Icon.Information)

        self.setText(
            "<h3>Help for Automatic Down Allocation System</h3>"
            "<p><b>Factory Information:</b> Click 'Edit' to set up your factory name and location. This information will be saved.</p>"
            "<p><b>Input Fields:</b> Fill in the details for Date, Buyer, Style, Season, Garments Stage, Base Size, Ecodown Weight, Garments Weight, and Approximate Weight.</p>"
            "<p><b>Panel | Size Table:</b></p>"
            "<ul>"
            "<li>Enter Panel Names in the first column and Panel Quantity in the second.</li>"
            "<li>Enter sewing area values for each size.</li>"
            "<li>Use <b>Ctrl+C</b> to copy and <b>Ctrl+V</b> to paste data.</li>"
            "<li><b>Ctrl+Z</b> to Undo, <b>Ctrl+Y</b> or <b>Ctrl+Shift+Z</b> to Redo.</li>"
            "<li>Right-click on the table for options like Insert/Delete Row/Column.</li>"
            "</ul>"
            "<p><b>SET PANEL | SIZE:</b> Adjusts the number of rows and size columns in the table.</p>"
            "<p><b>RESET ALL FIELDS:</b> Clears all input fields and table data.</p>"
            "<p><b>EXPORT TO EXCEL:</b> Exports all input and table data to an Excel file.</p>"
            "<p><b>About/Help:</b> Provides information about the application and this help guide.</p>"
        )
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.setFixedSize(600, 450) # Set a fixed size for consistency
