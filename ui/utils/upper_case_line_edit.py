# down_allocation_app/ui/utils/upper_case_line_edit.py

from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QKeyEvent, QFont # Import QFont
from PyQt6.QtCore import Qt
from styles import AppStyles # Assuming styles.py is in the parent directory or accessible

class UpperCaseLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Removed self.setStyleSheet(AppStyles.UPPERCASE_LINE_EDIT_STYLE)
        # to allow global font settings to apply consistently.
        self.textChanged.connect(self.force_uppercase)

        # Optionally, if you still want to ensure Courier New for this widget itself
        # without interfering with its editor role, you can set its font directly.
        # However, the QApplication font should handle this.
        # self.setFont(QFont("Courier New"))


    def force_uppercase(self, text):
        if text != text.upper():
            cursor_pos = self.cursorPosition()
            self.blockSignals(True)
            self.setText(text.upper())
            self.setCursorPosition(cursor_pos)
            self.blockSignals(False)

    def keyPressEvent(self, event: QKeyEvent):
        if event.text():
            upper_char = event.text().upper()
            modified_event = QKeyEvent(
                event.type(),
                event.key(),
                event.modifiers(),
                upper_char
            )
            super().keyPressEvent(modified_event)
            return
        super().keyPressEvent(event)

    def insertFromMimeData(self, source):
        if source.hasText():
            self.insertPlainText(source.text().upper())