# down_allocation_app/ui/main_window.py

from ui.sections.bottom_table import BottomTableSection
from ui.sections.top_table import TopTableSection
from ui.sections.adjust_table import AdjustTableSection
from ui.sections.top_input import TopInputSection
from ui.sections.factory_info import FactoryInfoSection
from ui.dialogs.settings_dialog import SettingsDialog
from ui.dialogs.progress_dialog import ProgressDialog
from ui.dialogs.confirmation_dialog import ConfirmationDialog
from ui.dialogs.factory_edit_dialog import FactoryEditDialog
from ui.dialogs.about_dialog import AboutDialog
from ui.dialogs.help_dialog import HelpDialog
from ui.menu_bar.app_menu_bar import AppMenuBar
from ui.tool_bar.app_tool_bar import AppToolBar
from styles import AppStyles
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QComboBox, QDateEdit, QPushButton,
                             QDialog, QListWidget, QDialogButtonBox, QFormLayout,
                             QFrame, QSizePolicy, QStyleFactory, QTableWidget,
                             QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox)
from PyQt6.QtGui import QFont, QDoubleValidator, QPalette, QColor, QIntValidator, QKeyEvent, QIcon, QPixmap, QAction
from PyQt6.QtCore import Qt, QDate, QSettings, QEvent, QTimer, QCoreApplication, QPoint, QPropertyAnimation, QEasingCurve
import sys
import os
import pandas as pd
import warnings
import json
warnings.filterwarnings("ignore", category=DeprecationWarning)


class DownAllocationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuration variables - now mostly from AppStyles
        self.input_field_width = AppStyles.INPUT_FIELD_WIDTH
        self.vertical_spacing = AppStyles.VERTICAL_SPACING
        self.horizontal_spacing = AppStyles.HORIZONTAL_SPACING
        self.factory_font_size = AppStyles.FACTORY_FONT_SIZE
        self.input_fields_font_size = AppStyles.INPUT_FIELDS_FONT_SIZE
        self.input_fields_label_size = AppStyles.INPUT_FIELDS_LABEL_SIZE
        self.row_column_count_size = AppStyles.ROW_COLUMN_COUNT_SIZE
        self.button_font_size = AppStyles.BUTTON_FONT_SIZE
        self.input_field_height = AppStyles.INPUT_FIELD_HEIGHT
        self.horizontal_form_spacing = AppStyles.HORIZONTAL_FORM_SPACING

        self.panel_name_col_width = AppStyles.PANEL_NAME_COL_WIDTH
        self.panel_qty_col_width = AppStyles.PANEL_QTY_COL_WIDTH
        self.sewing_area_col_width = AppStyles.SEWING_AREA_COL_WIDTH

        self.base_font = AppStyles.BASE_FONT

        # Using AppSettings for general app settings
        self.settings = QSettings("DownAllocation", "AppSettings")
        self.factory_settings = QSettings(
            "DownAllocation", "FactoryInfo")  # Dedicated for factory info

        # Initialize current project path to None
        self.current_project_path = None
        # Initialize last used folder paths for QFileDialog
        self.last_opened_folder = self.settings.value("last_opened_folder", self._get_desktop_path())
        self.last_saved_folder = self.settings.value("last_saved_folder", self._get_desktop_path())

        # Initialize initial states to None for safe access during early __init__ calls
        self.initial_input_data = None
        self.initial_table_data = None
        self.initial_row_count = None
        self.initial_col_count = None


        self.init_ui()
        # Instantiate and set the AppMenuBar
        self.app_menu_bar = AppMenuBar(self)
        self.setMenuBar(self.app_menu_bar)

        # Instantiate and add the AppToolBar
        self.app_tool_bar = AppToolBar("File Toolbar", self)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.app_tool_bar) # Add to top area

        self.connect_signals()

        # Load initial factory info
        factory_name = self.factory_settings.value("factory_name", "")
        factory_location = self.factory_settings.value("factory_location", "")

        if not factory_name or not factory_location:
            self.show_factory_edit()
        else:
            self.factory_info_section.update_factory_display(
                factory_name, factory_location)

        # Load and apply view settings from QSettings at startup
        show_factory_info = self.settings.value(
            'view_settings/show_factory_info', True, type=bool)
        show_bottom_table = self.settings.value(
            'view_settings/show_bottom_table', True, type=bool)

        # Update the menu bar's checked states
        self.app_menu_bar.set_view_actions_checked_state(show_factory_info, show_bottom_table)
        self.factory_info_section.setVisible(show_factory_info)
        self.bottom_table_section.setVisible(show_bottom_table)


        self.update_all_tables_and_dropdowns()
        
        # Now that all UI elements are set up and populated with defaults, capture the initial state.
        self.initial_input_data = self.top_input_section.get_input_data()
        self.initial_table_data = self.top_table_section.save_table_content()
        self.initial_row_count = self.adjust_table_section.row_input.text()
        self.initial_col_count = self.adjust_table_section.col_input.text()

        self.check_input_changes() # This will correctly set the save button state after initial load

        # Apply styles after UI setup and initial data load
        self.reapply_app_styles(on_startup=True)


    def init_ui(self):
        # Set initial window title to just the app name
        self.setWindowTitle("Automatic Down Allocation System")
        self.setMinimumSize(1300, 900)
        self.setFont(self.base_font)

        icon_path = os.path.join(os.path.dirname(
            __file__), '..', 'assets', 'app_icon.ico')
        icon_path = os.path.abspath(icon_path)
        self.setWindowIcon(QIcon(icon_path))

        self.showMaximized()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(self.vertical_spacing)

        self.factory_info_section = FactoryInfoSection(self)
        main_layout.addWidget(self.factory_info_section)

        self.top_input_section = TopInputSection(self)
        main_layout.addWidget(self.top_input_section)

        self.adjust_table_section = AdjustTableSection(self)
        main_layout.addWidget(self.adjust_table_section)

        self.top_table_section = TopTableSection(self)
        main_layout.addWidget(self.top_table_section)

        self.bottom_table_section = BottomTableSection(self)
        main_layout.addWidget(self.bottom_table_section)

        fusion_style = QStyleFactory.create("Fusion")
        if fusion_style:
            self.setStyle(fusion_style)

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.AlternateBase,
                         QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.ColorRole.Link, QColor(0, 0, 255))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(227, 242, 253))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
        self.setPalette(palette)

    def connect_signals(self):
        # Connect AppMenuBar signals to main_window methods
        self.app_menu_bar.new_requested.connect(self.reset_all_fields)
        self.app_menu_bar.open_requested.connect(self.open_project)
        self.app_menu_bar.save_requested.connect(self.save_project)
        self.app_menu_bar.save_as_requested.connect(self.save_as_project)
        self.app_menu_bar.export_excel_requested.connect(self.export_to_excel)
        self.app_menu_bar.export_pdf_requested.connect(self.export_to_pdf)
        self.app_menu_bar.exit_requested.connect(self.close)
        self.app_menu_bar.factory_edit_requested.connect(self.show_factory_edit)
        self.app_menu_bar.toggle_factory_info_requested.connect(self.toggle_factory_info_panel)
        self.app_menu_bar.toggle_bottom_table_requested.connect(self.toggle_bottom_table_panel)
        self.app_menu_bar.settings_requested.connect(self.show_settings_dialog)
        self.app_menu_bar.help_requested.connect(self.show_help_dialog)
        self.app_menu_bar.about_requested.connect(self.show_about_dialog)

        # Connect AppToolBar signals to main_window methods (removed new_requested)
        # self.app_tool_bar.new_requested.connect(self.reset_all_fields) # REMOVED
        self.app_tool_bar.open_requested.connect(self.open_project)
        self.app_tool_bar.save_requested.connect(self.save_project)
        self.app_tool_bar.print_preview_requested.connect(self.print_preview)
        self.app_tool_bar.print_requested.connect(self.print_document)

        self.top_input_section.date_input.dateChanged.connect(
            self.check_input_changes)
        self.top_input_section.buyer_input.textChanged.connect(
            self.check_input_changes)
        
        self.top_input_section.style_input.textChanged.connect(self.check_input_changes)

        self.top_input_section.season_combo.currentTextChanged.connect(
            self.check_input_changes)
        
        self.top_input_section.garments_stage_combo.currentTextChanged.connect(self.check_input_changes)
        
        self.top_input_section.ecodown_input.textChanged.connect(self.update_all_tables_and_dropdowns)
        
        self.top_input_section.garment_weight_input.textChanged.connect(self.update_all_tables_and_dropdowns)

        self.top_input_section.base_size_combo.currentTextChanged.connect(
            self.update_all_tables_and_dropdowns)
        self.top_input_section.base_size_combo.currentTextChanged.connect(
            self.highlight_base_size_in_tables)

        self.adjust_table_section.set_counts_requested.connect(
            lambda r, c: self.set_row_col_counts(r, c, show_confirmation=True))
        self.adjust_table_section.reset_all_requested.connect(
            self.reset_all_fields)
        self.adjust_table_section.row_input.textChanged.connect(
            self.check_input_changes)
        self.adjust_table_section.col_input.textChanged.connect(
            self.check_input_changes)

        self.top_table_section.data_changed.connect(
            self.update_all_tables_and_dropdowns)
        
        self.top_table_section.size_headers_changed.connect(
            self.top_input_section.update_base_size_dropdown)
        self.top_table_section.table.request_resize.connect(
            lambda r, c: self._handle_table_resize_request(r, c))

    # region Factory Information Methods
    def show_factory_edit(self):
        current_name = self.factory_settings.value(
            "factory_name", "")  # Use factory_settings
        current_location = self.factory_settings.value(
            "factory_location", "")  # Use factory_settings

        dialog = FactoryEditDialog(current_name, current_location, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            factory_name, factory_location = dialog.get_factory_info()
            self.factory_settings.setValue(
                "factory_name", factory_name)  # Use factory_settings
            self.factory_settings.setValue(
                "factory_location", factory_location)  # Use factory_settings
            self.factory_info_section.update_factory_display(
                factory_name, factory_location)
            
            # Only update title with factory name if no project is loaded
            if self.current_project_path is None:
                self.setWindowTitle(f"Automatic Down Allocation System - {factory_name}")
            self.check_input_changes()
    # endregion

    # region Table Methods Coordination
    def update_all_tables_and_dropdowns(self):
        """
        Orchestrates updates for all tables and dropdowns when relevant data changes.
        This is the central point for triggering recalculations and UI updates.
        """
        # Disconnect to prevent infinite loop during programmatic updates
        try:
            self.top_table_section.data_changed.disconnect(self.update_all_tables_and_dropdowns)
            self.top_input_section.ecodown_input.textChanged.disconnect(self.update_all_tables_and_dropdowns)
            self.top_input_section.garment_weight_input.textChanged.disconnect(self.update_all_tables_and_dropdowns)
            self.top_input_section.base_size_combo.currentTextChanged.disconnect(self.update_all_tables_and_dropdowns)
        except TypeError: # Signal might not be connected yet on first run
            pass

        try:
            self.calculate_top_table_totals()

            top_table_calc_data = self.top_table_section.get_table_data_for_calculation()
            input_data = self.top_input_section.get_input_data()

            self.bottom_table_section.update_table_data(
                top_table_calc_data, input_data)

            self.highlight_base_size_in_tables(input_data['base_size'])

            self.top_input_section.update_base_size_dropdown(
                self.top_table_section.get_available_sizes())

            # Calculate and update Approx Weight
            selected_base_size = self.top_input_section.base_size_combo.currentText()
            approx_weight_value = 0.0
            if selected_base_size:
                total_base_size_area = self.top_table_section.get_total_area_for_size(selected_base_size)
                # Use the new constant from AppStyles
                approx_weight_value = total_base_size_area * AppStyles.APPROX_WEIGHT_FACTOR
            self.top_input_section.set_approx_weight(approx_weight_value)

            self.check_input_changes()
        finally:
            # Reconnect signals
            self.top_table_section.data_changed.connect(self.update_all_tables_and_dropdowns)
            self.top_input_section.ecodown_input.textChanged.connect(self.update_all_tables_and_dropdowns)
            self.top_input_section.garment_weight_input.textChanged.connect(self.update_all_tables_and_dropdowns)
            self.top_input_section.base_size_combo.currentTextChanged.connect(self.update_all_tables_and_dropdowns)


    def calculate_top_table_totals(self):
        """
        Calculates and updates the total row in the top table.
        This method uses programmatic_change flag to prevent itemChanged signal recursion.
        """
        top_table_widget = self.top_table_section.table

        top_table_widget.programmatic_change = True
        try:
            total_qty = 0
            for r in range(2, top_table_widget.rowCount() - 1):
                qty_item = top_table_widget.item(r, 1)
                try:
                    qty = int(
                        qty_item.text()) if qty_item and qty_item.text().isdigit() else 0
                    total_qty += qty
                except ValueError:
                    pass

            total_qty_item = top_table_widget.item(
                top_table_widget.rowCount() - 1, 1)
            if not total_qty_item:
                total_qty_item = QTableWidgetItem()
                top_table_widget.setItem(
                    top_table_widget.rowCount() - 1, 1, total_qty_item)

            total_qty_item.setText(str(total_qty))
            total_qty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            total_qty_item.setFont(
                QFont("Courier New", AppStyles.TABLE_HEADERS_FONT_SIZE, QFont.Weight.Bold))
            total_qty_item.setBackground(QColor(220, 220, 220))

            for col_idx in range(2, top_table_widget.columnCount()):
                total_area = 0.0
                for row in range(2, top_table_widget.rowCount() - 1):
                    qty_item = top_table_widget.item(row, 1)
                    area_item = top_table_widget.item(row, col_idx)
                    try:
                        qty = int(
                            qty_item.text()) if qty_item and qty_item.text().isdigit() else 0
                        area = float(area_item.text()) if area_item and area_item.text().replace(
                            ".", "", 1).isdigit() else 0.0
                        total_area += qty * area
                    except ValueError:
                        pass

                total_area_item = top_table_widget.item(
                    top_table_widget.rowCount() - 1, col_idx)
                if not total_area_item:
                    total_area_item = QTableWidgetItem()
                    top_table_widget.setItem(
                        top_table_widget.rowCount() - 1, col_idx, total_area_item)
                total_area_item.setText(f"{total_area:.2f}")
                total_area_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                total_area_item.setFont(
                    QFont("Courier New", AppStyles.TABLE_HEADERS_FONT_SIZE, QFont.Weight.Bold))
                total_area_item.setBackground(QColor(220, 220, 220))
        finally:
            top_table_widget.programmatic_change = False
            top_table_widget.viewport().update()

    def set_row_col_counts(self, new_data_rows, new_size_cols, show_confirmation=True):
        current_data_rows = self.top_table_section.table.rowCount() - 3
        current_size_cols = self.top_table_section.table.columnCount() - 2

        if new_data_rows < 1 or new_size_cols < 1:
            QMessageBox.warning(
                self, "Input Error", "Number of panels and sizes must be at least 1.")
            return

        if new_data_rows == current_data_rows and new_size_cols == current_size_cols:
            if show_confirmation:
                QMessageBox.information(
                    self, "Table Size", "Table dimensions are already set to the requested values.")
            return

        proceed = True
        if show_confirmation:
            confirm_dialog = ConfirmationDialog(
                "Confirm Table Resize",
                "Changing table dimensions will clear existing data. Do you want to proceed?",
                self
            )
            if confirm_dialog.exec() == QDialog.DialogCode.Accepted:
                proceed = True
            else:
                proceed = False

        if proceed:
            self.top_table_section.table.push_undo_state()

            saved_data = self.top_table_section.save_table_content()

            self.default_data_rows = new_data_rows
            self.default_cols = new_size_cols + 2

            self.top_table_section.setup_table_content(
                self.default_data_rows, self.default_cols)

            self.top_table_section.restore_table_content(saved_data)

            self.adjust_table_section.update_row_col_inputs(
                self.default_data_rows, self.default_cols - 2)
            self.update_all_tables_and_dropdowns()
            if show_confirmation:
                QMessageBox.information(
                    self, "Table Size", "Table dimensions updated successfully.")
            self.check_input_changes()

    def _handle_table_resize_request(self, new_data_rows, new_size_cols):
        self.set_row_col_counts(
            new_data_rows, new_size_cols, show_confirmation=False)

    def highlight_base_size_in_tables(self, base_size):
        self.top_table_section.highlight_base_size(base_size)
        self.bottom_table_section.highlight_base_size(base_size)

    # endregion

    # region Global Application Actions
    def _get_desktop_path(self):
        """Returns the path to the user's desktop."""
        return os.path.join(os.path.expanduser('~'), 'Desktop')

    def _has_unsaved_changes(self):
        """Checks if there are any unsaved changes in the application state."""
        # If initial states haven't been set yet (during very early startup), consider no changes.
        if self.initial_input_data is None or \
           self.initial_table_data is None or \
           self.initial_row_count is None or \
           self.initial_col_count is None:
            return False

        current_input_data = self.top_input_section.get_input_data()
        current_table_data = self.top_table_section.save_table_content()
        current_row_count = self.adjust_table_section.row_input.text()
        current_col_count = self.adjust_table_section.col_input.text()

        # Compare current state with the initial state
        input_data_changed = (current_input_data != self.initial_input_data)
        table_data_changed = (current_table_data != self.initial_table_data)
        row_col_count_changed = (current_row_count != self.initial_row_count or
                                 current_col_count != self.initial_col_count)

        return input_data_changed or table_data_changed or row_col_count_changed

    def check_input_changes(self):
        """
        Updates the enabled/disabled state of the reset button based on changes.
        Now also triggers an update for save/export buttons.
        """
        has_changes = self._has_unsaved_changes()
        self.adjust_table_section.reset_all_btn.setEnabled(has_changes)
        self._update_export_save_buttons_state() # Call this to update save buttons as well

    def _get_base_filename_suggestion(self):
        """Constructs a dynamic base filename (without extension) for export/save."""
        style = self.top_input_section.style_input.text().strip()
        garments_stage = self.top_input_section.garments_stage_combo.currentText().strip()
        ecodown_weight_str = self.top_input_section.ecodown_input.text().strip()
        ecodown_weight_value = 0.0
        try:
            ecodown_weight_value = float(ecodown_weight_str)
        except ValueError:
            pass # Keep 0.0 if not a valid number

        parts = []
        if style:
            parts.append(style)
        if garments_stage:
            # Replace spaces with hyphens for filename compatibility
            parts.append(garments_stage.replace(" ", "-"))
        # Only append ecodown weight if it's a valid non-zero number
        if ecodown_weight_value > 0:
            parts.append(f"{ecodown_weight_str}gram") # Use original string for display consistency
        
        if parts:
            return " - ".join(parts)
        return "Untitled" # Default if no relevant inputs


    def _update_export_save_buttons_state(self):
        """
        Enables/disables Export and Save buttons based on required input fields
        and if any calculated total in the top table is greater than 0,
        and if there are unsaved changes for the 'Save' button.
        """
        input_data = self.top_input_section.get_input_data()
        style_filled = bool(input_data['style'].strip())
        garments_stage_selected = bool(input_data['garments_stage'].strip())
        ecodown_weight_filled = False
        try:
            if float(input_data['ecodown_weight']) > 0:
                ecodown_weight_filled = True
        except ValueError:
            pass # Keep as False if conversion fails
        
        garment_weight_filled = False
        try:
            if float(input_data['garment_weight']) > 0:
                garment_weight_filled = True
        except ValueError:
            pass

        has_calculated_area = False
        top_table_widget = self.top_table_section.table
        # Iterate through total row (last row) for area columns (from col 2 onwards)
        for col_idx in range(2, top_table_widget.columnCount()):
            total_item = top_table_widget.item(top_table_widget.rowCount() - 1, col_idx)
            if total_item:
                try:
                    if float(total_item.text()) > 0:
                        has_calculated_area = True
                        break
                except ValueError:
                    pass

        # Condition for export, save as, pdf export
        can_perform_major_operation = (style_filled and garments_stage_selected and
                                       (ecodown_weight_filled or garment_weight_filled) and
                                       has_calculated_area)
        
        # Use AppMenuBar methods to control action states
        self.app_menu_bar.set_export_excel_action_enabled(can_perform_major_operation)
        self.app_menu_bar.set_save_as_action_enabled(can_perform_major_operation)
        self.app_menu_bar.set_export_pdf_action_enabled(can_perform_major_operation)
        self.app_menu_bar.set_open_action_enabled(True) # Open is always enabled
        self.app_menu_bar.set_new_action_enabled(True) # New is always enabled (in menu)

        # 'Save' menu button is enabled only if there are unsaved changes AND it's valid to save
        self.app_menu_bar.set_save_action_enabled(self._has_unsaved_changes() and can_perform_major_operation)

        # Control toolbar button states (removed set_new_action_enabled)
        # self.app_tool_bar.set_new_action_enabled(True) # Removed
        self.app_tool_bar.set_open_action_enabled(True) # Open is always enabled on toolbar
        self.app_tool_bar.set_save_action_enabled(self._has_unsaved_changes() and can_perform_major_operation)
        self.app_tool_bar.set_print_preview_action_enabled(can_perform_major_operation)
        self.app_tool_bar.set_print_action_enabled(can_perform_major_operation)


    def reset_all_fields(self):
        progress = ProgressDialog(
            "Resetting All Fields", "Clearing data...", self)
        progress.show()
        QApplication.processEvents()
        progress.update_progress(10)

        factory_name = self.factory_settings.value(
            "factory_name", "")  # Use factory_settings
        factory_location = self.factory_settings.value(
            "factory_location", "")  # Use factory_settings
        progress.update_progress(20)

        self.top_input_section.clear_inputs()
        # Explicitly set to "0.000" if desired after clear, assuming inputs are numeric
        self.top_input_section.ecodown_input.setText("0.000")
        self.top_input_section.garment_weight_input.setText("0.000")
        progress.update_progress(40)

        self.default_data_rows = AppStyles.DEFAULT_DATA_ROWS
        self.default_cols = AppStyles.DEFAULT_COLS
        self.adjust_table_section.update_row_col_inputs(
            self.default_data_rows, self.default_cols - 2)

        self.top_table_section.clear_data()
        self.top_table_section.setup_table_content(
            self.default_data_rows, self.default_cols)
        
        progress.update_progress(70)

        # Reset current project path
        self.current_project_path = None
        self.setWindowTitle("Automatic Down Allocation System")

        # Update initial states to reflect the reset state
        self.initial_input_data = self.top_input_section.get_input_data()
        self.initial_table_data = self.top_table_section.save_table_content()
        self.initial_row_count = self.adjust_table_section.row_input.text()
        self.initial_col_count = self.adjust_table_section.col_input.text()


        self.factory_info_section.update_factory_display(
            factory_name, factory_location)
        progress.update_progress(90)

        self.update_all_tables_and_dropdowns()
        progress.update_progress(100)

        self.check_input_changes() # This will now disable the save button if no changes from loaded state
        progress.close()

    def export_to_excel(self):
        # Get suggested filename without extension
        suggested_base_filename = self._get_base_filename_suggestion()

        try:
            # Use last_saved_folder as default directory
            initial_dir = self.last_saved_folder
            if not os.path.isdir(initial_dir): # Fallback if last folder doesn't exist
                initial_dir = self._get_desktop_path()

            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Excel File", os.path.join(initial_dir, suggested_base_filename + ".xlsx"), "Excel Files (*.xlsx);;All Files (*)")

            if not file_path:
                return

            # Ensure .xlsx extension
            if not file_path.endswith(".xlsx"):
                file_path += ".xlsx"
            
            # Update last_saved_folder
            self.last_saved_folder = os.path.dirname(file_path)
            self.settings.setValue("last_saved_folder", self.last_saved_folder)


            progress_dialog = ProgressDialog(
                "Exporting to Excel", "Preparing data...", self)
            progress_dialog.show()
            QApplication.processEvents()
            progress_dialog.update_progress(10)

            input_data = self.top_input_section.get_input_data()
            bottom_table_widget = self.bottom_table_section.table

            with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                workbook = writer.book
                worksheet = workbook.add_worksheet('Report')

                # Define formats for xlsxwriter
                # Keep font_size dynamic based on AppStyles
                header_format = workbook.add_format({
                    'bold': True, 'align': 'center', 'valign': 'vcenter',
                    'bg_color': '#DCDCDC', 'border': 1, 'font_name': 'Courier New',
                    'font_size': AppStyles.TABLE_HEADERS_FONT_SIZE
                })
                cell_format = workbook.add_format({
                    'align': 'center', 'valign': 'vcenter', 'border': 1,
                    'font_name': 'Courier New', 'font_size': AppStyles.TABLE_TEXT_SIZE
                })
                bold_cell_format = workbook.add_format({
                    'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1,
                    'font_name': 'Courier New', 'font_size': AppStyles.TABLE_TEXT_SIZE
                })
                blue_bold_cell_format = workbook.add_format({
                    'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1,
                    'font_color': '#0000FF', 'font_name': 'Courier New', 'font_size': AppStyles.TABLE_TEXT_SIZE
                })
                highlight_bg_format = workbook.add_format({
                    'bg_color': '#DCE6F1', 'align': 'center', 'valign': 'vcenter', 'border': 1,
                    'font_name': 'Courier New', 'font_size': AppStyles.TABLE_TEXT_SIZE
                })
                bold_highlight_bg_format = workbook.add_format({
                    'bold': True, 'bg_color': '#DCE6F1', 'align': 'center', 'valign': 'vcenter', 'border': 1,
                    'font_name': 'Courier New', 'font_size': AppStyles.TABLE_TEXT_SIZE
                })
                blue_bold_highlight_bg_format = workbook.add_format({
                    'bold': True, 'bg_color': '#DCE6F1', 'align': 'center', 'valign': 'vcenter', 'border': 1,
                    'font_color': '#0000FF', 'font_name': 'Courier New', 'font_size': AppStyles.TABLE_TEXT_SIZE
                })
                
                # --- Write Factory Info and Input Data ---
                current_excel_row = 0 # Starting row for Excel output

                # Factory Info
                factory_name = self.factory_settings.value("factory_name", "N/A")
                factory_location = self.factory_settings.value("factory_location", "N/A")
                worksheet.write(current_excel_row, 0, 'Factory Name:', header_format)
                worksheet.write(current_excel_row, 1, factory_name, cell_format)
                current_excel_row += 1
                worksheet.write(current_excel_row, 0, 'Location:', header_format)
                worksheet.write(current_excel_row, 1, factory_location, cell_format)
                current_excel_row += 2 # Add spacing

                # Input Data
                worksheet.write(current_excel_row, 0, 'Input Field', header_format)
                worksheet.write(current_excel_row, 1, 'Value', header_format)
                current_excel_row += 1
                input_fields_order = [
                    ("Date", input_data['date']),
                    ("Buyer", input_data['buyer']),
                    ("Style", input_data['style']),
                    ("Season", input_data['season']),
                    ("Garments Stage", input_data['garments_stage']),
                    ("Base Size", input_data['base_size']),
                    ("Ecodown Weight", input_data['ecodown_weight']),
                    ("Garments Weight", input_data['garment_weight']),
                    ("Approx Weight", input_data['approx_weight'])
                ]
                for label, value in input_fields_order:
                    worksheet.write(current_excel_row, 0, label, cell_format)
                    worksheet.write(current_excel_row, 1, value, cell_format)
                    current_excel_row += 1
                current_excel_row += 2 # Add spacing

                progress_dialog.update_progress(30)

                # --- Write Bottom Table Data to match UI ---
                # Set dynamic column widths based on the visible data in the bottom table
                max_col_widths = [0] * bottom_table_widget.columnCount()
                for r_pyqt in range(bottom_table_widget.rowCount()):
                    if bottom_table_widget.isRowHidden(r_pyqt):
                        continue # Skip hidden rows
                    for c_pyqt in range(bottom_table_widget.columnCount()):
                        item = bottom_table_widget.item(r_pyqt, c_pyqt)
                        if item and item.text():
                            text_len = len(item.text())
                            if text_len > max_col_widths[c_pyqt]:
                                max_col_widths[c_pyqt] = text_len

                for col_idx, width in enumerate(max_col_widths):
                    worksheet.set_column(col_idx, col_idx, width + 2) # Add some padding


                # Keep track of which cells have already been written due to merges
                # This set will store (excel_row, excel_col) for cells that are *covered* by a merge
                # This helps prevent writing data to a cell that is already part of a merge.
                written_cells = set()

                # Iterate through each row of the PyQt table
                for r_pyqt in range(bottom_table_widget.rowCount()):
                    # If the PyQt row is hidden, skip writing it to Excel
                    if bottom_table_widget.isRowHidden(r_pyqt):
                        # Use xlsxwriter to hide the corresponding row in Excel
                        worksheet.set_row(current_excel_row, options={'hidden': True})
                        # IMPORTANT: Even if hidden, we must still increment the Excel row counter
                        # to maintain correct row mapping for subsequent visible rows.
                        current_excel_row += 1
                        continue

                    for c_pyqt in range(bottom_table_widget.columnCount()):
                        # Check if this cell is already covered by a previous merge in this row
                        if (current_excel_row, c_pyqt) in written_cells:
                            continue

                        item = bottom_table_widget.item(r_pyqt, c_pyqt)
                        text = item.text() if item else ""
                        
                        # Get span information from the PyQt table using QTableWidget's methods
                        row_span_pyqt = bottom_table_widget.rowSpan(r_pyqt, c_pyqt)
                        col_span_pyqt = bottom_table_widget.columnSpan(r_pyqt, c_pyqt)


                        # Determine cell format based on PyQt's item properties
                        current_cell_format = cell_format # Default
                        if item: # Only apply styles if item exists
                            if item.font().bold():
                                current_cell_format = bold_cell_format
                            if item.foreground().color() == QColor(0, 0, 255): # Blue color
                                current_cell_format = blue_bold_cell_format
                            # Note: The background logic for light grey/light blue is more complex with Qt roles
                            # For simplicity, let's try to infer from background color directly.
                            # QColor(220, 220, 220) for light gray header-like cells
                            # QColor(220, 230, 241) for light blue highlighted cells
                            if item.background().color() == QColor(220, 220, 220): 
                                # Use header_format for fixed grey cells, ensuring bold
                                # This handles "PANEL NAME", "PANEL QTY", "WEIGHT" labels, and TOTAL rows
                                header_like_format = workbook.add_format(header_format.get_properties())
                                header_like_format.set_font_size(AppStyles.TABLE_HEADERS_FONT_SIZE)
                                header_like_format.set_bg_color('#DCDCDC')
                                current_cell_format = header_like_format
                            elif item.background().color() == QColor(220, 230, 241): # Light blue highlight
                                # Create a format for the light blue background
                                highlight_format = workbook.add_format(cell_format.get_properties())
                                highlight_format.set_bg_color('#DCE6F1')
                                if item.font().bold() and item.foreground().color() == QColor(0,0,255):
                                    highlight_format.set_bold()
                                    highlight_format.set_font_color('#0000FF')
                                elif item.font().bold():
                                    highlight_format.set_bold()
                                current_cell_format = highlight_format
                            else: # Default white background
                                current_cell_format = cell_format # Ensure non-highlighted cells use base cell format
                                if item.font().bold():
                                    current_cell_format = bold_cell_format
                                if item.foreground().color() == QColor(0,0,255):
                                    current_cell_format = blue_bold_cell_format
                        
                        # Apply merges if necessary
                        if row_span_pyqt > 1 or col_span_pyqt > 1:
                            worksheet.merge_range(
                                current_excel_row, c_pyqt,
                                current_excel_row + row_span_pyqt - 1, c_pyqt + col_span_pyqt - 1,
                                text, current_cell_format
                            )
                            # Mark all cells covered by this merge as written
                            for r_merge in range(current_excel_row, current_excel_row + row_span_pyqt):
                                for c_merge in range(c_pyqt, c_pyqt + col_span_pyqt):
                                    written_cells.add((r_merge, c_merge))
                        else:
                            worksheet.write(current_excel_row, c_pyqt, text, current_cell_format)
                            written_cells.add((current_excel_row, c_pyqt)) # Mark 1x1 cell as written

                    current_excel_row += 1 # Move to the next row in Excel after processing a PyQt row.

            progress_dialog.update_progress(100)
            progress_dialog.close()

        except Exception as e:
            QMessageBox.critical(self, "Export Error",
                                 f"Failed to export data: {e}\n\nPlease ensure 'xlsxwriter' is installed: pip install xlsxwriter")
            if 'progress_dialog' in locals():
                progress_dialog.close()

    def open_project(self):
        # Get the file path from the user
        # Use last_opened_folder as the default directory
        initial_dir = self.last_opened_folder
        if not os.path.isdir(initial_dir): # Fallback if last folder doesn't exist
            initial_dir = self._get_desktop_path()

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Project", initial_dir, "Down Allocation Files (*.dax);;All Files (*)")

        if not file_path:
            return # User cancelled

        # Update last_opened_folder
        self.last_opened_folder = os.path.dirname(file_path)
        self.settings.setValue("last_opened_folder", self.last_opened_folder)


        progress_dialog = ProgressDialog(
            "Opening Project", "Loading data...", self)
        progress_dialog.show()
        QApplication.processEvents()
        progress_dialog.update_progress(10)

        try:
            with open(file_path, 'r') as f:
                project_data = json.load(f)

            progress_dialog.update_progress(30)

            # Restore Factory Info
            factory_name = project_data.get('factory_info', {}).get('name', '')
            factory_location = project_data.get('factory_info', {}).get('location', '')
            self.factory_settings.setValue("factory_name", factory_name)
            self.factory_settings.setValue("factory_location", factory_location)
            self.factory_info_section.update_factory_display(factory_name, factory_location)
            # Update current project path and window title after successful open
            self.current_project_path = file_path
            self.setWindowTitle(f"Automatic Down Allocation System - {os.path.basename(file_path)}") # Display filename in title


            progress_dialog.update_progress(50)

            # Restore Adjust Table counts (and indirectly, top_table's dimensions)
            adjust_counts = project_data.get('adjust_table_counts', {})
            new_data_rows = adjust_counts.get('rows', AppStyles.DEFAULT_DATA_ROWS)
            new_size_cols = adjust_counts.get('cols', AppStyles.DEFAULT_COLS - 2) # Convert back from total cols
            self.adjust_table_section.update_row_col_inputs(new_data_rows, new_size_cols)
            # This implicitly calls set_row_col_counts which will setup top table content
            # We don't need a confirmation for programmatic load, so passing False
            self.set_row_col_counts(new_data_rows, new_size_cols, show_confirmation=False)
            
            # Restore Top Table data AFTER dimensions are set
            top_table_data = project_data.get('top_table_data', {})
            self.top_table_section.restore_table_content(top_table_data)
            
            progress_dialog.update_progress(70) # Progress for loading top table data

            # Restore Top Input Section data - temporarily hold base_size
            input_data = project_data.get('input_data', {})
            temp_base_size = input_data.get('base_size', '') # Use .get() to avoid KeyError if not present
            # Remove base_size from input_data before setting, so it's not set twice.
            # Pop it if it exists, otherwise keep input_data as is.
            if 'base_size' in input_data:
                input_data.pop('base_size')

            self.top_input_section.set_input_data(input_data) # This sets all other input fields

            progress_dialog.update_progress(80) # Progress after setting most input data
            
            # Update all derived tables and dropdowns (this will correctly populate base_size_combo)
            self.update_all_tables_and_dropdowns()

            # Now, explicitly set base size after the dropdown has been fully populated by update_all_tables_and_dropdowns
            if temp_base_size:
                self.top_input_section.base_size_combo.setCurrentText(temp_base_size)
            
            # Update initial states to reflect the newly loaded project's state
            self.initial_input_data = self.top_input_section.get_input_data()
            self.initial_table_data = self.top_table_section.save_table_content()
            self.initial_row_count = self.adjust_table_section.row_input.text()
            self.initial_col_count = self.adjust_table_section.col_input.text()

            self.check_input_changes() # This will now disable the save button if no changes from loaded state

            progress_dialog.update_progress(100)
            progress_dialog.close()

        except FileNotFoundError:
            progress_dialog.close()
            QMessageBox.critical(self, "Error", f"File not found: {file_path}")
        except json.JSONDecodeError:
            progress_dialog.close()
            QMessageBox.critical(self, "Error", f"Invalid project file format: {file_path}")
        except Exception as e:
            progress_dialog.close()
            QMessageBox.critical(self, "Error", f"Failed to open project: {e}")


    def _perform_save_operation(self, file_path):
        """Helper method to perform the actual saving logic."""
        progress_dialog = ProgressDialog(
            "Saving Project", "Gathering data...", self)
        progress_dialog.show()
        QApplication.processEvents()
        progress_dialog.update_progress(10)

        try:
            # Gather all data to save
            project_data = {
                'factory_info': {
                    'name': self.factory_settings.value("factory_name", ""),
                    'location': self.factory_settings.value("factory_location", "")
                },
                'input_data': self.top_input_section.get_input_data(),
                'top_table_data': self.top_table_section.save_table_content(),
                'adjust_table_counts': {
                    'rows': int(self.adjust_table_section.row_input.text()),
                    'cols': int(self.adjust_table_section.col_input.text())
                }
            }
            progress_dialog.update_progress(50)

            # Save data to JSON file
            with open(file_path, 'w') as f:
                json.dump(project_data, f, indent=4) # Use indent for human-readable output

            progress_dialog.update_progress(100)
            progress_dialog.close()
            
            # Update current project path and window title after successful save
            self.current_project_path = file_path
            self.setWindowTitle(f"Automatic Down Allocation System - {os.path.basename(file_path)}") # Display filename in title

            # Update initial state after saving to reflect current state
            self.initial_input_data = self.top_input_section.get_input_data()
            self.initial_table_data = self.top_table_section.save_table_content()
            self.initial_row_count = self.adjust_table_section.row_input.text()
            self.initial_col_count = self.adjust_table_section.col_input.text()
            self.check_input_changes() # Re-check to disable save button if no further changes

            # Update last_saved_folder
            self.last_saved_folder = os.path.dirname(file_path)
            self.settings.setValue("last_saved_folder", self.last_saved_folder)

            return True # Indicate success

        except Exception as e:
            progress_dialog.close()
            QMessageBox.critical(self, "Error", f"Failed to save project: {e}")
            return False # Indicate failure

    def save_project(self):
        if self.current_project_path:
            # If a project is already open, save directly to its path
            self._perform_save_operation(self.current_project_path)
        else:
            # If no project is open, behave like "Save As"
            self.save_as_project()

    def save_as_project(self):
        # Get suggested filename without extension
        suggested_base_filename = self._get_base_filename_suggestion()
        
        # Use last_saved_folder as default directory
        initial_dir = self.last_saved_folder
        if not os.path.isdir(initial_dir): # Fallback if last folder doesn't exist
            initial_dir = self._get_desktop_path()

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Project As", os.path.join(initial_dir, suggested_base_filename + ".dax"), "Down Allocation Files (*.dax);;All Files (*)")

        if not file_path:
            return # User cancelled

        if not file_path.endswith(".dax"):
            file_path += ".dax"
        
        self._perform_save_operation(file_path)


    def export_to_pdf(self):
        QMessageBox.information(
            self, "Export to PDF", "PDF export functionality is not yet fully implemented. It will generate a print-ready PDF of current data.")
    
    def print_preview(self):
        """Placeholder for print preview functionality."""
        QMessageBox.information(
            self, "Print Preview", "Print preview functionality is not yet implemented.")

    def print_document(self):
        """Placeholder for printing functionality."""
        QMessageBox.information(
            self, "Print", "Print functionality is not yet implemented.")

    def toggle_factory_info_panel(self, is_checked: bool): # Added is_checked parameter
        self.factory_info_section.setVisible(is_checked)
        self.settings.setValue(
            'view_settings/show_factory_info', is_checked)  # Save state

    def toggle_bottom_table_panel(self, is_checked: bool): # Added is_checked parameter
        self.bottom_table_section.setVisible(is_checked)
        self.settings.setValue(
            'view_settings/show_bottom_table', is_checked)  # Save state

    def show_settings_dialog(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.settings_changed.connect(self.reapply_app_styles)
        settings_dialog.exec()

    def reapply_app_styles(self, on_startup=False):
        """
        Re-applies application styles based on current AppStyles values,
        which might have been updated by the SettingsDialog.
        """
        app_settings = QSettings("DownAllocation", "AppSettings")

        # 1. Update AppStyles class attributes from QSettings
        # This makes the latest settings available globally through AppStyles
        AppStyles.INPUT_FIELD_WIDTH = app_settings.value(
            'settings/input_field_width', AppStyles.INPUT_FIELD_WIDTH, type=int)
        AppStyles.INPUT_FIELDS_FONT_SIZE = app_settings.value(
            'settings/input_fields_font_size', AppStyles.INPUT_FIELDS_FONT_SIZE, type=int)
        AppStyles.TABLE_HEADERS_FONT_SIZE = app_settings.value(
            'settings/table_headers_font_size', AppStyles.TABLE_HEADERS_FONT_SIZE, type=int)
        AppStyles.TABLE_TEXT_SIZE = app_settings.value(
            'settings/table_text_size', AppStyles.TABLE_TEXT_SIZE, type=int)
        AppStyles.PANEL_NAME_COL_WIDTH = app_settings.value(
            'settings/panel_name_col_width', AppStyles.PANEL_NAME_COL_WIDTH, type=int)
        AppStyles.PANEL_QTY_COL_WIDTH = app_settings.value(
            'settings/panel_qty_col_width', AppStyles.PANEL_QTY_COL_WIDTH, type=int)
        AppStyles.SEWING_AREA_COL_WIDTH = app_settings.value(
            'settings/sewing_area_col_width', AppStyles.SEWING_AREA_COL_WIDTH, type=int)
        AppStyles.INPUT_FIELD_HEIGHT = app_settings.value(
            'settings/input_field_height', AppStyles.INPUT_FIELD_HEIGHT, type=int)
        AppStyles.BUTTON_FONT_SIZE = app_settings.value(
            'settings/button_font_size', AppStyles.BUTTON_FONT_SIZE, type=int)
        AppStyles.ROW_COLUMN_COUNT_SIZE = app_settings.value(
            'settings/row_column_count_size', AppStyles.ROW_COLUMN_COUNT_SIZE, type=int)
        AppStyles.FACTORY_FONT_SIZE = app_settings.value(
            'settings/factory_font_size', AppStyles.FACTORY_FONT_SIZE, type=int)
        AppStyles.INPUT_FIELDS_LABEL_SIZE = app_settings.value(
            'settings/input_fields_label_size', AppStyles.INPUT_FIELDS_LABEL_SIZE, type=int)

        # Re-create BASE_FONT as it depends on ROW_COLUMN_COUNT_SIZE
        AppStyles.BASE_FONT = QFont(
            "Courier New", AppStyles.ROW_COLUMN_COUNT_SIZE)

        # 2. Re-apply styles to individual UI components

        # Main Window
        self.setFont(AppStyles.BASE_FONT)

        # Section Frames (Factory Info no longer has a border)
        # Clear any stylesheet to remove border
        self.factory_info_section.setStyleSheet("")
        self.top_input_section.setStyleSheet(AppStyles.FORM_CARD_STYLE)
        self.adjust_table_section.setStyleSheet(AppStyles.SECTION_FRAME_STYLE)

        # Adjust Table Section specific elements
        self.adjust_table_section.set_row_col_btn.setStyleSheet(
            AppStyles.SET_COUNTS_BUTTON_STYLE)
        self.adjust_table_section.reset_all_btn.setStyleSheet(
            AppStyles.RESET_ALL_BUTTON_STYLE)

        # Labels in AdjustTableSection
        panel_label_obj = self.adjust_table_section.findChild(
            QLabel, "panel_label")
        if panel_label_obj:
            panel_label_obj.setFont(
                QFont("Courier New", AppStyles.ROW_COLUMN_COUNT_SIZE))
            # Re-apply style to update font, border etc.
            panel_label_obj.setStyleSheet(AppStyles.LABEL_STYLE)

        size_label_obj = self.adjust_table_section.findChild(
            QLabel, "size_label")
        if size_label_obj:
            size_label_obj.setFont(
                QFont("Courier New", AppStyles.ROW_COLUMN_COUNT_SIZE))
            # Re-apply style to update font, border etc.
            size_label_obj.setStyleSheet(AppStyles.LABEL_STYLE)

        # Input fields in AdjustTableSection
        # Use AppStyles values directly for width/height consistent with updated styles.py
        self.adjust_table_section.row_input.setFixedWidth(
            AppStyles.INPUT_FIELD_WIDTH // 2)
        self.adjust_table_section.row_input.setFixedHeight(
            AppStyles.INPUT_FIELD_HEIGHT)
        self.adjust_table_section.row_input.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_FONT_SIZE))
        self.adjust_table_section.row_input.setStyleSheet(
            AppStyles.LINE_EDIT_STYLE)

        self.adjust_table_section.col_input.setFixedWidth(
            AppStyles.INPUT_FIELD_WIDTH // 2)
        self.adjust_table_section.col_input.setFixedHeight(
            AppStyles.INPUT_FIELD_HEIGHT)
        self.adjust_table_section.col_input.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_FONT_SIZE))
        self.adjust_table_section.col_input.setStyleSheet(
            AppStyles.LINE_EDIT_STYLE)

        # Tables (Top and Bottom)
        self.top_table_section.setStyleSheet(f"""
            QTableWidget {{
                font-family: "Courier New";
                font-size: {AppStyles.TABLE_TEXT_SIZE}px;
                gridline-color: #dcdcdc;
                border: 1px solid #dcdcdc;
            }}
            QTableWidget::item {{
                padding: 5px;
            }}
            QTableWidget::item:selected {{
                background-color: #e3f2fd;
                color: black;
            }}
        """)
        self.bottom_table_section.setStyleSheet(f"""
            QTableWidget {{
                font-family: "Courier New";
                font-size: {AppStyles.TABLE_TEXT_SIZE}px;
                gridline-color: #dcdcdc;
                border: 1px solid #dcdcdc;
            }}
            QTableWidget::item {{
                padding: 5px;
            }}
            QTableWidget::item:selected {{
                background-color: #e3f2fd;
                color: black;
            }}
        """)

        # To force tables to re-render with new column widths and row heights:
        # Save current table data, re-setup structure, then restore data.
        top_table_data = self.top_table_section.save_table_content()
        current_data_rows = self.top_table_section.table.rowCount() - 3
        current_total_cols = self.top_table_section.table.columnCount()
        self.top_table_section.setup_table_content(
            current_data_rows, current_total_cols)
        self.top_table_section.restore_table_content(top_table_data)

        # TopInputSection elements
        self.top_input_section.date_input.setFixedHeight(
            AppStyles.INPUT_FIELD_HEIGHT)
        self.top_input_section.buyer_input.setFixedHeight(
            AppStyles.INPUT_FIELD_HEIGHT)
        self.top_input_section.style_input.setFixedHeight(
            AppStyles.INPUT_FIELD_HEIGHT)
        self.top_input_section.ecodown_input.setFixedHeight(
            AppStyles.INPUT_FIELD_HEIGHT)
        self.top_input_section.garment_weight_input.setFixedHeight(
            AppStyles.INPUT_FIELD_HEIGHT)
        self.top_input_section.approx_weight_input.setFixedHeight(
            AppStyles.INPUT_FIELD_HEIGHT)
        self.top_input_section.season_combo.setFixedHeight(
            AppStyles.INPUT_FIELD_HEIGHT)
        self.top_input_section.garments_stage_combo.setFixedHeight(
            AppStyles.INPUT_FIELD_HEIGHT)
        self.top_input_section.base_size_combo.setFixedHeight(
            AppStyles.INPUT_FIELD_HEIGHT)

        self.top_input_section.date_input.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_FONT_SIZE))
        self.top_input_section.buyer_input.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_FONT_SIZE))
        self.top_input_section.style_input.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_FONT_SIZE))
        self.top_input_section.ecodown_input.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_FONT_SIZE))
        self.top_input_section.garment_weight_input.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_FONT_SIZE))
        self.top_input_section.approx_weight_input.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_FONT_SIZE))
        self.top_input_section.season_combo.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_FONT_SIZE))
        self.top_input_section.garments_stage_combo.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_FONT_SIZE))
        self.top_input_section.base_size_combo.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_FONT_SIZE))

        self.top_input_section.date_input.setStyleSheet(
            AppStyles.DATE_EDIT_STYLE)
        self.top_input_section.buyer_input.setStyleSheet(
            AppStyles.LINE_EDIT_STYLE)
        self.top_input_section.style_input.setStyleSheet(
            AppStyles.LINE_EDIT_STYLE)
        self.top_input_section.ecodown_input.setStyleSheet(
            AppStyles.LINE_EDIT_STYLE)
        self.top_input_section.garment_weight_input.setStyleSheet(
            AppStyles.LINE_EDIT_STYLE)
        self.top_input_section.approx_weight_input.setStyleSheet(
            AppStyles.LINE_EDIT_STYLE)
        self.top_input_section.season_combo.setStyleSheet(
            AppStyles.COMBO_BOX_STYLE)
        self.top_input_section.garments_stage_combo.setStyleSheet(
            AppStyles.COMBO_BOX_STYLE)
        self.top_input_section.base_size_combo.setStyleSheet(
            AppStyles.COMBO_BOX_STYLE)

        for label in self.top_input_section.findChildren(QLabel):
            label.setFont(
                QFont("Courier New", AppStyles.INPUT_FIELDS_LABEL_SIZE))
            label.setStyleSheet(AppStyles.LABEL_STYLE)

        # Only run full table update and show message if not on startup
        if not on_startup:
            self.update_all_tables_and_dropdowns()

    def show_about_dialog(self):
        dialog = AboutDialog(self, version="1.0.0")
        dialog.exec()

    def show_help_dialog(self):
        dialog = HelpDialog(self)
        dialog.exec()

    def print_preview(self):
        """Placeholder for print preview functionality."""
        QMessageBox.information(
            self, "Print Preview", "Print preview functionality is not yet implemented.")

    def print_document(self):
        """Placeholder for printing functionality."""
        QMessageBox.information(
            self, "Print", "Print functionality is not yet implemented.")
    # endregion
