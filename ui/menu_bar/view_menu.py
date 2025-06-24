# down_allocation_app/ui/menu_bar/view_menu.py

from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, pyqtSignal

class ViewMenu(QMenu):
    # Signals for toggling visibility of UI sections
    toggle_factory_info_requested = pyqtSignal(bool)
    toggle_bottom_table_requested = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__("&View", parent)
        self._create_actions()

    def _create_actions(self):
        """Creates the QActions for the View menu."""

        # Factory Info Panel Toggle Action
        self.toggle_factory_info_action = QAction("Factory Info Panel", self, checkable=True)
        self.toggle_factory_info_action.setStatusTip("Toggles the visibility of the factory info section")
        self.toggle_factory_info_action.setChecked(True) # Default state from main_window.py
        self.toggle_factory_info_action.triggered.connect(self.toggle_factory_info_requested.emit)
        self.addAction(self.toggle_factory_info_action)

        # Bottom Table Panel Toggle Action
        self.toggle_bottom_table_action = QAction("Bottom Table Panel", self, checkable=True)
        self.toggle_bottom_table_action.setStatusTip("Toggles the visibility of the bottom summary table")
        self.toggle_bottom_table_action.setChecked(True) # Default state from main_window.py
        self.toggle_bottom_table_action.triggered.connect(self.toggle_bottom_table_requested.emit)
        self.addAction(self.toggle_bottom_table_action)
