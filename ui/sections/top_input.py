# down_allocation_app/ui/sections/top_input.py

from PyQt6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QComboBox, QDateEdit, QWidget, QSizePolicy, QMessageBox)
from PyQt6.QtGui import QDoubleValidator, QFont
from PyQt6.QtCore import Qt, QDate
# Assuming styles.py is in the parent directory or accessible
from styles import AppStyles
from ui.utils.upper_case_line_edit import UpperCaseLineEdit  # Assuming this path


class TopInputSection(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Fixed)
        self.setStyleSheet(AppStyles.FORM_CARD_STYLE)
        self.setup_ui()

    def setup_ui(self):
        # Create container widget for centering
        form_container = QWidget()
        form_container_layout = QHBoxLayout(form_container)
        form_container_layout.setContentsMargins(0, 0, 0, 0)

        # Create 3 columns for the form
        form_columns = QHBoxLayout()
        form_columns.setSpacing(AppStyles.HORIZONTAL_SPACING)

        # Column 1: Date, Buyer, Style
        col1 = QVBoxLayout()
        col1.setSpacing(AppStyles.VERTICAL_SPACING)

        # Date input
        self.date_label = QLabel("Date:")  # Make label an instance attribute
        self.date_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.date_input = QDateEdit(QDate.currentDate())
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        self.date_input.setCalendarPopup(True)
        self.date_input.setFixedWidth(AppStyles.INPUT_FIELD_WIDTH)
        self.date_input.setMinimumHeight(AppStyles.INPUT_FIELD_HEIGHT)
        date_layout = QHBoxLayout()
        date_layout.addWidget(self.date_label)
        date_layout.addWidget(self.date_input)
        col1.addLayout(date_layout)

        # Buyer input
        self.buyer_label = QLabel("Buyer:")  # Make label an instance attribute
        self.buyer_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.buyer_input = UpperCaseLineEdit()
        #self.buyer_input.setPlaceholderText("Enter Buyer Name")
        self.buyer_input.setFixedWidth(AppStyles.INPUT_FIELD_WIDTH)
        self.buyer_input.setMinimumHeight(AppStyles.INPUT_FIELD_HEIGHT)
        buyer_layout = QHBoxLayout()
        buyer_layout.addWidget(self.buyer_label)
        buyer_layout.addWidget(self.buyer_input)
        col1.addLayout(buyer_layout)

        # Style input
        self.style_label = QLabel("Style:")  # Make label an instance attribute
        self.style_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.style_input = UpperCaseLineEdit()
        #self.style_input.setPlaceholderText("Enter Style Number")
        self.style_input.setFixedWidth(AppStyles.INPUT_FIELD_WIDTH)
        self.style_input.setMinimumHeight(AppStyles.INPUT_FIELD_HEIGHT)
        style_layout = QHBoxLayout()
        style_layout.addWidget(self.style_label)
        style_layout.addWidget(self.style_input)
        col1.addLayout(style_layout)
        form_columns.addLayout(col1)

        # Column 2: Season, Garments Stage, Base Size
        col2 = QVBoxLayout()
        col2.setSpacing(AppStyles.VERTICAL_SPACING)

        # Season dropdown
        # Make label an instance attribute
        self.season_label = QLabel("Season:")
        self.season_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.season_combo = QComboBox()
        self.season_combo.setFixedWidth(AppStyles.INPUT_FIELD_WIDTH)
        self.season_combo.addItems(
            ["", "Spring", "Summer", "Fall", "Winter", "All Seasons"])
        self.season_combo.setMinimumHeight(AppStyles.INPUT_FIELD_HEIGHT)
        season_layout = QHBoxLayout()
        season_layout.addWidget(self.season_label)
        season_layout.addWidget(self.season_combo)
        col2.addLayout(season_layout)

        # Garments Stage dropdown
        # Make label an instance attribute
        self.garments_stage_label = QLabel("Garments Stage:")
        self.garments_stage_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.garments_stage_combo = QComboBox()
        self.garments_stage_combo.setFixedWidth(AppStyles.INPUT_FIELD_WIDTH)
        self.garments_stage_combo.addItems([
            "", "Proto", "Fit", "Salesman", "Size Set", "PP", "TOP", "Shipping"
        ])
        self.garments_stage_combo.setMinimumHeight(
            AppStyles.INPUT_FIELD_HEIGHT)
        garments_layout = QHBoxLayout()
        garments_layout.addWidget(self.garments_stage_label)
        garments_layout.addWidget(self.garments_stage_combo)
        col2.addLayout(garments_layout)

        # Base Size dropdown (dynamic dropdown)
        # Make label an instance attribute
        self.base_size_label = QLabel("Base Size:")
        self.base_size_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.base_size_combo = QComboBox()
        self.base_size_combo.setFixedWidth(AppStyles.INPUT_FIELD_WIDTH)
        # Initial empty item
        self.base_size_combo.addItems([""])
        self.base_size_combo.setMinimumHeight(AppStyles.INPUT_FIELD_HEIGHT)
        base_layout = QHBoxLayout()
        base_layout.addWidget(self.base_size_label)
        base_layout.addWidget(self.base_size_combo)
        col2.addLayout(base_layout)
        form_columns.addLayout(col2)

        # Column 3: Ecodown Weight, Garments Weight, Approximate Weight
        col3 = QVBoxLayout()
        col3.setSpacing(AppStyles.VERTICAL_SPACING)

        # Ecodown Weight
        # Make label an instance attribute
        self.ecodown_label = QLabel("Ecodown Weight:")
        self.ecodown_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.ecodown_input = QLineEdit()
        self.ecodown_input.setPlaceholderText("0")
        self.ecodown_input.setFixedWidth(AppStyles.INPUT_FIELD_WIDTH)
        self.ecodown_input.setValidator(QDoubleValidator(0.0, 999999.0, 3))
        self.ecodown_input.setMinimumHeight(AppStyles.INPUT_FIELD_HEIGHT)
        ecodown_layout = QHBoxLayout()
        ecodown_layout.addWidget(self.ecodown_label)
        ecodown_layout.addWidget(self.ecodown_input)
        col3.addLayout(ecodown_layout)

        # Garment Weight
        # Make label an instance attribute
        self.garment_weight_label = QLabel("Garments Weight:")
        self.garment_weight_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.garment_weight_input = QLineEdit()
        self.garment_weight_input.setPlaceholderText("0")
        self.garment_weight_input.setFixedWidth(AppStyles.INPUT_FIELD_WIDTH)
        self.garment_weight_input.setValidator(
            QDoubleValidator(0.0, 999999.0, 3))
        self.garment_weight_input.setMinimumHeight(
            AppStyles.INPUT_FIELD_HEIGHT)
        garment_layout = QHBoxLayout()
        garment_layout.addWidget(self.garment_weight_label)
        garment_layout.addWidget(self.garment_weight_input)
        col3.addLayout(garment_layout)

        # Approximate Weight (Non-editable, calculated)
        # Make label an instance attribute
        self.approx_weight_label = QLabel("Approx Weight:")
        self.approx_weight_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.approx_weight_input = QLineEdit()
        self.approx_weight_input.setPlaceholderText("Calculated Weight")
        self.approx_weight_input.setFixedWidth(AppStyles.INPUT_FIELD_WIDTH)
        self.approx_weight_input.setMinimumHeight(AppStyles.INPUT_FIELD_HEIGHT)
        self.approx_weight_input.setReadOnly(True)
        approx_layout = QHBoxLayout()
        approx_layout.addWidget(self.approx_weight_label)
        approx_layout.addWidget(self.approx_weight_input)
        col3.addLayout(approx_layout)

        form_columns.addLayout(col3)

        form_container_layout.addStretch()
        form_container_layout.addLayout(form_columns)
        form_container_layout.addStretch()

        # Set layout to form card
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(form_container)
        # Keep this for outer centering
        self.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Apply initial styles during setup
        self.reapply_styles()

    def get_input_data(self):
        return {
            "date": self.date_input.date().toString(Qt.DateFormat.ISODate),
            "buyer": self.buyer_input.text(),
            "style": self.style_input.text(),
            "season": self.season_combo.currentText(),
            "garments_stage": self.garments_stage_combo.currentText(),
            "base_size": self.base_size_combo.currentText(),
            "ecodown_weight": self.ecodown_input.text(),
            "garment_weight": self.garment_weight_input.text(),
            "approx_weight": self.approx_weight_input.text()
        }

    def set_input_data(self, data):
        self.date_input.setDate(QDate.fromString(
            data.get("date", QDate.currentDate().toString(
                Qt.DateFormat.ISODate)),
            Qt.DateFormat.ISODate))
        self.buyer_input.setText(data.get("buyer", ""))
        self.style_input.setText(data.get("style", ""))
        self.season_combo.setCurrentText(data.get("season", ""))
        self.garments_stage_combo.setCurrentText(
            data.get("garments_stage", ""))
        self.base_size_combo.setCurrentText(data.get("base_size", ""))
        self.ecodown_input.setText(data.get("ecodown_weight", ""))
        self.garment_weight_input.setText(data.get("garment_weight", ""))
        self.set_approx_weight(
            float(data.get("approx_weight", "0.0")) if data.get("approx_weight") else 0.0)

    def clear_inputs(self):
        self.date_input.setDate(QDate.currentDate())
        self.buyer_input.clear()
        self.style_input.clear()
        self.season_combo.setCurrentIndex(0)
        self.garments_stage_combo.setCurrentIndex(0)
        self.base_size_combo.clear()
        self.ecodown_input.clear()
        self.garment_weight_input.clear()
        self.set_approx_weight(0.0)

    def update_base_size_dropdown(self, sizes):
        try:
            self.base_size_combo.blockSignals(True)
            current_selection = self.base_size_combo.currentText()
            self.base_size_combo.clear()
            self.base_size_combo.addItems([""] + sizes)

            if current_selection in sizes:
                self.base_size_combo.setCurrentText(current_selection)
            else:
                self.base_size_combo.setCurrentIndex(0)
        finally:
            self.base_size_combo.blockSignals(False)

    def set_approx_weight(self, weight_value: float):
        """Sets the approximate weight, formatted to 0 decimal places."""
        self.approx_weight_input.setText(f"{int(round(weight_value))}")

    def reapply_styles(self):
        """
        Re-applies styles to all components within this section based on AppStyles.
        This method is called internally or by the parent (main_window) when settings change.
        """
        self.setStyleSheet(
            AppStyles.FORM_CARD_STYLE)  # Re-apply outer frame style

        # Apply styles to labels
        self.date_label.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_LABEL_SIZE, QFont.Weight.Bold))
        self.date_label.setStyleSheet(AppStyles.LABEL_STYLE)

        self.buyer_label.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_LABEL_SIZE, QFont.Weight.Bold))
        self.buyer_label.setStyleSheet(AppStyles.LABEL_STYLE)

        self.style_label.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_LABEL_SIZE, QFont.Weight.Bold))
        self.style_label.setStyleSheet(AppStyles.LABEL_STYLE)

        self.season_label.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_LABEL_SIZE, QFont.Weight.Bold))
        self.season_label.setStyleSheet(AppStyles.LABEL_STYLE)

        self.garments_stage_label.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_LABEL_SIZE, QFont.Weight.Bold))
        self.garments_stage_label.setStyleSheet(AppStyles.LABEL_STYLE)

        self.base_size_label.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_LABEL_SIZE, QFont.Weight.Bold))
        self.base_size_label.setStyleSheet(AppStyles.LABEL_STYLE)

        self.ecodown_label.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_LABEL_SIZE, QFont.Weight.Bold))
        self.ecodown_label.setStyleSheet(AppStyles.LABEL_STYLE)

        self.garment_weight_label.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_LABEL_SIZE, QFont.Weight.Bold))
        self.garment_weight_label.setStyleSheet(AppStyles.LABEL_STYLE)

        self.approx_weight_label.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_LABEL_SIZE, QFont.Weight.Bold))
        self.approx_weight_label.setStyleSheet(AppStyles.LABEL_STYLE)

        # Apply styles to input fields and combos
        self.date_input.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_FONT_SIZE))
        self.date_input.setStyleSheet(AppStyles.DATE_EDIT_STYLE)
        self.date_input.setMinimumHeight(AppStyles.INPUT_FIELD_HEIGHT)
        self.date_input.setFixedWidth(
            AppStyles.INPUT_FIELD_WIDTH)  # Re-apply fixed width

        self.buyer_input.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_FONT_SIZE))
        self.buyer_input.setStyleSheet(AppStyles.LINE_EDIT_STYLE)
        self.buyer_input.setMinimumHeight(AppStyles.INPUT_FIELD_HEIGHT)
        self.buyer_input.setFixedWidth(
            AppStyles.INPUT_FIELD_WIDTH)  # Re-apply fixed width

        self.style_input.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_FONT_SIZE))
        self.style_input.setStyleSheet(AppStyles.LINE_EDIT_STYLE)
        self.style_input.setMinimumHeight(AppStyles.INPUT_FIELD_HEIGHT)
        self.style_input.setFixedWidth(
            AppStyles.INPUT_FIELD_WIDTH)  # Re-apply fixed width

        self.season_combo.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_FONT_SIZE))
        self.season_combo.setStyleSheet(AppStyles.COMBO_BOX_STYLE)
        self.season_combo.setMinimumHeight(AppStyles.INPUT_FIELD_HEIGHT)
        self.season_combo.setFixedWidth(
            AppStyles.INPUT_FIELD_WIDTH)  # Re-apply fixed width

        self.garments_stage_combo.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_FONT_SIZE))
        self.garments_stage_combo.setStyleSheet(AppStyles.COMBO_BOX_STYLE)
        self.garments_stage_combo.setMinimumHeight(
            AppStyles.INPUT_FIELD_HEIGHT)
        self.garments_stage_combo.setFixedWidth(
            AppStyles.INPUT_FIELD_WIDTH)  # Re-apply fixed width

        self.base_size_combo.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_FONT_SIZE))
        self.base_size_combo.setStyleSheet(AppStyles.COMBO_BOX_STYLE)
        self.base_size_combo.setMinimumHeight(AppStyles.INPUT_FIELD_HEIGHT)
        self.base_size_combo.setFixedWidth(
            AppStyles.INPUT_FIELD_WIDTH)  # Re-apply fixed width

        self.ecodown_input.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_FONT_SIZE))
        self.ecodown_input.setStyleSheet(AppStyles.LINE_EDIT_STYLE)
        self.ecodown_input.setMinimumHeight(AppStyles.INPUT_FIELD_HEIGHT)
        self.ecodown_input.setFixedWidth(
            AppStyles.INPUT_FIELD_WIDTH)  # Re-apply fixed width

        self.garment_weight_input.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_FONT_SIZE))
        self.garment_weight_input.setStyleSheet(AppStyles.LINE_EDIT_STYLE)
        self.garment_weight_input.setMinimumHeight(
            AppStyles.INPUT_FIELD_HEIGHT)
        self.garment_weight_input.setFixedWidth(
            AppStyles.INPUT_FIELD_WIDTH)  # Re-apply fixed width

        self.approx_weight_input.setFont(
            QFont("Courier New", AppStyles.INPUT_FIELDS_FONT_SIZE))
        self.approx_weight_input.setStyleSheet(AppStyles.LINE_EDIT_STYLE)
        self.approx_weight_input.setMinimumHeight(AppStyles.INPUT_FIELD_HEIGHT)
        self.approx_weight_input.setFixedWidth(
            AppStyles.INPUT_FIELD_WIDTH)  # Re-apply fixed width
