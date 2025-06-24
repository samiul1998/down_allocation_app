# down_allocation_app/ui/sections/adjust_table.py

from PyQt6.QtWidgets import QFrame, QLabel, QLineEdit, QPushButton, QHBoxLayout, QSizePolicy, QMessageBox, QDialog
from PyQt6.QtGui import QIntValidator, QFont
from PyQt6.QtCore import Qt, pyqtSignal
from styles import AppStyles # Assuming styles.py is in the parent directory or accessible
from ui.dialogs.confirmation_dialog import ConfirmationDialog # Assuming this path

class AdjustTableSection(QFrame):
    # Signals for actions
    set_counts_requested = pyqtSignal(int, int) # (rows, columns)
    reset_all_requested = pyqtSignal()
    # Keeping these signals, even if buttons are removed from UI, as they are connected to menu actions
    export_excel_requested = pyqtSignal()
    about_requested = pyqtSignal()
    help_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.parent_window = parent 
        self.setup_ui()
        self.setStyleSheet(AppStyles.SECTION_FRAME_STYLE) # Apply section frame style here

    def setup_ui(self):
        # Main horizontal layout for the entire AdjustTableSection
        main_h_layout = QHBoxLayout(self)
        main_h_layout.setContentsMargins(10, 5, 10, 5)
        main_h_layout.setSpacing(AppStyles.HORIZONTAL_SPACING) # Use common horizontal spacing

        # Add a stretch at the beginning to push all subsequent elements to the right
        main_h_layout.addStretch(1)

        # Layout for "Panel: [input]"
        panel_group_layout = QHBoxLayout()
        panel_group_layout.setSpacing(0) # Tight spacing between label and input
        
        panel_label = QLabel("PANEL:")
        panel_label.setObjectName("panel_label") # Set objectName for findChild
        panel_label.setStyleSheet(AppStyles.LABEL_STYLE) # Apply LABEL_STYLE
        panel_label.setFont(QFont("Courier New", AppStyles.ROW_COLUMN_COUNT_SIZE))
        panel_group_layout.addWidget(panel_label)

        self.row_input = QLineEdit(str(AppStyles.DEFAULT_DATA_ROWS))
        self.row_input.setValidator(QIntValidator(1, 100))
        self.row_input.setFixedWidth(100) # Increased width to prevent cropping
        self.row_input.setFixedHeight(30) # Set fixed height to match buttons
        self.row_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.row_input.setFont(QFont("Courier New", AppStyles.INPUT_FIELDS_FONT_SIZE)) # Use INPUT_FIELDS_FONT_SIZE for text
        self.row_input.setStyleSheet(AppStyles.LINE_EDIT_STYLE) # Apply LINE_EDIT_STYLE
        panel_group_layout.addWidget(self.row_input)

        main_h_layout.addLayout(panel_group_layout)

        # Spacer between Panel group and Size group
        main_h_layout.addSpacing(AppStyles.HORIZONTAL_FORM_SPACING)

        # Layout for "SIZE: [input]"
        size_group_layout = QHBoxLayout()
        size_group_layout.setSpacing(0) # Tight spacing between label and input

        col_label = QLabel("SIZE:")
        col_label.setObjectName("size_label") # Set objectName for findChild
        col_label.setStyleSheet(AppStyles.LABEL_STYLE) # Apply LABEL_STYLE
        col_label.setFont(QFont("Courier New", AppStyles.ROW_COLUMN_COUNT_SIZE))
        size_group_layout.addWidget(col_label)

        self.col_input = QLineEdit(str(AppStyles.DEFAULT_COLS - 2)) # -2 for fixed cols
        self.col_input.setValidator(QIntValidator(1, 50))
        self.col_input.setFixedWidth(100) # Increased width to prevent cropping
        self.col_input.setFixedHeight(30) # Set fixed height to match buttons
        self.col_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.col_input.setFont(QFont("Courier New", AppStyles.INPUT_FIELDS_FONT_SIZE)) # Use INPUT_FIELDS_FONT_SIZE for text
        self.col_input.setStyleSheet(AppStyles.LINE_EDIT_STYLE) # Apply LINE_EDIT_STYLE
        size_group_layout.addWidget(self.col_input)

        main_h_layout.addLayout(size_group_layout)

        # Spacer before the SET button
        main_h_layout.addSpacing(AppStyles.HORIZONTAL_FORM_SPACING)

        # SET PANEL | SIZE button
        self.set_row_col_btn = QPushButton("SET PANEL | SIZE")
        self.set_row_col_btn.setFont(QFont("Courier New", AppStyles.BUTTON_FONT_SIZE))
        self.set_row_col_btn.clicked.connect(self._on_set_counts_clicked)
        self.set_row_col_btn.setStyleSheet(AppStyles.SET_COUNTS_BUTTON_STYLE) # Apply specific style
        main_h_layout.addWidget(self.set_row_col_btn)

        # Spacer before the RESET ALL FIELDS button
        main_h_layout.addSpacing(AppStyles.HORIZONTAL_SPACING)

        # RESET ALL FIELDS button
        self.reset_all_btn = QPushButton("RESET ALL FIELDS")
        self.reset_all_btn.setFont(QFont("Courier New", AppStyles.BUTTON_FONT_SIZE))
        self.reset_all_btn.clicked.connect(self._on_reset_all_clicked)
        self.reset_all_btn.setEnabled(False) # Disabled by default
        self.reset_all_btn.setStyleSheet(AppStyles.RESET_ALL_BUTTON_STYLE) # Apply specific style
        main_h_layout.addWidget(self.reset_all_btn)

        # The Export, About, Help buttons are now handled by the menu bar and removed from the UI directly.
        # self.export_excel_btn = QPushButton("EXPORT TO EXCEL")
        # self.about_btn = QPushButton("ABOUT")
        # self.help_btn = QPushButton("HELP")


    def _on_set_counts_clicked(self):
        try:
            rows = int(self.row_input.text())
            cols = int(self.col_input.text())
            self.set_counts_requested.emit(rows, cols)
        except ValueError:
            QMessageBox.warning(self.parent_window, "Input Error", "Please enter valid numbers for Panel and Size.")

    def _on_reset_all_clicked(self):
        confirm_dialog = ConfirmationDialog(
            "Confirm Reset",
            "Are you sure you want to reset all input fields and table data?",
            self.parent_window # Pass main window as parent for proper modality
        )
        if confirm_dialog.exec() == QDialog.DialogCode.Accepted:
            self.reset_all_requested.emit()

    def update_row_col_inputs(self, rows, cols):
        """Updates the text in the row/column input fields."""
        self.row_input.setText(str(rows))
        self.col_input.setText(str(cols))