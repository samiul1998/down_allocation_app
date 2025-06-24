# down_allocation_app/styles.py

from PyQt6.QtGui import QFont, QColor, QPalette


class AppStyles:
    # Configuration variables (restored to user's specified "before" values)
    INPUT_FIELD_WIDTH = 250
    VERTICAL_SPACING = 12
    HORIZONTAL_SPACING = 20
    FACTORY_FONT_SIZE = 15
    INPUT_FIELDS_FONT_SIZE = 20
    INPUT_FIELDS_LABEL_SIZE = 20
    ROW_COLUMN_COUNT_SIZE = 12
    BUTTON_FONT_SIZE = 12

    # Mapped old font size names to new, refactored names for consistency
    # Used for top two header rows in top table, and bottom table's TOTAL rows
    TABLE_HEADERS_FONT_SIZE = 12
    # Used for data cells in both tables, and "DOWN WEIGHT"/"GARMENTS WEIGHT" labels
    TABLE_TEXT_SIZE = 12

    DEFAULT_DATA_ROWS = 10
    DEFAULT_COLS = 10
    INPUT_FIELD_HEIGHT = 10  # Increased to 30 to match button heights and prevent cropping
    HORIZONTAL_FORM_SPACING = 30  # This controls spacing within form elements

    # Column width settings (restored to user's specified "before" values)
    PANEL_NAME_COL_WIDTH = 200
    PANEL_QTY_COL_WIDTH = 120
    SEWING_AREA_COL_WIDTH = 100

    # Fonts (restored to user's specified "before" value)
    BASE_FONT = QFont("Courier New", ROW_COLUMN_COUNT_SIZE)

    # Colors
    TABLE_HINT_TEXT_COLOR = QColor(150, 150, 150)  # Light gray for hint text

    # New constant for Approximate Weight calculation
    APPROX_WEIGHT_FACTOR = 0.02094

    # Stylesheets (ALL restored from user's provided "before" snippet, with unsupported CSS removed)

    # General button style (adapted from the old EDIT_BUTTON_STYLE for broader use)
    BUTTON_STYLE = """
        QPushButton {
            background-color: #4CAF50; /* Green */
            color: white;
            border: none;
            padding: 8px 16px;
            text-align: center;
            text-decoration: none;
            font-size: 10px; /* Kept generic button size smaller for distinction from main inputs */
            margin: 4px 2px;
            border-radius: 5px;
            font-family: "Courier New";
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #367c39;
        }
        QPushButton:disabled {
            background-color: #cccccc;
            color: #666666;
        }
    """

    # Specific style for the Edit Factory button (restored from user's provided old snippet)
    EDIT_BUTTON_STYLE = """
        QPushButton {
            background-color: #6c757d;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 5px 10px;
        }
        QPushButton:hover {
            background-color: #5a6268;
        }
    """

    # Styles for the buttons in AdjustTableSection, matching the user's provided snippet exactly
    SET_COUNTS_BUTTON_STYLE = """
        QPushButton {
            background-color: #2196F3;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            min-width: 100px;
        }
        QPushButton:hover {
            background-color: #0b7dda;
        }
    """
    RESET_ALL_BUTTON_STYLE = """
        QPushButton {
            background-color: #f44336;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            min-width: 100px;
        }
        QPushButton:hover {
            background-color: #da190b;
        }
        QPushButton:disabled {
            background-color: #cccccc;
            color: #666666;
        }
    """
    EXPORT_EXCEL_BUTTON_STYLE = """
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            min-width: 100px;
        }
        QPushButton:hover {
            background-color: #388E3C;
        }
    """
    ABOUT_BUTTON_STYLE = """
        QPushButton {
            background-color: #6c757d;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            min-width: 100px;
        }
        QPushButton:hover {
            background-color: #5a6268;
        }
    """
    HELP_BUTTON_STYLE = """
        QPushButton {
            background-color: #17a2b8;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            min-width: 100px;
        }
        QPushButton:hover {
            background-color: #138496;
        }
    """

    # Frame styles for sections
    SECTION_FRAME_STYLE = """
        QFrame {
            border: 1px solid #dcdcdc;
            border-radius: 8px;
            background-color: #fdfdfd;
            padding: 10px;
        }
    """

    # Style for the form card/input section container (restored from user's provided old snippet)
    FORM_CARD_STYLE = f"""
        QFrame {{
            background-color: #ffffff;
            border-radius: 8px;
            padding: 15px;
            /* 'box-shadow' removed - not supported by PyQt */
        }}
        QLabel {{
            font-family: "Courier New";
            font-size: {INPUT_FIELDS_LABEL_SIZE}px;
            color: #495057;
            padding-right: 5px;
        }}
        QLineEdit, QComboBox, QDateEdit {{
            font-family: "Courier New";
            font-size: {INPUT_FIELDS_FONT_SIZE}px;
            border: 1px solid #ced4da;
            border-radius: 4px;
            padding: 8px;
            min-height: {INPUT_FIELD_HEIGHT}px; /* Min-height from new value */
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 30px;
            border-left-width: 1px;
            border-left-color: #e0e0e0;
            border-left-style: solid;
            border-top-right-radius: 4px;
            border-bottom-right-radius: 4px;
        }}
        QComboBox QAbstractItemView {{
            font-family: "Courier New";
            font-size: {INPUT_FIELDS_FONT_SIZE}px;
            border: 1px solid #e0e0e0;
            selection-background-color: #e3f2fd;
            selection-color: black;
            padding: 4px;
        }}
    """

    # Label style definition (restored from user's provided old snippet, with border/background for clarity)
    LABEL_STYLE = f"""
        QLabel {{
            font-family: "Courier New";
            font-size: {INPUT_FIELDS_LABEL_SIZE}px;
            color: #495057;
            padding-right: 5px;
            border: none; /* Explicitly ensure no border */
            background-color: transparent; /* Explicitly ensure no background */
        }}
    """

    # LineEdit common style (restored from user's provided old snippet)
    LINE_EDIT_STYLE = f"""
        QLineEdit {{
            font-family: "Courier New";
            font-size: {INPUT_FIELDS_FONT_SIZE}px;
            border: 1px solid #ced4da;
            border-radius: 4px;
            padding: 8px;
            min-height: {INPUT_FIELD_HEIGHT}px; /* Min-height from new value */
        }}
    """

    # ComboBox common style (added for TopInputSection)
    COMBO_BOX_STYLE = f"""
        QComboBox {{
            border: 1px solid #cccccc;
            border-radius: 4px;
            padding: 5px;
            font-family: "Courier New";
            font-size: {INPUT_FIELDS_FONT_SIZE}px;
            background-color: #ffffff;
            selection-background-color: #a8d9ff;
            min-height: {INPUT_FIELD_HEIGHT}px; /* Min-height from new value */
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left-width: 1px;
            border-left-color: #cccccc;
            border-left-style: solid;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
        }}
        QComboBox::down-arrow {{
            image: url(assets/arrow_down.png); /* Placeholder if needed, otherwise use built-in */
        }}
    """

    # DateEdit common style (added for TopInputSection)
    DATE_EDIT_STYLE = f"""
        QDateEdit {{
            border: 1px solid #cccccc;
            border-radius: 4px;
            padding: 5px;
            font-family: "Courier New";
            font-size: {INPUT_FIELDS_FONT_SIZE}px;
            background-color: #ffffff;
            selection-background-color: #a8d9ff;
            min-height: {INPUT_FIELD_HEIGHT}px; /* Min-height from new value */
        }}
        QDateEdit:focus {{
            border: 1px solid #4CAF50;
        }}
        QDateEdit::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left-width: 1px;
            border-left-color: #cccccc;
            border-left-style: solid;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
        }}
        QDateEdit::down-arrow {{
            image: url(assets/calendar_icon.png); /* Placeholder if needed, otherwise use built-in */
        }}
    """

    # QProgressBar styles (restored from user's provided old snippet)
    PROGRESS_BAR_STYLE = """
        QProgressBar {
            border: 1px solid #ccc;
            border-radius: 5px;
            text-align: center;
            background: #f0f0f0;
        }
        QProgressBar::chunk {
            background-color: #4CAF50;
            width: 10px;
            border-radius: 4px;
        }
    """

    # Confirmation Dialog styles (restored from user's provided old snippet)
    CONFIRMATION_LABEL_STYLE = """
        QLabel {
            font-family: 'Segoe UI';
            font-size: 14px;
            color: #333;
            padding: 20px;
        }
    """

    CONFIRMATION_BUTTON_STYLE = """
        QPushButton {
            font-family: 'Segoe UI';
            font-size: 13px;
            min-width: 80px;
            padding: 8px 16px;
            border-radius: 4px;
            border: none;
        }
        QPushButton[text="Yes"] {
            background-color: #4285F4;
            color: white;
        }
        QPushButton[text="Yes"]:hover {
            background-color: #3367D6;
        }
        QPushButton[text="No"] {
            background-color: #F1F3F4;
            color: #3C4043;
        }
        QPushButton[text="No"]:hover {
            background-color: #E8EAED;
        }
    """

    CONFIRMATION_DIALOG_STYLE = """
        QDialog {
            background-color: white;
            border-radius: 8px;
        }
    """

    # This was likely for a specific QLineEdit delegate, kept as is.
    UPPERCASE_LINE_EDIT_STYLE = "font-family: 'Courier New';"