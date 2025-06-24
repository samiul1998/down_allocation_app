# down_allocation_app/ui/sections/bottom_table.py

# Import QSizePolicy
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QTableWidgetItem, QHeaderView, QSizePolicy
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt
import sys  # For getattr(sys, 'frozen', False)
from ui.widgets.table_widget import TableWidget  # Assuming this path
# Assuming styles.py is in the parent directory or accessible
from styles import AppStyles


class BottomTableSection(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)  # Corrected usage
        self.setup_ui()
        # Initial call to setup_table_content, will be updated by main_window
        self.setup_table_content(
            AppStyles.DEFAULT_DATA_ROWS, AppStyles.DEFAULT_COLS)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        # Placeholder initial size, actual size set in setup_table_content
        self.table = TableWidget(5, 5, self)

        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setEditTriggers(
            TableWidget.EditTrigger.NoEditTriggers)  # Make non-editable

        self.table.setStyleSheet(f"""
            QTableWidget {{
                font-family: "Courier New";
                font-size: {AppStyles.TABLE_TEXT_SIZE}px; /* Use TABLE_TEXT_SIZE for general table font */
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

        layout.addWidget(self.table)

    def setup_table_content(self, data_rows, top_table_cols):
        """
        Sets up the structure of the bottom table based on top table dimensions.
        top_table_cols refers to the total number of columns in the top table (incl. Panel Name, Qty).
        """
        # Calculate rows needed (2 header rows + 2 rows per data row + 2 total rows)
        total_rows = 2 + (2 * data_rows) + 2
        # Columns match top table but with extra "WEIGHT" column
        total_cols = top_table_cols + 1  # Panel Name, Qty, Weight + size cols

        # Check if table needs resizing
        if self.table.rowCount() != total_rows or self.table.columnCount() != total_cols:
            self.table.setRowCount(total_rows)
            self.table.setColumnCount(total_cols)

        # Clear all spans first
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                # Only reset span if it's currently a multi-cell span
                if self.table.columnSpan(row, col) > 1 or self.table.rowSpan(row, col) > 1:
                    self.table.setSpan(row, col, 1, 1)

        # Set up header merges (rows 0-1 are headers)
        self.table.setSpan(0, 0, 2, 1)  # PANEL NAME (span 2 rows)
        self.table.setSpan(0, 1, 2, 1)  # PANEL QTY (span 2 rows)
        self.table.setSpan(0, 2, 2, 1)  # WEIGHT (span 2 rows)
        self.table.setSpan(0, 3, 1, total_cols - 3)  # SIZE header span

        # Create and set header items
        headers = [
            ("PANEL NAME", 0, 0),
            ("PANEL QTY", 0, 1),
            ("WEIGHT", 0, 2),
            ("SIZE || WEIGHT DISTRIBUTION", 0, 3)
        ]
        for text, row, col in headers:
            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # Use TABLE_HEADERS_FONT_SIZE
            item.setFont(
                QFont("Courier New", AppStyles.TABLE_HEADERS_FONT_SIZE, QFont.Weight.Bold))
            # Ensure black text - Issue 1
            item.setForeground(QColor(Qt.GlobalColor.black))
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.table.setItem(row, col, item)

        # Set size headers in row 1 (below merged SIZE header)
        # These will be updated dynamically from top_table
        for col in range(3, total_cols):
            # Initial empty, will be filled by update_table_data
            item = QTableWidgetItem("")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # Use TABLE_HEADERS_FONT_SIZE
            item.setFont(
                QFont("Courier New", AppStyles.TABLE_HEADERS_FONT_SIZE))
            # Ensure black text - Issue 1
            item.setForeground(QColor(Qt.GlobalColor.black))
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.table.setItem(1, col, item)

        # Set column widths
        self.table.setColumnWidth(0, AppStyles.PANEL_NAME_COL_WIDTH)
        self.table.setColumnWidth(1, AppStyles.PANEL_QTY_COL_WIDTH)
        # Default for weight col
        self.table.setColumnWidth(2, AppStyles.SEWING_AREA_COL_WIDTH)
        for col in range(3, total_cols):
            self.table.setColumnWidth(col, AppStyles.SEWING_AREA_COL_WIDTH)

        # Set row heights for specific rows
        self.table.setRowHeight(0, 40)  # Main header row
        self.table.setRowHeight(1, 30)  # Size header row
        self.table.verticalHeader().setDefaultSectionSize(
            28)  # Default height for data rows and total rows

        # Initialize all cells to ensure they exist, especially for clear_data_rows later
        for r in range(self.table.rowCount()):
            for c in range(self.table.columnCount()):
                if not self.table.item(r, c):
                    item = QTableWidgetItem("")
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    # Make all cells non-editable
                    item.setFlags(Qt.ItemFlag.NoItemFlags)
                    # Use TABLE_TEXT_SIZE for data cells
                    item.setFont(
                        QFont("Courier New", AppStyles.TABLE_TEXT_SIZE))
                    # Ensure black by default
                    item.setForeground(QColor(Qt.GlobalColor.black))
                    self.table.setItem(r, c, item)

        # Hide in production (PyInstaller)
        if getattr(sys, 'frozen', False):
            self.table.setVisible(False)
        else:
            self.table.setVisible(True)

    def update_table_data(self, top_table_data, input_data):
        """
        Updates the bottom table based on top table data and input fields.
        :param top_table_data: Dictionary from TopTableSection.get_table_data_for_calculation()
        :param input_data: Dictionary from TopInputSection.get_input_data()
        """
        self.table.blockSignals(True)
        try:
            num_data_rows = len(top_table_data['panels'])
            num_size_cols = len(top_table_data['sizes'])

            # Recalculate row/column count needed for bottom table
            # 2 headers + 2 rows per panel + 2 total rows
            new_total_rows = 2 + (2 * num_data_rows) + 2
            # Convert back to top_table style for setup_table_content
            new_top_table_cols_for_bottom = num_size_cols + 2

            # Always call setup_table_content to ensure structure matches
            self.setup_table_content(
                num_data_rows, new_top_table_cols_for_bottom)

            # Update size headers in row 1
            for col_idx, size_name in enumerate(top_table_data['sizes']):
                # +3 for first three fixed columns
                header_item = self.table.item(1, col_idx + 3)
                header_item.setText(size_name)

            # Clear any extra size headers if columns reduced
            for col_idx in range(num_size_cols + 3, self.table.columnCount()):
                header_item = self.table.item(1, col_idx)
                if header_item:
                    header_item.setText("")

            ecodown_weight = float(input_data.get(
                'ecodown_weight', '0') or '0')
            garment_weight = float(input_data.get(
                'garment_weight', '0') or '0')
            base_size = input_data.get('base_size', '').strip()

            # Find base size column in top table data structure
            base_col_idx = -1
            if base_size:
                try:
                    base_col_idx = top_table_data['sizes'].index(base_size)
                except ValueError:
                    pass  # Base size not found in current sizes

            # Calculate total_base_area
            total_base_area = 0.0
            if base_col_idx != -1:  # Only calculate if base size is found
                for panel_entry in top_table_data['panels']:
                    panel_qty = panel_entry['qty']
                    # Ensure index is valid
                    if base_col_idx < len(panel_entry['areas']):
                        base_area_for_panel_qty_total = panel_qty * \
                            panel_entry['areas'][base_col_idx]
                        total_base_area += base_area_for_panel_qty_total

            # Clear previous highlights and content from data rows and totals
            self.clear_data_rows()
            self.clear_totals()

            # Update each panel's data
            current_bottom_data_row = 2
            for panel_entry in top_table_data['panels']:
                panel_name = panel_entry['name']
                panel_qty = panel_entry['qty']
                panel_areas = panel_entry['areas']

                # Set panel name (merged across 2 rows)
                name_cell = self.table.item(current_bottom_data_row, 0)
                name_cell.setText(panel_name)
                self.table.setSpan(current_bottom_data_row, 0, 2, 1)
                # Removed bold for data cells in first 3 columns, consistent with top table data - Issue 2 fix
                # Consistent font
                name_cell.setFont(
                    QFont("Courier New", AppStyles.TABLE_TEXT_SIZE))
                name_cell.setForeground(
                    QColor(Qt.GlobalColor.black))  # Ensure black text

                # Set panel quantity with "1X" prefix
                qty_cell = self.table.item(current_bottom_data_row, 1)
                qty_cell.setText(f"1X{panel_qty}" if panel_qty > 0 else "")
                self.table.setSpan(current_bottom_data_row, 1, 2, 1)
                # Removed bold for data cells in first 3 columns - Issue 2 fix
                # Consistent font
                qty_cell.setFont(
                    QFont("Courier New", AppStyles.TABLE_TEXT_SIZE))
                qty_cell.setForeground(
                    QColor(Qt.GlobalColor.black))  # Ensure black text

                # Set weight labels explicitly - these should remain bold
                down_label_cell = self.table.item(current_bottom_data_row, 2)
                down_label_cell.setText("DOWN WEIGHT")
                down_label_cell.setFont(QFont(
                    "Courier New", AppStyles.TABLE_TEXT_SIZE, QFont.Weight.Bold))  # Apply font and bold
                down_label_cell.setForeground(
                    QColor(Qt.GlobalColor.black))  # Ensure black text

                garment_label_cell = self.table.item(
                    current_bottom_data_row + 1, 2)
                garment_label_cell.setText("GARMENTS WEIGHT")
                garment_label_cell.setFont(QFont(
                    "Courier New", AppStyles.TABLE_TEXT_SIZE, QFont.Weight.Bold))  # Apply font and bold
                garment_label_cell.setForeground(
                    QColor(Qt.GlobalColor.black))  # Ensure black text

                self.table.setRowHidden(current_bottom_data_row, False)
                self.table.setRowHidden(
                    current_bottom_data_row + 1, garment_weight <= 0)

                # Calculate and set weights for each size
                for col_offset, size_area in enumerate(panel_areas):
                    current_col = col_offset + 3  # Adjust for first 3 fixed columns

                    sewing_area_total_for_size = panel_qty * size_area

                    down_weight_val = 0.0
                    garment_weight_val = 0.0

                    if total_base_area > 0 and base_col_idx != -1:
                        # Calculation logic for down_weight_val and garment_weight_val
                        # based on total_base_area
                        down_weight_val = (
                            ecodown_weight / total_base_area) * sewing_area_total_for_size
                        garment_weight_val = (
                            garment_weight / total_base_area) * sewing_area_total_for_size

                        if panel_qty > 0:  # Ensure no division by zero for per panel values
                            down_weight_val /= panel_qty
                            garment_weight_val /= panel_qty
                        else:
                            down_weight_val = 0.0
                            garment_weight_val = 0.0

                    # Down weight row
                    down_cell = self.table.item(
                        current_bottom_data_row, current_col)
                    down_cell.setText(
                        f"{down_weight_val:.2f}" if down_weight_val != 0 else "")
                    # Apply font size
                    down_cell.setFont(
                        QFont("Courier New", AppStyles.TABLE_TEXT_SIZE))

                    # Garment weight row
                    garment_cell = self.table.item(
                        current_bottom_data_row + 1, current_col)
                    if garment_weight > 0:
                        garment_cell.setText(
                            f"{garment_weight_val:.2f}" if garment_weight_val != 0 else "")
                    else:
                        garment_cell.setText("")
                    garment_cell.setFont(
                        QFont("Courier New", AppStyles.TABLE_TEXT_SIZE))  # Apply font size

                    # Apply bold and blue highlight to this column in bottom_table only
                    if base_col_idx != -1 and col_offset == base_col_idx:
                        font = down_cell.font()
                        font.setBold(True)
                        down_cell.setFont(font)
                        down_cell.setForeground(QColor(0, 0, 255))  # Blue
                        if garment_cell:
                            g_font = garment_cell.font()
                            g_font.setBold(True)
                            garment_cell.setFont(g_font)
                            garment_cell.setForeground(QColor(0, 0, 255))
                    else:  # Ensure other columns are not bold/blue and are black
                        font = down_cell.font()
                        font.setBold(False)
                        down_cell.setFont(font)
                        down_cell.setForeground(
                            QColor(0, 0, 0))  # Ensure black text
                        if garment_cell:
                            g_font = garment_cell.font()
                            g_font.setBold(False)
                            garment_cell.setFont(g_font)
                            garment_cell.setForeground(
                                QColor(0, 0, 0))  # Ensure black text

                current_bottom_data_row += 2  # Move to the next pair of rows for the next panel

            # Hide remaining rows if there are fewer panels than previous update
            # Up to total rows
            for row_to_hide in range(current_bottom_data_row, self.table.rowCount() - 2):
                self.table.setRowHidden(row_to_hide, True)

            # Auto-resize weight column to fit content
            self.table.resizeColumnToContents(2)
            font_metrics = self.table.fontMetrics()
            min_width = max(
                font_metrics.horizontalAdvance("DOWN WEIGHT"),
                font_metrics.horizontalAdvance("GARMENTS WEIGHT")
            ) + 20
            if self.table.columnWidth(2) < min_width:
                self.table.setColumnWidth(2, min_width)

            # Update totals
            self.update_bottom_totals(
                top_table_data['panels'], garment_weight > 0)
        finally:
            self.table.blockSignals(False)
            self.table.viewport().update()

    def update_bottom_totals(self, panels_data, show_garments_total):
        total_cols = self.table.columnCount()

        down_totals = [0.0] * (total_cols - 3)
        garment_totals = [0.0] * (total_cols - 3)

        # Sum from the actual cells in the bottom table to ensure consistency with what's displayed
        for row in range(2, self.table.rowCount() - 2, 2):  # Iterate over 'DOWN WEIGHT' rows
            if self.table.isRowHidden(row):  # Skip hidden panel rows
                continue

            qty_text = self.table.item(row, 1).text(
            ) if self.table.item(row, 1) else ""
            try:
                # Extract quantity (e.g., from "1X5" extract 5)
                qty = int(qty_text.replace("1X", "")) if qty_text.startswith(
                    "1X") and qty_text[2:].isdigit() else 1
            except ValueError:
                qty = 1  # Default to 1 if parsing fails

            for i, col in enumerate(range(3, total_cols)):
                down_cell = self.table.item(row, col)
                if down_cell and down_cell.text():
                    try:
                        # Sum the displayed per-panel down weight, then multiply by actual panel quantity
                        down_totals[i] += float(down_cell.text()) * qty
                    except ValueError:
                        pass

                garment_row = row + 1
                # Only sum if garment row is visible
                if not self.table.isRowHidden(garment_row):
                    garment_cell = self.table.item(garment_row, col)
                    if garment_cell and garment_cell.text():
                        try:
                            garment_totals[i] += float(
                                garment_cell.text()) * qty
                        except ValueError:
                            pass

        # TOTAL DOWN WEIGHT row
        total_down_row_idx = self.table.rowCount() - 2
        # Apply merge for the first 3 columns for the label - Issue 1 fix
        self.table.setSpan(total_down_row_idx, 0, 1, 3)
        self.table.setRowHidden(total_down_row_idx, False)

        label_item = self.table.item(total_down_row_idx, 0)
        label_item.setText("TOTAL DOWN WEIGHT")
        label_item.setFlags(Qt.ItemFlag.NoItemFlags)
        label_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        # Use TABLE_HEADERS_FONT_SIZE
        label_item.setFont(
            QFont("Courier New", AppStyles.TABLE_HEADERS_FONT_SIZE, QFont.Weight.Bold))
        # Ensure black text - Issue 1
        label_item.setForeground(QColor(Qt.GlobalColor.black))

        for i, col in enumerate(range(3, total_cols)):
            item = self.table.item(total_down_row_idx, col)
            item.setText(f"{round(down_totals[i]):.0f}")  # Rounded
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # Use TABLE_HEADERS_FONT_SIZE
            item.setFont(
                QFont("Courier New", AppStyles.TABLE_HEADERS_FONT_SIZE, QFont.Weight.Bold))
            # Ensure black text - Issue 1
            item.setForeground(QColor(Qt.GlobalColor.black))

        # TOTAL GARMENT WEIGHT row
        total_garment_row_idx = self.table.rowCount() - 1
        # Apply merge for the first 3 columns for the label - Issue 1 fix
        self.table.setSpan(total_garment_row_idx, 0, 1, 3)
        self.table.setRowHidden(total_garment_row_idx, not show_garments_total)

        if show_garments_total:
            label_item = self.table.item(total_garment_row_idx, 0)
            label_item.setText("TOTAL GARMENT WEIGHT")
            label_item.setFlags(Qt.ItemFlag.NoItemFlags)
            label_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # Use TABLE_HEADERS_FONT_SIZE
            label_item.setFont(
                QFont("Courier New", AppStyles.TABLE_HEADERS_FONT_SIZE, QFont.Weight.Bold))
            # Ensure black text - Issue 1
            label_item.setForeground(QColor(Qt.GlobalColor.black))

            for i, col in enumerate(range(3, total_cols)):
                item = self.table.item(total_garment_row_idx, col)
                item.setText(f"{round(garment_totals[i]):.0f}")  # Rounded
                item.setFlags(Qt.ItemFlag.NoItemFlags)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                # Use TABLE_HEADERS_FONT_SIZE
                item.setFont(
                    QFont("Courier New", AppStyles.TABLE_HEADERS_FONT_SIZE, QFont.Weight.Bold))
                # Ensure black text - Issue 1
                item.setForeground(QColor(Qt.GlobalColor.black))

        # Clear cells in hidden garment total row if it's not shown
        else:
            for col in range(total_cols):
                item = self.table.item(total_garment_row_idx, col)
                if item:
                    item.setText("")
                    # Ensure black text
                    item.setForeground(QColor(Qt.GlobalColor.black))
                    # Reset font
                    item.setFont(
                        QFont("Courier New", AppStyles.TABLE_TEXT_SIZE))

    def highlight_base_size(self, base_size):
        # Block signals during highlight operations
        self.table.blockSignals(True)
        try:
            # Clear previous highlights in bottom_table only
            for row in range(self.table.rowCount()):
                for col in range(3, self.table.columnCount()):  # Skip first 3 cols
                    item = self.table.item(row, col)
                    if item:
                        # Or default background
                        item.setBackground(QColor(Qt.GlobalColor.white))
                        # Ensure font and color are reset to default unless it's the highlighted column
                        font = item.font()
                        font.setBold(False)
                        item.setFont(font)
                        # Ensure black text
                        item.setForeground(QColor(Qt.GlobalColor.black))

            if base_size and str(base_size).strip():
                size_upper = str(base_size).strip().upper()
                for col in range(3, self.table.columnCount()):
                    header_item = self.table.item(1, col)
                    if header_item and header_item.text().strip().upper() == size_upper:
                        # Apply bold + blue to entire column
                        # Start from data rows
                        for row_idx in range(2, self.table.rowCount()):
                            item = self.table.item(row_idx, col)
                            if item:
                                font = item.font()
                                font.setBold(True)
                                item.setFont(font)
                                item.setForeground(QColor(0, 0, 255))  # Blue
                        break  # Stop after finding the column
        finally:
            self.table.blockSignals(False)  # Unblock signals

    def clear_data_rows(self):
        """Clears content of data rows in bottom table, keeping structure."""
        self.table.programmatic_change = True
        self.table.blockSignals(True)
        try:
            for row in range(2, self.table.rowCount() - 2):  # Exclude headers and total rows
                # Clear content for first 3 columns, reset their spans and fonts
                for col in range(3):
                    item = self.table.item(row, col)
                    if item:
                        item.setText("")
                        # Reset to default data font
                        item.setFont(
                            QFont("Courier New", AppStyles.TABLE_TEXT_SIZE))
                        # Reset to black color
                        item.setForeground(QColor(Qt.GlobalColor.black))
                    # Re-apply fixed spans for the merged columns (Panel Name, Qty)
                    if col == 0 or col == 1:
                        # Restore 2-row span
                        self.table.setSpan(row, col, 2, 1)
                    else:  # col == 2 (Weight label)
                        # Ensure no unintended span for Weight label
                        self.table.setSpan(row, col, 1, 1)

                # Clear content for size-related columns
                for col in range(3, self.table.columnCount()):
                    item = self.table.item(row, col)
                    if item:
                        item.setText("")
                        # Reset to default data font
                        item.setFont(
                            QFont("Courier New", AppStyles.TABLE_TEXT_SIZE))
                        # Reset to black color
                        item.setForeground(QColor(Qt.GlobalColor.black))
                    # Ensure no unintended span
                    self.table.setSpan(row, col, 1, 1)

                # Unhide all rows initially
                self.table.setRowHidden(row, False)
        finally:
            self.table.blockSignals(False)
            self.table.programmatic_change = False
            self.table.viewport().update()

    def clear_totals(self):
        """Clears content of total rows in bottom table."""
        self.table.programmatic_change = True
        self.table.blockSignals(True)
        try:
            for row_idx in [self.table.rowCount() - 2, self.table.rowCount() - 1]:
                # Clear content for first 3 columns, reset their span
                for col in range(3):
                    item = self.table.item(row_idx, col)
                    if item:
                        item.setText("")
                        # Reset to default header font
                        item.setFont(
                            QFont("Courier New", AppStyles.TABLE_HEADERS_FONT_SIZE))
                        # Reset to black color
                        item.setForeground(QColor(Qt.GlobalColor.black))

                    # This span is for the total label itself, which should be merged
                    # Re-applying the merge here to ensure it's always set correctly.
                    self.table.setSpan(row_idx, 0, 1, 3)

                # Clear content for size-related columns
                for col in range(3, self.table.columnCount()):
                    item = self.table.item(row_idx, col)
                    if item:
                        item.setText("")
                        # Reset to default header font
                        item.setFont(
                            QFont("Courier New", AppStyles.TABLE_HEADERS_FONT_SIZE))
                        # Reset to black color
                        item.setForeground(QColor(Qt.GlobalColor.black))
                    # Ensure no unintended span
                    self.table.setSpan(row_idx, col, 1, 1)

                # Unhide totals initially
                self.table.setRowHidden(row_idx, False)
        finally:
            self.table.blockSignals(False)
            self.table.programmatic_change = False
            self.table.viewport().update()
