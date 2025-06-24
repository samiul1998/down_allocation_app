# down_allocation_app/ui/widgets/table_widget.py

from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView, QApplication, QMessageBox
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt, pyqtSignal
from ui.dialogs.progress_dialog import ProgressDialog # Assuming this path

class TableWidget(QTableWidget):
    # Signal to notify parent of table dimension changes due to paste
    # This signal will be caught by main_window to orchestrate table resizing
    request_resize = pyqtSignal(int, int) # new_data_rows, new_size_cols

    def __init__(self, rows=0, cols=0, parent=None): # Set default rows/cols to 0 as they are setup later
        super().__init__(rows, cols, parent)
        self.setup_table_general_props() # Renamed to avoid conflict with potential setup_table in sections
        self.pasted_cells = []
        self.undo_stack = []
        self.redo_stack = []
        self.initial_state_saved = False  # Track if initial state is saved
        self.programmatic_change = False  # Flag to prevent undo tracking during restore

    def setup_table_general_props(self): # Renamed
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked |
                             QAbstractItemView.EditTrigger.EditKeyPressed)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        
        # Connect itemChanged signal to track user changes
        self.itemChanged.connect(self.on_item_changed)

    def on_item_changed(self, item):
        """Track when user manually changes items"""
        if not self.programmatic_change:
            # Save initial state if this is the first user change
            if not self.initial_state_saved:
                # Save the state before this change by temporarily reverting
                current_text = item.text()
                self.programmatic_change = True
                item.setText("")  # Temporarily clear to save previous state
                self.push_undo_state()
                item.setText(current_text)  # Restore current text
                self.programmatic_change = False
                self.initial_state_saved = True
            
            # Apply uppercase conversion for specific cells
            row, col = item.row(), item.column()
            if col == 0 or (row == 1 and col >= 2): # Panel Name or Size Header
                if item.text() != item.text().upper():
                    self.programmatic_change = True
                    item.setText(item.text().upper())
                    self.programmatic_change = False

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_C and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.copy_selection()
        elif event.key() == Qt.Key.Key_V and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.push_undo_state()
            self.paste_to_selection()
            # self.select_pasted_cells() # This is called at the end of paste_to_selection already
        elif event.key() == Qt.Key.Key_Delete:
            self.push_undo_state()
            self.clear_selection()
        elif event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_F2):
            current = self.currentIndex()
            if current.isValid() and current.row() < self.rowCount() - 1:
                self.edit(current)
        elif event.key() == Qt.Key.Key_Z and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                self.redo()
            else:
                self.undo()
        elif event.key() == Qt.Key.Key_Y and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.redo()
        elif event.key() == Qt.Key.Key_Z and event.modifiers() == (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier):
            self.redo()
        elif event.key() in range(Qt.Key.Key_0, Qt.Key.Key_9 + 1):
            current = self.currentIndex()
            if current.isValid() and current.row() < self.rowCount() - 1:
                if event.modifiers() & Qt.KeyboardModifier.KeypadModifier:
                    self.edit(current)
                    if self.cellWidget(current.row(), current.column()):
                        self.cellWidget(
                            current.row(), current.column()).keyPressEvent(event)
                    return
            super().keyPressEvent(event)
        elif event.text() and not event.modifiers():
            current = self.currentIndex()
            if current.isValid() and current.row() < self.rowCount() - 1:
                self.edit(current)
                if self.cellWidget(current.row(), current.column()):
                    self.cellWidget(current.row(), current.column()
                                    ).keyPressEvent(event)
                return
            super().keyPressEvent(event)
        elif event.key() in (Qt.Key.Key_Up, Qt.Key.Key_Down, Qt.Key.Key_Left, Qt.Key.Key_Right):
            current = self.currentIndex()
            if current.isValid():
                # Removed problematic manual commitData and closePersistentEditor calls
                # Qt's delegate system should handle this automatically when focus changes
                
                row, col = current.row(), current.column()
                if event.key() == Qt.Key.Key_Up:
                    row -= 1
                elif event.key() == Qt.Key.Key_Down:
                    row += 1
                elif event.key() == Qt.Key.Key_Left:
                    col -= 1
                elif event.key() == Qt.Key.Key_Right:
                    col += 1

                new_index = self.model().index(row, col)
                if new_index.isValid() and row < self.rowCount():
                    self.setCurrentIndex(new_index)
                    self.scrollTo(new_index)
                return
            super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def save_state(self):
        state = []
        for row in range(self.rowCount()):
            row_data = []
            for col in range(self.columnCount()):
                item = self.item(row, col)
                row_data.append(item.text() if item else "")
            state.append(row_data)
        return state

    def push_undo_state(self):
        """Only save undo state when there are actual user changes"""
        if self.programmatic_change:
            return
            
        current_state = self.save_state()
        
        # Don't save duplicate states
        if self.undo_stack and current_state == self.undo_stack[-1]:
            return
            
        self.undo_stack.append(current_state)
        self.redo_stack = []  # Clear redo stack when new action is performed
        
        # Limit undo stack size
        if len(self.undo_stack) > 100:
            self.undo_stack.pop(0)

    def undo(self):
        if not self.undo_stack:
            return
            
        # Save current state to redo stack
        current_state = self.save_state()
        self.redo_stack.append(current_state)
        
        # Get and restore previous state
        previous_state = self.undo_stack.pop()
        self.restore_state(previous_state)
        
        # Limit redo stack size
        if len(self.redo_stack) > 100:
            self.redo_stack.pop(0)

    def redo(self):
        if not self.redo_stack:
            return
            
        # Save current state to undo stack
        current_state = self.save_state()
        self.undo_stack.append(current_state)
        
        # Get and restore next state
        next_state = self.redo_stack.pop()
        self.restore_state(next_state)
        
        # Limit undo stack size
        if len(self.undo_stack) > 100:
            self.undo_stack.pop(0)

    def restore_state(self, state):
        """Restore table state without triggering undo tracking"""
        self.programmatic_change = True
        self.blockSignals(True)
        
        try:
            # Ensure row/column counts match the state before restoring
            self.setRowCount(len(state))
            if state:
                self.setColumnCount(len(state[0]))

            for row in range(self.rowCount()):
                for col in range(self.columnCount()):
                    item = self.item(row, col)
                    if not item:
                        item = QTableWidgetItem()
                        self.setItem(row, col, item)
                    # Use .setText() directly, it will be handled by the delegate's editor
                    item.setText(state[row][col])
        finally:
            self.blockSignals(False)
            self.programmatic_change = False
            self.viewport().update()
            
            # Recalculate totals in main window after state restore
            if self.window() and hasattr(self.window(), 'update_all_tables_and_dropdowns'):
                self.window().update_all_tables_and_dropdowns()


    def copy_selection(self):
        selection = self.selectedIndexes()
        if not selection:
            return
        rows = sorted(index.row() for index in selection)
        cols = sorted(index.column() for index in selection)
        min_row, max_row = rows[0], rows[-1]
        min_col, max_col = cols[0], cols[-1]
        clipboard = QApplication.clipboard()
        text = ""
        for r in range(min_row, max_row + 1):
            row_text = []
            for c in range(min_col, max_col + 1):
                item = self.item(r, c)
                row_text.append(item.text() if item else "")
            text += "\t".join(row_text) + "\n"
        clipboard.setText(text.strip())

    def paste_to_selection(self):
        try:
            progress = ProgressDialog("Pasting Data", "Processing paste operation...", self.window())
            progress.show()
            QApplication.processEvents()
            progress.update_progress(5)

            selection = self.selectedIndexes()
            if not selection:
                progress.close()
                return

            first_row = selection[0].row()
            first_col = selection[0].column()
            clipboard = QApplication.clipboard()
            text = clipboard.text()
            
            if not text.strip():
                progress.close()
                return

            rows = [row for row in text.split('\n') if row.strip()]
            grid = [row.split('\t') for row in rows]
            progress.update_progress(15)

            # Determine if paste target is the size header row (row 1)
            is_size_header_paste = (first_row == 1)

            if is_size_header_paste:
                is_vertical = all(len(row) == 1 for row in grid) and len(grid) > 1
                if is_vertical:
                    transposed = []
                    # Handle transposition for vertical paste into a horizontal header row
                    max_len_in_grid = max(len(r_data) for r_data in grid) if grid else 0
                    if max_len_in_grid == 1: # Only transpose if single column data
                        transposed = [[] for _ in range(1)] # Initialize with one row for the transposed data
                        for r_data in grid:
                            if r_data:
                                transposed[0].append(r_data[0])
                        grid = transposed
                    # If it's not single column or already horizontal, keep as is
            progress.update_progress(20)

            needed_rows_for_paste = len(grid)
            # Find the maximum column count from the pasted data
            needed_cols_for_paste = 0
            if grid:
                for r_data in grid:
                    needed_cols_for_paste = max(needed_cols_for_paste, len(r_data))


            # Calculate potential new dimensions based on paste operation
            # Existing data rows and size columns (excluding fixed headers/totals)
            current_data_rows = self.rowCount() - 3
            current_size_cols = self.columnCount() - 2

            # Calculate target dimensions
            # For data rows: if pasting into data rows, it's the max of current data rows
            # or the row number of the last pasted cell minus header rows.
            target_data_rows = current_data_rows
            if first_row >= 2 and first_row < self.rowCount() - 1: # Pasting into data rows
                target_data_rows = max(current_data_rows, (first_row + needed_rows_for_paste) - 2)

            # For size columns: if pasting into size headers or data, it's the max of current size cols
            # or the column index of the last pasted cell minus fixed columns.
            target_size_cols = current_size_cols
            if first_col >= 2: # Pasting into size columns (header or data)
                target_size_cols = max(current_size_cols, (first_col + needed_cols_for_paste) - 2)


            # Check if resize is actually needed
            if target_data_rows > current_data_rows or target_size_cols > current_size_cols:
                progress.label.setText("Adjusting table size due to paste...")
                progress.update_progress(25)
                # Emit signal to parent (main_window) to request resize
                self.request_resize.emit(target_data_rows, target_size_cols)
                # Allow the main window to handle the resize. This method will effectively pause
                # until the resize is complete (due to QApplication.processEvents and synchronous calls).
                QApplication.processEvents() # Allow resize to process

            progress.update_progress(50)
            progress.label.setText("Pasting data...")

            self.pasted_cells = []
            total_cells = needed_rows_for_paste * needed_cols_for_paste if grid else 1
            processed_cells = 0
            
            self.programmatic_change = True # Set programmatic flag BEFORE modifying items
            self.blockSignals(True) # Block signals during paste operation
            
            try:
                for r, row_data in enumerate(grid):
                    for c, value in enumerate(row_data):
                        current_row = first_row + r
                        current_col = first_col + c

                        processed_cells += 1
                        if processed_cells % 10 == 0:
                            progress_val = 50 + (40 * processed_cells / total_cells)
                            progress.update_progress(min(90, int(progress_val)))
                            QApplication.processEvents()

                        if (current_row >= self.rowCount() or 
                            current_col >= self.columnCount() or
                            current_row == 0 or # Cannot paste into main merged header (row 0)
                            current_row == self.rowCount() - 1): # Cannot paste into total row
                            continue

                        # Apply validation rules (simplified from original for brevity, but should be complete)
                        # Ensure proper validation based on column types
                        if current_row == 1 and current_col >= 2: # Size Header Row
                            # Any text is allowed, will be uppercased by delegate
                            pass 
                        elif current_col == 1:  # Panel Quantity column (1-9)
                            if not value.isdigit() or not (1 <= int(value) <= 9):
                                continue # Skip invalid qty
                        elif current_col >= 2:  # Sewing area columns (float)
                            try:
                                float(value)
                            except ValueError:
                                continue # Skip invalid float

                        if not self.item(current_row, current_col):
                            self.setItem(current_row, current_col, QTableWidgetItem())

                        # Apply uppercase if it's a panel name or size header
                        if current_col == 0 or (current_row == 1 and current_col >= 2):
                            self.item(current_row, current_col).setText(value.strip().upper())
                        else:
                            self.item(current_row, current_col).setText(value.strip())
                        
                        self.pasted_cells.append((current_row, current_col))
            finally:
                self.blockSignals(False) # Unblock signals after paste
                self.programmatic_change = False # Reset programmatic flag

            progress.update_progress(95)
            self.select_pasted_cells()
            
            # Request totals calculation and dropdown update after paste
            # This covers the dropdown update for size headers (Issue 1)
            if self.window() and hasattr(self.window(), 'update_all_tables_and_dropdowns'):
                self.window().update_all_tables_and_dropdowns()
            
            progress.update_progress(100)

        except Exception as e:
            QMessageBox.warning(self.window(), "Paste Error", f"Failed to paste data: {str(e)}")
            if 'progress' in locals():
                progress.close()

    def select_pasted_cells(self):
        if not self.pasted_cells:
            return
        self.clearSelection()
        for row, col in self.pasted_cells:
            item = self.item(row, col)
            if item:
                item.setSelected(True)

    def clear_selection(self):
        for index in self.selectedIndexes():
            if index.row() == 0 or index.row() == self.rowCount() - 1: # Cannot clear headers or total row
                continue
            if self.item(index.row(), index.column()):
                self.item(index.row(), index.column()).setText("")