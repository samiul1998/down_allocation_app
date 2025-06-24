# down_allocation_app/ui/menu_bar/file_menu.py

import os
from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt, pyqtSignal

class FileMenu(QMenu):
    # Define signals for each menu action that the main window will connect to
    new_requested = pyqtSignal()
    open_requested = pyqtSignal()
    save_requested = pyqtSignal()
    save_as_requested = pyqtSignal()
    export_excel_requested = pyqtSignal()
    export_pdf_requested = pyqtSignal()
    exit_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__("&File", parent)
        self.parent_window = parent # Reference to the main window if needed

        self._create_actions()

    def _get_icon_path(self, icon_name):
        """Helper to get the absolute path for an icon."""
        # Assuming icons are in 'down_allocation_app/assets'
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return os.path.abspath(os.path.join(base_dir, 'assets', icon_name))

    def _create_actions(self):
        """Creates the QActions for the File menu."""

        # New Action
        self.new_action = QAction("New", self)
        self.new_action.setShortcut("Ctrl+N")
        self.new_action.setStatusTip("Clear all current inputs and tables")
        self.new_action.triggered.connect(self.new_requested.emit)
        self.addAction(self.new_action)

        # Open Action
        self.open_action = QAction("Open...", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.setStatusTip("Open a saved project file (.dax)")
        # self.open_action.setIcon(QIcon(self._get_icon_path('open_icon.png'))) # Add icon if available
        self.open_action.triggered.connect(self.open_requested.emit)
        self.addAction(self.open_action)

        # Save Action
        self.save_action = QAction("Save", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.setStatusTip("Save the current project as a .dax file")
        # self.save_action.setIcon(QIcon(self._get_icon_path('save_icon.png'))) # Add icon if available
        self.save_action.triggered.connect(self.save_requested.emit)
        self.addAction(self.save_action)
        
        # Save As Action (previously Ctrl+Shift+S in main_window, kept here)
        self.save_as_action = QAction("Save As...", self)
        self.save_as_action.setShortcut("Ctrl+Shift+S")
        self.save_as_action.setStatusTip("Save the current project to a new file")
        self.save_as_action.triggered.connect(self.save_as_requested.emit)
        self.addAction(self.save_as_action)

        self.addSeparator() # Separator after save actions

        # Export to Excel Action
        self.export_excel_action = QAction("Export to Excel", self)
        self.export_excel_action.setShortcut("Ctrl+Shift+E")
        self.export_excel_action.setStatusTip("Exports table data to .xlsx")
        self.export_excel_action.triggered.connect(self.export_excel_requested.emit)
        self.addAction(self.export_excel_action)

        # Export to PDF Action
        self.export_pdf_action = QAction("Export to PDF", self)
        self.export_pdf_action.setShortcut("Ctrl+E")
        self.export_pdf_action.setStatusTip("Generates a print-ready .pdf")
        # self.export_pdf_action.setIcon(QIcon(self._get_icon_path('print_icon.png'))) # Add icon if available
        self.export_pdf_action.triggered.connect(self.export_pdf_requested.emit)
        self.addAction(self.export_pdf_action)

        self.addSeparator() # Separator before exit

        # Exit Action
        self.exit_action = QAction("Exit", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.setStatusTip("Closes the application")
        self.exit_action.triggered.connect(self.exit_requested.emit)
        self.addAction(self.exit_action)

    def set_new_action_enabled(self, enabled: bool):
        """Enables or disables the 'New' action."""
        self.new_action.setEnabled(enabled)

    def set_open_action_enabled(self, enabled: bool):
        """Enables or disables the 'Open' action."""
        self.open_action.setEnabled(enabled)

    def set_save_action_enabled(self, enabled: bool):
        """Enables or disables the 'Save' action."""
        self.save_action.setEnabled(enabled)

    def set_save_as_action_enabled(self, enabled: bool):
        """Enables or disables the 'Save As' action."""
        self.save_as_action.setEnabled(enabled)

    def set_export_excel_action_enabled(self, enabled: bool):
        """Enables or disables the 'Export to Excel' action."""
        self.export_excel_action.setEnabled(enabled)

    def set_export_pdf_action_enabled(self, enabled: bool):
        """Enables or disables the 'Export to PDF' action."""
        self.export_pdf_action.setEnabled(enabled)

    def set_exit_action_enabled(self, enabled: bool):
        """Enables or disables the 'Exit' action."""
        self.exit_action.setEnabled(enabled)
