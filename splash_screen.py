import os
import sys
from PyQt6.QtWidgets import (
    QSplashScreen, QProgressBar, QVBoxLayout, QWidget, QApplication,
    QGraphicsOpacityEffect
)
from PyQt6.QtGui import QPixmap, QColor, QFont, QPainter
# Re-added pyqtSignal
from PyQt6.QtCore import Qt, QTimer, QRect, QPropertyAnimation, QEasingCurve, pyqtSignal


class SplashScreen(QSplashScreen):
    # New signal to indicate when splash screen is truly done (progress 100% + faded out)
    progress_complete_and_faded_out = pyqtSignal()

    def __init__(self, pixmap=None, version="1.0.0"):
        if pixmap and not pixmap.isNull():
            # Scale pixmap to fit better, maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(
                600, 400, Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            super().__init__(scaled_pixmap, Qt.WindowType.WindowStaysOnTopHint)
        else:
            # Create a blank pixmap if none provided or invalid
            blank_pixmap = QPixmap(600, 400)
            blank_pixmap.fill(Qt.GlobalColor.white)
            super().__init__(blank_pixmap, Qt.WindowType.WindowStaysOnTopHint)

        self.version = version
        # Set window flags for frameless and always-on-top behavior
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint |
                            Qt.WindowType.FramelessWindowHint)
        self.setEnabled(False)  # Disable interaction with splash screen

        self.setup_ui()
        self.setup_fade_effect()

    def setup_ui(self):
        # Main container for splash screen content
        self.container = QWidget(self)
        self.container.setGeometry(self.rect())

        layout = QVBoxLayout(self.container)
        # Right and bottom margin for progress bar/version
        layout.setContentsMargins(0, 0, 20, 20)
        layout.setSpacing(0)
        # Removed layout.setAlignment - addStretch will handle alignment

        # Progress bar - Restored original styles
        # Pass self.container as parent
        self.progress = QProgressBar(self.container)
        self.progress.setRange(0, 100)  # Ensure range is set
        self.progress.setTextVisible(False)  # Hide text inside progress bar
        # Fixed height for the progress bar - Restored original
        self.progress.setFixedHeight(6)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid rgba(255, 255, 255, 30); /* Original style */
                border-radius: 3px;
                background-color: rgba(0, 0, 0, 20); /* Original style */
            }
            QProgressBar::chunk {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255, 255, 255, 150),
                    stop:1 rgba(200, 200, 255, 200)
                ); /* Original style */
                border-radius: 2px;
            }
        """)

        layout.addStretch()  # Push the progress bar to the bottom
        layout.addWidget(self.progress)

        self.progress_value = 0  # Initial progress value

        # Timer for progress bar animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)

        # Show version message using QSplashScreen's built-in functionality - Restored original
        self.setFont(QFont("Arial", 8, QFont.Weight.Bold))
        self.showMessage(
            f"Version {self.version}",
            alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom,
            color=QColor(255, 255, 255, 180)  # Semi-transparent white
        )

    def setup_fade_effect(self):
        # Opacity effect for fade-in/fade-out
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        # Animation for opacity
        self.fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_anim.setDuration(800)  # Duration for fade animation
        self.fade_anim.setEasingCurve(
            QEasingCurve.Type.InOutQuad)  # Smooth easing curve
        # Connect the fade animation's finished signal to our handler
        self.fade_anim.finished.connect(self._on_fade_finished)

    def fade_in(self):
        # Set start and end values for fade-in
        self.opacity_effect.setOpacity(0.0)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.start()

    def fade_out(self):
        # Starts the fade-out animation.
        self.fade_anim.setStartValue(1.0)
        self.fade_anim.setEndValue(0.0)
        self.fade_anim.start()

    def start_animation(self, duration=2500):
        """Starts the progress bar and fade-in animation."""
        self.progress_value = 0
        self.progress.setValue(0)
        interval = duration // 100
        self.timer.start(interval)
        self.fade_in()  # Starts fade-in when animation begins.

    def update_progress(self):
        """Updates the progress bar and triggers fade-out when complete."""
        if self.progress_value < 100:
            self.progress_value += 1
            self.progress.setValue(self.progress_value)
        else:
            self.timer.stop()  # Stop progress timer
            self.fade_out()  # Trigger the fade-out as progress completes.

    def _on_fade_finished(self):
        """Handler for when the fade animation finishes."""
        # Only emit finished signal and hide if it was a fade-out animation (opacity reached 0)
        if self.opacity_effect.opacity() == 0.0:
            self.hide()  # Hide the splash screen
            self.progress_complete_and_faded_out.emit()  # Emit the signal to main.py

    def show_centered(self):
        """Centers the splash screen on the primary screen."""
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        splash_geometry = self.frameGeometry()
        splash_geometry.moveCenter(screen_geometry.center())
        self.move(splash_geometry.topLeft())
        self.show()

    def drawContents(self, painter):
        # Restored original drawContents for shadow and pixmap drawing
        shadow_rect = QRect(5, 5, self.width()-10, self.height()-10)
        painter.fillRect(shadow_rect, QColor(0, 0, 0, 30)
                         )  # Translucent black shadow

        main_rect = QRect(0, 0, self.width()-5, self.height()-5)
        painter.drawPixmap(main_rect, self.pixmap())  # Draw the scaled pixmap

        # Crucial for displaying showMessage text and other QWidget content
        super().drawContents(painter)