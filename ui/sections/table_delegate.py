# down_allocation_app/ui/sections/table_delegate.py

from PyQt6.QtWidgets import QStyledItemDelegate, QTableWidgetItem
from PyQt6.QtGui import QFont, QDoubleValidator, QIntValidator, QKeyEvent, QPalette, QColor
from PyQt6.QtCore import Qt, QEvent
from styles import AppStyles # Assuming styles.py is in the parent directory or accessible
from ui.utils.upper_case_line_edit import UpperCaseLineEdit # Assuming this path


class TableItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        # Don't create editor for main header row (0) or total row
        if index.row() == 0 or index.row() == self.parent().rowCount() - 1:
            return None
        # Always allow editing for size headers (row 1, columns 2+)
        if index.row() == 1 and index.column() >= 2:
            editor = super().createEditor(parent, option, index)
            return editor
        # For data rows (row 2+)
        if index.row() >= 2 and index.row() < self.parent().rowCount() - 1:
            editor = super().createEditor(parent, option, index)
            # Set validation based on column
            if index.column() == 1:  # Panel Quantity column (1-9)
                validator = QIntValidator(1, 9, parent)
                editor.setValidator(validator)
            elif index.column() >= 2:  # Sewing area columns
                validator = QDoubleValidator(0, 9999, 2, parent)
                validator.setNotation(QDoubleValidator.Notation.StandardNotation)
                editor.setValidator(validator)
            return editor
        return None

    def eventFilter(self, editor, event):
        # Intercept key press in editor
        if isinstance(event, QKeyEvent):
            if event.key() in (Qt.Key.Key_Left, Qt.Key.Key_Right,
                               Qt.Key.Key_Up, Qt.Key.Key_Down):
                # Commit data before navigating
                self.commitData.emit(editor)
                self.closeEditor.emit(editor, QStyledItemDelegate.EndEditHint.NoHint)
                # Return True to consume the event
                return True
        return super().eventFilter(editor, event)

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        # Set text alignment to center for all cells
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter
        # Show hint text for empty cells with gray color
        if not index.data(Qt.ItemDataRole.DisplayRole):
            option.palette.setColor(QPalette.ColorRole.Text, AppStyles.TABLE_HINT_TEXT_COLOR)
            if index.row() == 1 and index.column() >= 2:  # Size headers
                option.text = f"SIZE {index.column()-1}"
            elif index.row() >= 2 and index.row() < self.parent().rowCount() - 1:
                if index.column() == 0:  # Panel Name
                    option.text = "PANEL NAME"
                elif index.column() == 1:  # Panel Quantity
                    option.text = "0"
                elif index.column() >= 2:  # Sewing area
                    option.text = "0.00"

class UpperCaseItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        # Apply to Panel Name column (column 0) and Size Headers (row 1, columns ≥2)
        if index.column() == 0 or (index.row() == 1 and index.column() >= 2):
            editor = UpperCaseLineEdit(parent)
            return editor
        return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        if isinstance(editor, UpperCaseLineEdit):
            editor.blockSignals(True)
            editor.setText(index.data(Qt.ItemDataRole.DisplayRole) or "")
            editor.blockSignals(False)
        else:
            super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        if isinstance(editor, UpperCaseLineEdit):
            model.setData(index, editor.text().strip().upper(), Qt.ItemDataRole.EditRole)
        else:
            super().setModelData(editor, model, index)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def eventFilter(self, editor, event):
        if isinstance(editor, UpperCaseLineEdit):
            if event.type() == QEvent.Type.KeyPress:
                if event.text():
                    editor.keyPressEvent(event)
                    self.commitData.emit(editor)
                    return True
            elif event.type() == QEvent.Type.FocusOut:
                self.commitData.emit(editor)
                self.closeEditor.emit(editor, QStyledItemDelegate.EndEditHint.NoHint)
                return True
        return super().eventFilter(editor, event)