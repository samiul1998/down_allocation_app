# down_allocation_app/ui/tool_bar/app_tool_bar.py

import os
from PyQt6.QtWidgets import QToolBar
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt, pyqtSignal, QSize

class AppToolBar(QToolBar):
    # Signals for toolbar actions (removed new_requested)
    # new_requested = pyqtSignal() # REMOVED
    open_requested = pyqtSignal()
    save_requested = pyqtSignal()
    print_preview_requested = pyqtSignal()
    print_requested = pyqtSignal()

    def __init__(self, title="Main Toolbar", parent=None):
        super().__init__(title, parent)
        self.setMovable(True)
        self.setFloatable(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)

        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.setIconSize(QSize(32, 32))

        self.icon_spacing_padding = 10 # Adjust this value as needed

        self.setStyleSheet(f"""
            QToolButton {{
                padding: {self.icon_spacing_padding}px;
                margin: 0px;
            }}
            QToolBar::separator {{
                width: 15px; 
            }}
        """)

        self._create_actions()

    def _get_icon_path(self, icon_name):
        """Helper to get the absolute path for an icon.
        Includes error handling for missing icons."""
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        icon_path = os.path.abspath(os.path.join(base_dir, 'assets', icon_name))
        
        if not os.path.exists(icon_path):
            print(f"Warning: Icon file not found at {icon_path}. Using blank icon.")
            return QIcon()
        return QIcon(icon_path)

    def _create_actions(self):
        """Creates and adds QActions to the toolbar."""

        # Removed: New Action
        # self.new_action = QAction(self._get_icon_path('new_icon.png'), "New", self)
        # self.new_action.setToolTip("New (Ctrl+N)")
        # self.new_action.triggered.connect(self.new_requested.emit)
        # self.addAction(self.new_action)

        # Open Action
        self.open_action = QAction(self._get_icon_path('open_icon.png'), "Open", self)
        self.open_action.setToolTip("Open (Ctrl+O)")
        self.open_action.triggered.connect(self.open_requested.emit)
        self.addAction(self.open_action)

        # Save Action
        self.save_action = QAction(self._get_icon_path('save_icon.png'), "Save", self)
        self.save_action.setToolTip("Save (Ctrl+S)")
        self.save_action.triggered.connect(self.save_requested.emit)
        self.addAction(self.save_action)

        # Print Preview Action
        self.print_preview_action = QAction(self._get_icon_path('print_preview.png'), "Print Preview", self)
        self.print_preview_action.setToolTip("Print Preview (Ctrl+P)")
        self.print_preview_action.triggered.connect(self.print_preview_requested.emit)
        self.addAction(self.print_preview_action)

        # Print Action
        self.print_action = QAction(self._get_icon_path('print_icon.png'), "Print", self)
        self.print_action.setToolTip("Print (Ctrl+Shift+P)")
        self.print_action.triggered.connect(self.print_requested.emit)
        self.addAction(self.print_action)

    # Methods to enable/disable toolbar actions, to be called from main_window
    def set_save_action_enabled(self, enabled: bool):
        self.save_action.setEnabled(enabled)

    def set_open_action_enabled(self, enabled: bool):
        self.open_action.setEnabled(enabled)

    def set_print_preview_action_enabled(self, enabled: bool):
        self.print_preview_action.setEnabled(enabled)

    def set_print_action_enabled(self, enabled: bool):
        self.print_action.setEnabled(enabled)

    # Removed: set_new_action_enabled
    # def set_new_action_enabled(self, enabled: bool):
    #    self.new_action.setEnabled(enabled)
