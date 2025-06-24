# down_allocation_app/ui/dialogs/confirmation_dialog.py

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QPushButton
from PyQt6.QtCore import Qt
from styles import AppStyles # Assuming styles.py is in the parent directory or accessible

class ConfirmationDialog(QDialog):
    def __init__(self, title="Confirm Action", message="Are you sure you want to proceed?", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(400, 200)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowCloseButtonHint)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Message label
        self.label = QLabel(message)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet(AppStyles.CONFIRMATION_LABEL_STYLE)
        layout.addWidget(self.label)
        
        # Button box
        button_box = QDialogButtonBox()
        button_box.setCenterButtons(True)
        
        self.yes_btn = button_box.addButton("Yes", QDialogButtonBox.ButtonRole.AcceptRole)
        self.no_btn = button_box.addButton("No", QDialogButtonBox.ButtonRole.RejectRole)
        
        # Connect buttons
        self.yes_btn.clicked.connect(self.accept)
        self.no_btn.clicked.connect(self.reject)
        
        # Styling for buttons
        button_box.setStyleSheet(AppStyles.CONFIRMATION_BUTTON_STYLE)
        
        layout.addWidget(button_box)
        
        # Dialog styling
        self.setStyleSheet(AppStyles.CONFIRMATION_DIALOG_STYLE)