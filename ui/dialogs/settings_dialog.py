# down_allocation_app/ui/dialogs/settings_dialog.py

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QDialogButtonBox, QFrame, QApplication, QMessageBox,
                             QFormLayout)  # Import QFormLayout
from PyQt6.QtGui import QFont, QDoubleValidator, QIntValidator
from PyQt6.QtCore import Qt, QSettings, pyqtSignal
from styles import AppStyles  # Import AppStyles to get default values


class SettingsDialog(QDialog):
    settings_changed = pyqtSignal()  # Signal to notify main window

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Application Settings")
        # self.setFixedSize(500, 400) # Removed fixed size for auto-adjust

        self.settings = QSettings("DownAllocation", "AppSettings")
        # Ensure QSettings has latest AppStyles defaults before loading current settings
        self._load_app_styles_into_qsettings()
        self.current_settings = self._load_current_settings_from_qsettings()

        self.setup_ui()
        self._load_ui_from_settings()

    def _load_app_styles_into_qsettings(self):
        """
        Ensures QSettings are initialized with AppStyles defaults if not already present.
        This prevents settings dialog from starting with empty fields or incorrect defaults.
        """
        defaults = {
            'input_field_width': AppStyles.INPUT_FIELD_WIDTH,
            'input_fields_font_size': AppStyles.INPUT_FIELDS_FONT_SIZE,
            'table_headers_font_size': AppStyles.TABLE_HEADERS_FONT_SIZE,
            'table_text_size': AppStyles.TABLE_TEXT_SIZE,
            'panel_name_col_width': AppStyles.PANEL_NAME_COL_WIDTH,
            'panel_qty_col_width': AppStyles.PANEL_QTY_COL_WIDTH,
            'sewing_area_col_width': AppStyles.SEWING_AREA_COL_WIDTH,
            'input_field_height': AppStyles.INPUT_FIELD_HEIGHT,
            'button_font_size': AppStyles.BUTTON_FONT_SIZE,
            'row_column_count_size': AppStyles.ROW_COLUMN_COUNT_SIZE,
            'factory_font_size': AppStyles.FACTORY_FONT_SIZE,  # Added for persistence
            'input_fields_label_size': AppStyles.INPUT_FIELDS_LABEL_SIZE,  # Added for persistence
        }
        for key, default_value in defaults.items():
            # Only set if the setting doesn't already exist in QSettings
            if not self.settings.contains(f'settings/{key}'):
                self.settings.setValue(f'settings/{key}', default_value)

    def _load_current_settings_from_qsettings(self):
        """Loads settings from QSettings."""
        s = self.settings
        return {
            'input_field_width': s.value('settings/input_field_width', type=int),
            'input_fields_font_size': s.value('settings/input_fields_font_size', type=int),
            'table_headers_font_size': s.value('settings/table_headers_font_size', type=int),
            'table_text_size': s.value('settings/table_text_size', type=int),
            'panel_name_col_width': s.value('settings/panel_name_col_width', type=int),
            'panel_qty_col_width': s.value('settings/panel_qty_col_width', type=int),
            'sewing_area_col_width': s.value('settings/sewing_area_col_width', type=int),
            'input_field_height': s.value('settings/input_field_height', type=int),
            'button_font_size': s.value('settings/button_font_size', type=int),
            'row_column_count_size': s.value('settings/row_column_count_size', type=int),
            # Loaded
            'factory_font_size': s.value('settings/factory_font_size', type=int),
            # Loaded
            'input_fields_label_size': s.value('settings/input_fields_label_size', type=int),
        }

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        general_settings_frame = QFrame()
        general_settings_frame.setStyleSheet(AppStyles.FORM_CARD_STYLE)

        # Use QFormLayout for the settings, it's better for label-input pairs
        settings_form_layout = QFormLayout(general_settings_frame)
        settings_form_layout.setContentsMargins(15, 15, 15, 15)
        settings_form_layout.setHorizontalSpacing(
            10)  # Space between label and field
        settings_form_layout.setVerticalSpacing(10)  # Space between rows
        # Align labels to the right and vertically center
        settings_form_layout.setLabelAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.fields = {}  # Dictionary to hold QLineEdit references

        settings_to_add = [
            ("Input Field Width (px):", 'input_field_width', QIntValidator(50, 500)),
            ("Input Fields Font Size (px):",
             'input_fields_font_size', QIntValidator(8, 30)),
            ("Input Field Height (px):", 'input_field_height', QIntValidator(20, 60)),
            ("Button Font Size (px):", 'button_font_size', QIntValidator(8, 20)),
            ("Row/Col Label Font Size (px):",
             'row_column_count_size', QIntValidator(8, 20)),
            ("Table Headers Font Size (px):",
             'table_headers_font_size', QIntValidator(8, 20)),
            ("Table Text Font Size (px):", 'table_text_size', QIntValidator(8, 20)),
            ("Panel Name Column Width (px):",
             'panel_name_col_width', QIntValidator(50, 300)),
            ("Panel Qty Column Width (px):",
             'panel_qty_col_width', QIntValidator(50, 200)),
            ("Sewing Area Column Width (px):",
             'sewing_area_col_width', QIntValidator(50, 200)),
            ("Factory Info Font Size (px):",
             'factory_font_size', QIntValidator(8, 30)),  # Added
            ("Input Labels Font Size (px):",
             'input_fields_label_size', QIntValidator(8, 30)),  # Added
        ]

        for label_text, key, validator in settings_to_add:
            label = QLabel(label_text)
            label.setFont(QFont("Courier New", 10, QFont.Weight.Bold))
            # Ensure plain text label
            label.setStyleSheet(
                "color: #333333; border: none; background-color: transparent;")

            line_edit = QLineEdit()
            line_edit.setValidator(validator)
            line_edit.setFixedWidth(80)  # Keep fixed width for the input box
            line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # Use LINE_EDIT_STYLE for consistency
            line_edit.setStyleSheet(AppStyles.LINE_EDIT_STYLE)
            line_edit.setFont(QFont("Courier New", 10))

            settings_form_layout.addRow(
                label, line_edit)  # Add row to QFormLayout
            self.fields[key] = line_edit

        main_layout.addWidget(general_settings_frame)
        main_layout.addStretch(1)  # Push content to top

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

        # Apply button styles
        ok_btn = button_box.button(QDialogButtonBox.StandardButton.Ok)
        if ok_btn:
            ok_btn.setStyleSheet(AppStyles.CONFIRMATION_BUTTON_STYLE.replace(
                'QPushButton[text="Yes"]', 'QPushButton') + " QPushButton { background-color: #4CAF50; }")
            ok_btn.setText("Apply")  # Change "Ok" to "Apply"

        cancel_btn = button_box.button(QDialogButtonBox.StandardButton.Cancel)
        if cancel_btn:
            cancel_btn.setStyleSheet(AppStyles.CONFIRMATION_BUTTON_STYLE.replace(
                'QPushButton[text="No"]', 'QPushButton') + " QPushButton { background-color: #f44336; }")
            cancel_btn.setText("Cancel")

    def _load_ui_from_settings(self):
        """Loads current settings from internal state into the UI fields."""
        for key, line_edit in self.fields.items():
            value = self.current_settings.get(key)
            if value is not None:
                line_edit.setText(str(value))

    def accept(self):
        """Handles 'Apply' button click: saves settings and emits signal."""
        try:
            new_settings = {}
            for key, line_edit in self.fields.items():
                value = line_edit.text()
                # Use validator type for conversion, defaulting to int
                if line_edit.validator() and isinstance(line_edit.validator(), QIntValidator):
                    new_settings[key] = int(value)
                elif line_edit.validator() and isinstance(line_edit.validator(), QDoubleValidator):
                    new_settings[key] = float(value)
                else:
                    # Fallback for non-numeric fields if any were added
                    new_settings[key] = value

            # Save settings to QSettings for persistence
            for key, value in new_settings.items():
                self.settings.setValue(f'settings/{key}', value)

            # Update AppStyles class attributes immediately so main window can re-read them
            AppStyles.INPUT_FIELD_WIDTH = new_settings['input_field_width']
            AppStyles.INPUT_FIELDS_FONT_SIZE = new_settings['input_fields_font_size']
            AppStyles.TABLE_HEADERS_FONT_SIZE = new_settings['table_headers_font_size']
            AppStyles.TABLE_TEXT_SIZE = new_settings['table_text_size']
            AppStyles.PANEL_NAME_COL_WIDTH = new_settings['panel_name_col_width']
            AppStyles.PANEL_QTY_COL_WIDTH = new_settings['panel_qty_col_width']
            AppStyles.SEWING_AREA_COL_WIDTH = new_settings['sewing_area_col_width']
            AppStyles.INPUT_FIELD_HEIGHT = new_settings['input_field_height']
            AppStyles.BUTTON_FONT_SIZE = new_settings['button_font_size']
            AppStyles.ROW_COLUMN_COUNT_SIZE = new_settings['row_column_count_size']
            AppStyles.FACTORY_FONT_SIZE = new_settings['factory_font_size']
            AppStyles.INPUT_FIELDS_LABEL_SIZE = new_settings['input_fields_label_size']

            # Re-create BASE_FONT as it depends on ROW_COLUMN_COUNT_SIZE
            AppStyles.BASE_FONT = QFont(
                "Courier New", AppStyles.ROW_COLUMN_COUNT_SIZE)

            self.settings_changed.emit()  # Notify parent (main window) that settings have changed
            super().accept()  # Close the dialog
        except ValueError as e:
            QMessageBox.warning(
                self, "Invalid Input", f"Please ensure all values are valid numbers: {e}")
            return
        except Exception as e:
            QMessageBox.critical(self, "Error Saving Settings",
                                 f"An unexpected error occurred: {e}")
            return
