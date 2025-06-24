# down_allocation_app/main.py
import os
import sys
from PyQt6.QtWidgets import QApplication, QSplashScreen
from PyQt6.QtGui import QPixmap, QFont
# Ensure pyqtSignal is imported for clarity
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, pyqtSignal

from splash_screen import SplashScreen
from ui.main_window import DownAllocationApp

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    splash_path = os.path.join(os.path.dirname( 
        __file__), 'assets', 'splash_image.png')
    if not os.path.exists(splash_path):
        print(
            f"Warning: Splash image not found at {splash_path}. Using blank pixmap.")
        pixmap = QPixmap(600, 400)
        pixmap.fill(Qt.GlobalColor.white)
    else:
        pixmap = QPixmap(os.path.abspath(splash_path))

    splash = SplashScreen(pixmap, version="1.0.0")
    splash.show_centered()

    global main_window  # Declare global to keep main_window alive

    # This function will be called when the splash screen has completed its progress and faded out.
    def _create_and_show_main_app():
        global main_window
        # Now that the splash screen is guaranteed to be hidden,
        # we can safely instantiate the main application.
        main_window = DownAllocationApp()
        main_window.showMaximized()

        # Finally, delete the splash screen object now that the main window is visible.
        splash.deleteLater()

    # Connect the splash screen's signal to our main app creation function.
    # The splash screen will emit this signal only after its progress bar is 100% and it has faded out.
    splash.progress_complete_and_faded_out.connect(_create_and_show_main_app)

    # Start the splash screen's animation (progress bar fills and then fade-in occurs simultaneously).
    # The fade-out will be triggered internally by the splash screen when progress is complete.
    # Use a duration that allows progress bar to complete visually
    splash.start_animation(duration=2500)

    sys.exit(app.exec())
