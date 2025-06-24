# down_allocation_app/ui/sections/top_table.py

from PyQt6.QtWidgets import QFrame, QHeaderView, QVBoxLayout, QMenu, QMessageBox, QTableWidgetItem, QSizePolicy
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt, QModelIndex, pyqtSignal
# Assuming styles.py is in the parent directory or accessible
from styles import AppStyles
from ui.widgets.table_widget import TableWidget  # Assuming this path
# Assuming this path
from ui.sections.table_delegate import TableItemDelegate, UpperCaseItemDelegate
# Import ConfirmationDialog
from ui.dialogs.confirmation_dialog import ConfirmationDialog


class TopTableSection(QFrame):
    # Signals to communicate changes back to main_window
    # Emitted when size headers are updated
    size_headers_changed = pyqtSignal(list)
    # General signal for data changes (e.g., from paste, undo/redo)
    data_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent  # Reference to the main window
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)  # Corrected usage
        self.setup_ui()
        self.setup_table_content(
            AppStyles.DEFAULT_DATA_ROWS, AppStyles.DEFAULT_COLS)

    def setup_ui(self):
        table_layout = QVBoxLayout(self)
        # 2 headers + data rows + 1 total row
        self.table = TableWidget(
            AppStyles.DEFAULT_DATA_ROWS + 3, AppStyles.DEFAULT_COLS, self)

        self.table.setItemDelegateForColumn(
            0, UpperCaseItemDelegate(self.table))
        # The TableItemDelegate includes validation and hint text
        # Apply TableItemDelegate to all other editable columns
        for i in range(1, AppStyles.DEFAULT_COLS):
            self.table.setItemDelegateForColumn(
                i, TableItemDelegate(self.table))

        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)  # Corrected method name

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

        # Set specific column widths
        self.table.setColumnWidth(0, AppStyles.PANEL_NAME_COL_WIDTH)
        self.table.setColumnWidth(1, AppStyles.PANEL_QTY_COL_WIDTH)
        for i in range(2, self.table.columnCount()):
            self.table.setColumnWidth(i, AppStyles.SEWING_AREA_COL_WIDTH)

        # Set row heights
        self.table.verticalHeader().setDefaultSectionSize(
            28)  # Default row height for data
        self.table.setRowHeight(0, 40)  # Main header row
        self.table.setRowHeight(1, 30)  # Size header row
        self.table.setRowHeight(self.table.rowCount() - 1, 35)  # Total row

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

        table_layout.addWidget(self.table)

        # Connect context menu
        self.table.customContextMenuRequested.connect(self.create_context_menu)

        # Forward itemChanged signal from inner table
        self.table.itemChanged.connect(self._on_inner_item_changed)

    def _on_inner_item_changed(self, item):
        """Internal handler for item changes in the TableWidget."""
        # Crucial: If change is programmatic, do not process or emit further signals from this method.
        # This prevents recursion during programmatic updates (like total calculation).
        if self.table.programmatic_change:
            return

        if item.row() == 0 or item.row() == self.table.rowCount() - 1:  # Header or total row, usually non-editable
            return

        # Format text (already handled by UpperCaseItemDelegate for relevant cells)
        # However, if an item is set programmatically or through paste, this ensures uppercase
        # We also need to block signals here to prevent self-recursion if setText is called.
        if (item.column() == 0) or (item.row() == 1 and item.column() >= 2):
            if item.text() != item.text().upper():
                self.table.blockSignals(True)  # Block signals temporarily
                item.setText(item.text().upper())
                self.table.blockSignals(False)  # Unblock signals

        # Check for duplicate size headers
        if item.row() == 1 and item.column() >= 2:
            current_text = item.text().strip()
            if current_text:
                for col_idx in range(2, self.table.columnCount()):
                    if col_idx != item.column():
                        other_item = self.table.item(1, col_idx)
                        if other_item and other_item.text().strip() == current_text:
                            QMessageBox.warning(self.parent_window, "Duplicate Size",
                                                f"Size '{current_text}' already exists! Please choose a unique name.")
                            # Block signals temporarily
                            self.table.blockSignals(True)
                            item.setText("")  # Clear the duplicate
                            self.table.blockSignals(False)  # Unblock signals
                            break
            # Emit signal about size headers change to update base size dropdown in TopInputSection
            self.size_headers_changed.emit(self.get_available_sizes())

        # Emit general data changed signal for parent to recalculate totals
        self.data_changed.emit()

    def setup_table_content(self, data_rows, total_cols):
        """Sets up the table headers, merges, and initial empty cells."""
        self.table.setRowCount(
            2 + data_rows + 1)  # 2 header rows + data_rows + 1 total row
        self.table.setColumnCount(total_cols)

        # Clear existing spans
        for r in range(self.table.rowCount()):
            for c in range(self.table.columnCount()):
                if self.table.columnSpan(r, c) > 1 or self.table.rowSpan(r, c) > 1:
                    self.table.setSpan(r, c, 1, 1)

        # Set up header merges
        self.table.setSpan(0, 0, 2, 1)  # PANEL NAME (span 2 rows)
        self.table.setSpan(0, 1, 2, 1)  # PANEL QUANTITY (span 2 rows)
        self.table.setSpan(0, 2, 1, total_cols - 2)  # SIZE header span

        # Create and set header items
        headers = [
            ("PANEL NAME", 0, 0),
            ("PANEL QUANTITY", 0, 1),
            ("SIZE || PANEL SEWING AREA", 0, 2)
        ]

        for text, row, col in headers:
            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setFont(
                QFont("Courier New", AppStyles.TABLE_HEADERS_FONT_SIZE, QFont.Weight.Bold))
            # Ensure black text - Issue 1
            item.setForeground(QColor(Qt.GlobalColor.black))
            # Make completely non-interactive
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.table.setItem(row, col, item)

        # Set size headers in row 1 (below merged SIZE header)
        for col in range(2, total_cols):
            # Initialize with empty string so delegate can show hint text
            item = QTableWidgetItem("")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # Use TABLE_HEADERS_FONT_SIZE
            item.setFont(
                QFont("Courier New", AppStyles.TABLE_HEADERS_FONT_SIZE))
            # Ensure black text - Issue 1
            item.setForeground(QColor(Qt.GlobalColor.black))
            item.setToolTip("Enter size name like XS, S, M, L")
            # Make size headers fully editable
            item.setFlags(Qt.ItemFlag.ItemIsEnabled |
                          Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(1, col, item)

        # Set up data rows (from row 2 to second-to-last row)
        for row in range(2, self.table.rowCount() - 1):
            # Panel Name column
            name_item = QTableWidgetItem("")
            name_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # Use TABLE_TEXT_SIZE
            name_item.setFont(QFont("Courier New", AppStyles.TABLE_TEXT_SIZE))
            self.table.setItem(row, 0, name_item)

            # Panel Quantity column
            qty_item = QTableWidgetItem("")
            qty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # Use TABLE_TEXT_SIZE
            qty_item.setFont(QFont("Courier New", AppStyles.TABLE_TEXT_SIZE))
            self.table.setItem(row, 1, qty_item)

            # Sewing area columns
            for col in range(2, total_cols):
                area_item = QTableWidgetItem("")
                area_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                # Use TABLE_TEXT_SIZE
                area_item.setFont(
                    QFont("Courier New", AppStyles.TABLE_TEXT_SIZE))
                self.table.setItem(row, col, area_item)

        # Set up TOTAL row
        total_item = QTableWidgetItem("TOTAL")
        total_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        total_item.setFont(
            QFont("Courier New", AppStyles.TABLE_HEADERS_FONT_SIZE, QFont.Weight.Bold))  # Use TABLE_HEADERS_FONT_SIZE
        # Ensure black text - Issue 1
        total_item.setForeground(QColor(Qt.GlobalColor.black))
        total_item.setFlags(Qt.ItemFlag.ItemIsEnabled |
                            Qt.ItemFlag.ItemIsSelectable)  # Not editable
        self.table.setItem(self.table.rowCount() - 1, 0, total_item)
        self.table.setSpan(self.table.rowCount() - 1, 0, 1, 2)

        for col in range(2, total_cols):
            total_cell = QTableWidgetItem("0.00")
            total_cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            total_cell.setFont(
                QFont("Courier New", AppStyles.TABLE_HEADERS_FONT_SIZE, QFont.Weight.Bold))  # Use TABLE_HEADERS_FONT_SIZE
            # Ensure black text - Issue 1
            total_cell.setForeground(QColor(Qt.GlobalColor.black))
            total_cell.setFlags(Qt.ItemFlag.ItemIsEnabled |
                                Qt.ItemFlag.ItemIsSelectable)  # Not editable
            self.table.setItem(self.table.rowCount() - 1, col, total_cell)

        # Set column widths again after potential resize
        self.table.setColumnWidth(0, AppStyles.PANEL_NAME_COL_WIDTH)
        self.table.setColumnWidth(1, AppStyles.PANEL_QTY_COL_WIDTH)
        for col in range(2, self.table.columnCount()):
            self.table.setColumnWidth(col, AppStyles.SEWING_AREA_COL_WIDTH)

        # Ensure delegates are re-applied if table dimensions change significantly
        self.table.setItemDelegateForColumn(
            0, UpperCaseItemDelegate(self.table))
        for i in range(1, self.table.columnCount()):
            self.table.setItemDelegateForColumn(
                i, TableItemDelegate(self.table))

    def create_context_menu(self, pos):
        context_menu = QMenu(self.table)
        insert_row_action = context_menu.addAction("Insert Row")
        delete_row_action = context_menu.addAction("Delete Row")
        context_menu.addSeparator()
        insert_column_action = context_menu.addAction("Insert Column")
        delete_column_action = context_menu.addAction("Delete Column")

        action = context_menu.exec(self.table.mapToGlobal(pos))

        if action == insert_row_action:
            self.insert_row()
        elif action == delete_row_action:
            self.delete_row()
        elif action == insert_column_action:
            self.insert_column()
        elif action == delete_column_action:
            self.delete_column()

    def insert_row(self):
        current_row = self.table.currentRow()
        if current_row == -1 or current_row >= self.table.rowCount() - 1:
            current_row = self.table.rowCount() - 2  # Insert before total row

        self.table.push_undo_state()  # Save state before modification

        self.table.insertRow(current_row)
        for col in range(self.table.columnCount()):
            item = QTableWidgetItem("")
            # Use TABLE_TEXT_SIZE
            item.setFont(QFont("Courier New", AppStyles.TABLE_TEXT_SIZE))
            self.table.setItem(current_row, col, item)
        self.table.setRowHeight(current_row, 28)  # Default row height

        # Update row input in AdjustTableSection
        if self.parent_window and hasattr(self.parent_window, 'adjust_table_section'):
            new_data_rows = self.table.rowCount() - 3  # Subtracting header and total rows
            self.parent_window.adjust_table_section.update_row_col_inputs(
                new_data_rows, self.table.columnCount() - 2)

        self.data_changed.emit()  # Recalculate totals

    def delete_row(self):
        current_row = self.table.currentRow()
        if current_row < 2 or current_row >= self.table.rowCount() - 1:  # Cannot delete header or total row
            QMessageBox.warning(self.parent_window, "Delete Row",
                                "Cannot delete header rows or total row.")
            return

        confirm_dialog = ConfirmationDialog(
            "Confirm Deletion", "Are you sure you want to delete this row?", self.parent_window)
        if confirm_dialog.exec() == QMessageBox.StandardButton.Yes:  # Use QMessageBox.StandardButton.Yes
            self.table.push_undo_state()  # Save state before modification
            self.table.removeRow(current_row)

            # Update row input in AdjustTableSection
            if self.parent_window and hasattr(self.parent_window, 'adjust_table_section'):
                new_data_rows = self.table.rowCount() - 3
                self.parent_window.adjust_table_section.update_row_col_inputs(
                    new_data_rows, self.table.columnCount() - 2)

            self.data_changed.emit()  # Recalculate totals

    def insert_column(self):
        current_col = self.table.currentColumn()
        # Insert after fixed columns (Panel Name, Panel Quantity)
        if current_col < 2 or current_col == -1:
            # Insert at the end if no selection in data cols
            current_col = self.table.columnCount()

        self.table.push_undo_state()  # Save state before modification

        self.table.insertColumn(current_col)
        self.table.setColumnWidth(current_col, AppStyles.SEWING_AREA_COL_WIDTH)
        # Set delegate for new column
        self.table.setItemDelegateForColumn(
            current_col, TableItemDelegate(self.table))
        self.table.setItemDelegateForColumn(
            current_col, UpperCaseItemDelegate(self.table))  # Ensure uppercase too

        # Update column header (Size X)
        # Initialize with empty string so delegate can show hint text
        item = QTableWidgetItem("")
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        # Use TABLE_HEADERS_FONT_SIZE
        item.setFont(QFont("Courier New", AppStyles.TABLE_HEADERS_FONT_SIZE))
        # Ensure black text - Issue 1
        item.setForeground(QColor(Qt.GlobalColor.black))
        item.setToolTip("Enter size name like XS, S, M, L")
        item.setFlags(Qt.ItemFlag.ItemIsEnabled |
                      Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable)
        # Set the size header for the new column
        self.table.setItem(1, current_col, item)

        # Also, update main merged header if needed (not strictly necessary here as it spans dynamically)
        # Ensure the main header span is correct
        self.table.setSpan(0, 2, 1, self.table.columnCount() - 2)

        # Initialize cells for the new column
        for row in range(2, self.table.rowCount()):
            new_item = QTableWidgetItem("")
            new_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # Use TABLE_TEXT_SIZE
            new_item.setFont(QFont("Courier New", AppStyles.TABLE_TEXT_SIZE))
            self.table.setItem(row, current_col, new_item)

        # Update column input in AdjustTableSection
        if self.parent_window and hasattr(self.parent_window, 'adjust_table_section'):
            new_data_cols = self.table.columnCount() - 2
            self.parent_window.adjust_table_section.update_row_col_inputs(
                self.table.rowCount() - 3, new_data_cols)

        self.size_headers_changed.emit(
            self.get_available_sizes())  # Update base size dropdown
        self.data_changed.emit()  # Recalculate totals

    def delete_column(self):
        current_col = self.table.currentColumn()
        if current_col < 2 or current_col >= self.table.columnCount():  # Cannot delete fixed columns
            QMessageBox.warning(self.parent_window, "Delete Column",
                                "Cannot delete fixed columns (Panel Name, Panel Quantity).")
            return

        if self.table.columnCount() - 2 <= 1:  # Prevent deleting if only one size column remains
            QMessageBox.warning(self.parent_window, "Delete Column",
                                "At least one size column must remain.")
            return

        confirm_dialog = ConfirmationDialog(
            "Confirm Deletion", "Are you sure you want to delete this column?", self.parent_window)
        if confirm_dialog.exec() == QMessageBox.StandardButton.Yes:
            self.table.push_undo_state()  # Save state before modification
            self.table.removeColumn(current_col)

            # Update column input in AdjustTableSection
            if self.parent_window and hasattr(self.parent_window, 'adjust_table_section'):
                new_data_cols = self.table.columnCount() - 2
                self.parent_window.adjust_table_section.update_row_col_inputs(
                    self.table.rowCount() - 3, new_data_cols)

            # Re-label remaining size headers to be sequential (but as hint if empty)
            for col in range(2, self.table.columnCount()):
                item = self.table.item(1, col)
                if item:
                    # Clear text so delegate can apply hint if needed
                    item.setText("")

            # Re-adjust the main header span if columns changed
            self.table.setSpan(0, 2, 1, self.table.columnCount() - 2)

            self.size_headers_changed.emit(
                self.get_available_sizes())  # Update base size dropdown
            self.data_changed.emit()  # Recalculate totals

    def get_available_sizes(self):
        return [self.table.item(1, col).text().strip()
                for col in range(2, self.table.columnCount())
                if self.table.item(1, col) and self.table.item(1, col).text().strip()]

    def highlight_base_size(self, size):
        # Block signals during highlight operations
        self.table.blockSignals(True)
        try:
            # Clear previous highlights
            for r in range(self.table.rowCount()):
                for c in range(self.table.columnCount()):
                    item = self.table.item(r, c)
                    if item:
                        # Ensure default white background for all cells, except totals which are grey
                        # If it's a total row or a fixed header, retain its color
                        if r == self.table.rowCount() - 1 or (r == 0 and c < 2) or (r == 1 and c < 2):
                           pass
                        else:
                            item.setBackground(QColor(Qt.GlobalColor.white))

            if size and str(size).strip():
                size_upper = str(size).strip().upper()
                # Find the column index of the base size
                for col_idx in range(2, self.table.columnCount()):
                    header_item = self.table.item(1, col_idx)
                    if header_item and header_item.text().strip().upper() == size_upper:
                        # Highlight the entire column
                        for row_idx in range(self.table.rowCount()):
                            item = self.table.item(row_idx, col_idx)
                            if item:
                                item.setBackground(
                                    QColor(220, 230, 241))  # Light blue
                        break  # Stop after finding the column
        finally:
            self.table.blockSignals(False)  # Unblock signals

    def save_table_content(self):
        """Save all table data and size headers."""
        saved_data = {
            'size_names': [],
            # List of {'name': 'PNL1', 'qty': '1', 'areas': ['10.0', '12.0']}
            'panel_data': []
        }

        # Save size names (row 1, columns 2+)
        for col in range(2, self.table.columnCount()):
            item = self.table.item(1, col)
            saved_data['size_names'].append(item.text() if item else "")

        # Save panel names, quantities, and sewing areas (rows 2 to second-to-last)
        for row in range(2, self.table.rowCount() - 1):  # Exclude TOTAL row
            panel_name_item = self.table.item(row, 0)
            panel_qty_item = self.table.item(row, 1)

            panel_entry = {
                'name': panel_name_item.text() if panel_name_item else "",
                'qty': panel_qty_item.text() if panel_qty_item else "",
                'areas': []
            }

            for col in range(2, self.table.columnCount()):
                area_item = self.table.item(row, col)
                panel_entry['areas'].append(
                    area_item.text() if area_item else "")

            saved_data['panel_data'].append(panel_entry)

        return saved_data

    def restore_table_content(self, saved_data):
        """Restore table data and size headers after expansion."""
        self.table.blockSignals(True)  # Block signals during restore
        self.table.programmatic_change = True  # Prevent undo state saving

        try:
            # Restore size names first
            if 'size_names' in saved_data:
                for col in range(2, min(self.table.columnCount(), len(saved_data['size_names']) + 2)):
                    if col - 2 < len(saved_data['size_names']):
                        item = self.table.item(1, col)
                        if item:
                            item.setText(saved_data['size_names'][col - 2])

            # Restore panel data
            if 'panel_data' in saved_data:
                # Limit to available rows and saved data
                for row_idx in range(min(self.table.rowCount() - 1 - 2, len(saved_data['panel_data']))):
                    current_table_row = row_idx + 2  # Actual row in QTableWidget

                    panel_entry = saved_data['panel_data'][row_idx]

                    name_item = self.table.item(current_table_row, 0)
                    # Create if not exists (should be rare after setup_table_content)
                    if not name_item:
                        name_item = QTableWidgetItem()
                        self.table.setItem(current_table_row, 0, name_item)
                    name_item.setText(panel_entry.get('name', ''))

                    qty_item = self.table.item(current_table_row, 1)
                    if not qty_item:
                        qty_item = QTableWidgetItem()
                        self.table.setItem(current_table_row, 1, qty_item)
                    qty_item.setText(panel_entry.get('qty', ''))

                    for col_idx in range(2, min(self.table.columnCount(), len(panel_entry.get('areas', [])) + 2)):
                        if col_idx - 2 < len(panel_entry.get('areas', [])):
                            area_item = self.table.item(
                                current_table_row, col_idx)
                            if not area_item:
                                area_item = QTableWidgetItem()
                                self.table.setItem(
                                    current_table_row, col_idx, area_item)
                            area_item.setText(
                                panel_entry['areas'][col_idx - 2])
        finally:
            self.table.blockSignals(False)
            self.table.programmatic_change = False
            self.table.viewport().update()
            # Ensure dropdown is updated
            self.size_headers_changed.emit(self.get_available_sizes())
            self.data_changed.emit()  # Recalculate totals after restoring

    def clear_data(self):
        """Clears all data rows and size headers, keeping the structure."""
        self.table.programmatic_change = True  # Prevent undo tracking during clear
        self.table.blockSignals(True)
        try:
            # Clear size headers (row 1, columns 2+)
            for col in range(2, self.table.columnCount()):
                item = self.table.item(1, col)
                if item:
                    item.setText("")  # Clear text to show hint

            # Clear data rows (row 2 to second-to-last)
            for row in range(2, self.table.rowCount() - 1):
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    if item:
                        item.setText("")

            # Clear total row values (columns 2+)
            for col in range(2, self.table.columnCount()):
                item = self.table.item(self.table.rowCount() - 1, col)
                if item:
                    item.setText("0.00")
        finally:
            self.table.blockSignals(False)
            self.table.programmatic_change = False
            self.table.viewport().update()
            self.size_headers_changed.emit(self.get_available_sizes())
            self.data_changed.emit()

    def get_table_data_for_calculation(self):
        """
        Returns a structured dictionary of data from the top table
        suitable for calculations in BottomTableSection.
        """
        data = {
            'sizes': [],
            # Each panel is {'name': 'PNL1', 'qty': 1, 'areas': [10.0, 12.0, ...]}
            'panels': []
        }

        # Get sizes from header row
        for col in range(2, self.table.columnCount()):
            size_item = self.table.item(1, col)
            # Ensure that the actual text is retrieved, not the hint text
            size_text = size_item.text().strip() if size_item else ""
            # If it's a hint (empty or default "SIZE X"), don't include it in sizes for calculation purposes
            # The simplified get_available_sizes will already filter out empty strings,
            # so this check is mostly for robustness during calculation if a hint somehow remains.
            # Heuristic to check if it's a default hint
            if size_text.startswith("SIZE ") and not size_text.replace("SIZE ", "").isdigit():
                # Add empty string for calculation if it's just a hint
                data['sizes'].append("")
            else:
                data['sizes'].append(size_text)

        # Get panel data
        for row in range(2, self.table.rowCount() - 1):
            name_item = self.table.item(row, 0)
            qty_item = self.table.item(row, 1)

            try:
                qty = int(qty_item.text()
                          ) if qty_item and qty_item.text().isdigit() else 0
            except ValueError:
                qty = 0  # Invalid quantity

            panel_areas = []
            for col in range(2, self.table.columnCount()):
                area_item = self.table.item(row, col)
                try:
                    area = float(area_item.text()
                                 ) if area_item and area_item.text() else 0.0
                except ValueError:
                    area = 0.0  # Invalid area
                panel_areas.append(area)

            if name_item and name_item.text().strip() and qty > 0:  # Only include valid panels
                data['panels'].append({
                    'name': name_item.text().strip(),
                    'qty': qty,
                    'areas': panel_areas
                })
        return data

    def get_total_area_for_size(self, size_name: str) -> float:
        """
        Retrieves the total sewing area for a given size from the bottom row of the top table.
        
        Args:
            size_name (str): The name of the size (e.g., "S", "M", "L").
        
        Returns:
            float: The total sewing area for the specified size, or 0.0 if not found/invalid.
        """
        size_name_upper = size_name.strip().upper()

        # Find the column index for the given size
        col_index = -1
        # Start from column 2 where sizes begin
        for col in range(2, self.table.columnCount()):
            header_item = self.table.item(1, col)  # Size headers are in row 1
            if header_item and header_item.text().strip().upper() == size_name_upper:
                col_index = col
                break

        if col_index != -1:
            # Get the value from the total row in that column
            total_row = self.table.rowCount() - 1
            total_item = self.table.item(total_row, col_index)
            if total_item:
                try:
                    return float(total_item.text())
                except ValueError:
                    return 0.0  # Return 0.0 if the total value is not a valid number
        return 0.0  # Return 0.0 if the size column is not found
