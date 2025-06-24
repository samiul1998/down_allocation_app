# down_allocation_app/ui/sections/factory_info.py

from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt, pyqtSignal
# Assuming styles.py is in the parent directory or accessible
from styles import AppStyles


class FactoryInfoSection(QFrame):
    # Removed edit_factory_requested signal as the action is now in the menu bar.
    # edit_factory_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # Removed the AppStyles.SECTION_FRAME_STYLE here to remove the border - Issue 1
        # Fixed height, expanding width
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Fixed)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 5, 10, 5)  # Smaller margins
        main_layout.setSpacing(AppStyles.HORIZONTAL_SPACING)

        # Left side: Factory Name and Location
        info_layout = QVBoxLayout()
        # Closer spacing for info lines
        info_layout.setSpacing(AppStyles.VERTICAL_SPACING // 2)

        self.factory_name_label = QLabel("Factory Name: N/A")
        self.factory_name_label.setFont(
            QFont("Courier New", AppStyles.FACTORY_FONT_SIZE, QFont.Weight.Bold))
        # Ensure plain text with no border or special background
        self.factory_name_label.setStyleSheet(
            "color: #333333; border: none; background-color: transparent;")
        info_layout.addWidget(self.factory_name_label)

        self.factory_location_label = QLabel("Location: N/A")
        self.factory_location_label.setFont(
            QFont("Courier New", AppStyles.FACTORY_FONT_SIZE))
        # Ensure plain text with no border or special background
        self.factory_location_label.setStyleSheet(
            "color: #555555; border: none; background-color: transparent;")
        info_layout.addWidget(self.factory_location_label)

        main_layout.addLayout(info_layout)
        main_layout.addStretch(1)  # Pushes content to the left

        # Removed the "Edit Factory Info" button as it's moved to the menu bar.
        # The space where the button was is now filled by the stretch.

    def update_factory_display(self, name, location):
        self.factory_name_label.setText(f"Factory Name: {name}")
        self.factory_location_label.setText(f"Location: {location}")