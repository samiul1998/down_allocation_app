# down_allocation_app/ui/menu_bar/help_menu.py

from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, pyqtSignal

class HelpMenu(QMenu):
    # Signals for help and about dialogs
    help_requested = pyqtSignal()
    about_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__("&Help", parent)
        self._create_actions()

    def _create_actions(self):
        """Creates the QActions for the Help menu."""

        # Help Action
        self.help_action = QAction("Help", self)
        self.help_action.setShortcut("F1")
        self.help_action.setStatusTip("Opens a help dialog or user guide")
        self.help_action.triggered.connect(self.help_requested.emit)
        self.addAction(self.help_action)

        # About Action
        self.about_action = QAction("About", self)
        self.about_action.setStatusTip("Shows app version, credits, and purpose")
        self.about_action.triggered.connect(self.about_requested.emit)
        self.addAction(self.about_action)
