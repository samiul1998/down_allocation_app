# down_allocation_app/ui/dialogs/progress_dialog.py

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QApplication
from PyQt6.QtCore import Qt, QTimer
from styles import AppStyles # Assuming styles.py is in the parent directory or accessible

class ProgressDialog(QDialog):
    def __init__(self, title="Processing", message="Please wait...", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(300, 100)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.label = QLabel(message)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(True)
        self.progress.setStyleSheet(AppStyles.PROGRESS_BAR_STYLE)
        layout.addWidget(self.progress)
        
        # Timer for smooth progress animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.increment_progress)
        self.current_progress = 0
        self.target_progress = 0
        self.step = 1
        
    def increment_progress(self):
        if self.current_progress < self.target_progress:
            self.current_progress += self.step
            self.progress.setValue(self.current_progress)
            QApplication.processEvents()
        else:
            self.timer.stop()
            if self.current_progress >= 100:
                self.close()
    
    def update_progress(self, value):
        self.target_progress = value
        self.step = max(1, (self.target_progress - self.current_progress) // 10)
        self.timer.start(30)  # Update every 30ms for smooth animation
    
    def closeEvent(self, event):
        self.timer.stop()
        super().closeEvent(event)