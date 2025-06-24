# down_allocation_app/ui/menu_bar/app_menu_bar.py

from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtCore import pyqtSignal

from ui.menu_bar.file_menu import FileMenu
from ui.menu_bar.edit_menu import EditMenu
from ui.menu_bar.view_menu import ViewMenu # Assuming you want a View menu
from ui.menu_bar.help_menu import HelpMenu

class AppMenuBar(QMenuBar):
    # Consolidate all signals from individual menus here
    new_requested = pyqtSignal()
    open_requested = pyqtSignal()
    save_requested = pyqtSignal()
    save_as_requested = pyqtSignal()
    export_excel_requested = pyqtSignal()
    export_pdf_requested = pyqtSignal()
    exit_requested = pyqtSignal()
    factory_edit_requested = pyqtSignal()
    toggle_factory_info_requested = pyqtSignal(bool)
    toggle_bottom_table_requested = pyqtSignal(bool)
    help_requested = pyqtSignal()
    about_requested = pyqtSignal()
    settings_requested = pyqtSignal() # Re-adding this signal as it was in main_window.py's menu bar

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent

        self._create_menus()
        self._connect_menu_signals()

    def _create_menus(self):
        """Instantiates individual menu classes and adds them to the menu bar."""
        self.file_menu = FileMenu(self)
        self.edit_menu = EditMenu(self)
        self.view_menu = ViewMenu(self)
        self.help_menu = HelpMenu(self)

        self.addMenu(self.file_menu)
        self.addMenu(self.edit_menu)
        self.addMenu(self.view_menu)
        # Re-introducing a placeholder for System Setup/Settings menu
        # This can be made a separate class if it becomes complex
        self.settings_menu = self.addMenu("&System Setup")
        self.settings_action = self.settings_menu.addAction("Settings...")
        self.settings_action.setShortcut("Ctrl+Alt+S")
        self.settings_action.setStatusTip("Opens a settings dialog to control app-wide visual variables")
        self.settings_action.triggered.connect(self.settings_requested.emit)

        self.addMenu(self.help_menu)

    def _connect_menu_signals(self):
        """Connects signals from individual menu classes to AppMenuBar's own signals."""
        self.file_menu.new_requested.connect(self.new_requested.emit)
        self.file_menu.open_requested.connect(self.open_requested.emit)
        self.file_menu.save_requested.connect(self.save_requested.emit)
        self.file_menu.save_as_requested.connect(self.save_as_requested.emit)
        self.file_menu.export_excel_requested.connect(self.export_excel_requested.emit)
        self.file_menu.export_pdf_requested.connect(self.export_pdf_requested.emit)
        self.file_menu.exit_requested.connect(self.exit_requested.emit)

        self.edit_menu.factory_edit_requested.connect(self.factory_edit_requested.emit)

        self.view_menu.toggle_factory_info_requested.connect(self.toggle_factory_info_requested.emit)
        self.view_menu.toggle_bottom_table_requested.connect(self.toggle_bottom_table_requested.emit)

        self.help_menu.help_requested.connect(self.help_requested.emit)
        self.help_menu.about_requested.connect(self.about_requested.emit)

    # Method to update the checked state of view menu actions from main_window
    def set_view_actions_checked_state(self, factory_info_checked: bool, bottom_table_checked: bool):
        self.view_menu.toggle_factory_info_action.setChecked(factory_info_checked)
        self.view_menu.toggle_bottom_table_action.setChecked(bottom_table_checked)

    # Methods to enable/disable specific actions, to be called from main_window
    def set_new_action_enabled(self, enabled: bool):
        """Enables or disables the 'New' action in the File menu."""
        self.file_menu.set_new_action_enabled(enabled)

    def set_save_action_enabled(self, enabled: bool):
        """Enables or disables the 'Save' action in the File menu."""
        self.file_menu.set_save_action_enabled(enabled)

    def set_save_as_action_enabled(self, enabled: bool):
        """Enables or disables the 'Save As' action in the File menu."""
        self.file_menu.set_save_as_action_enabled(enabled)

    def set_export_excel_action_enabled(self, enabled: bool):
        """Enables or disables the 'Export to Excel' action in the File menu."""
        self.file_menu.set_export_excel_action_enabled(enabled)

    def set_export_pdf_action_enabled(self, enabled: bool):
        """Enables or disables the 'Export to PDF' action in the File menu."""
        self.file_menu.set_export_pdf_action_enabled(enabled)

    def set_open_action_enabled(self, enabled: bool):
        """Enables or disables the 'Open' action in the File menu."""
        self.file_menu.set_open_action_enabled(enabled)
