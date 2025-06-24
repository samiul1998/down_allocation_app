# down_allocation_app/ui/menu_bar/edit_menu.py

from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, pyqtSignal

class EditMenu(QMenu):
    # Define signals for each menu action that the main window will connect to
    factory_edit_requested = pyqtSignal()
    # Add signals for undo/redo/cut/copy/paste if those actions are handled here
    # For now, based on main_window.py, only factory_edit is an explicit menu action.

    def __init__(self, parent=None):
        super().__init__("&Edit", parent)
        self.parent_window = parent # Reference to the main window if needed

        self._create_actions()

    def _create_actions(self):
        """Creates the QActions for the Edit menu."""

        # Edit Factory Info Action (previously handled by factory_info_section, now moved to menu)
        self.edit_factory_action = QAction("Factory Name...", self)
        self.edit_factory_action.setStatusTip("Edit factory name and location information")
        self.edit_factory_action.triggered.connect(self.factory_edit_requested.emit)
        self.addAction(self.edit_factory_action)

        # In main_window.py, there are also mentions of Ctrl+Z/Y for undo/redo
        # and Ctrl+C/V for copy/paste, which are typically handled at the TableWidget level.
        # If specific menu actions are desired for these, they would be added here.
        # For now, we are adhering to the current main_window.py's menu structure.
