# plateQLineEdit.py
"""
Custom QLineEdit widget for handling license plate input with validation.
"""

from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QLineEdit

# Unicode ranges for various character sets
SPACE_CODEPOINTS = '\u0020\u2000-\u200F\u2028-\u202F'
STANDARD_ALPHA_CODEPOINTS = 'A-Za-z'  # Standard Latin alphabet
STANDARD_NUM_CODEPOINTS = '0-9'  # Standard digits

# Define styles
FOCUS_STYLE = """
    background-color: rgb(153, 193, 241);
    border-color: rgb(0, 0, 0);
    border-width: 1px;
    border-style: solid;
"""

UNFOCUS_STYLE = """
    background-color: white;
    border-color: rgb(0, 0, 0);
    border-width: 1px;
    border-style: solid;
"""


class plateQLineEdit(QLineEdit):
    """
    Custom QLineEdit for license plate and related input fields with validation.
    
    This class extends QLineEdit to provide specific validation for different
    types of input fields used in the license plate management system.
    """

    def __init__(self, arg__1, parent=None, *args, **kwargs):
        """
        Initialize the custom QLineEdit.

        Args:
            arg__1: Initial text
            parent: Parent widget
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments
        """
        super().__init__(arg__1, parent, *args, **kwargs)

    def persianRegValidator(self, regExType):
        """
        Get the appropriate regular expression validator based on field type.

        Args:
            regExType (str): Type of input field to validate

        Returns:
            QRegularExpression: Validator for the specified field type
        """
        # Text-only fields (names)
        if regExType in ['fNameTextBox', 'lNameTextBox']:
            return QRegularExpression(f'^[{STANDARD_ALPHA_CODEPOINTS}{SPACE_CODEPOINTS}]*$')

        # License plate character field
        if regExType == 'plateTextNum_2':
            return QRegularExpression(f'^[{STANDARD_ALPHA_CODEPOINTS}{SPACE_CODEPOINTS}]*$')

        # Numeric-only fields
        if regExType in ['buildingTextBox', 'numTextBox', 'blockTextBox']:
            return QRegularExpression(f'^[{STANDARD_NUM_CODEPOINTS}]*$')

        # License plate number fields
        if regExType in ['plateTextNum_1', 'plateTextNum_3', 'plateTextNum_4']:
            return QRegularExpression(f'^[{STANDARD_NUM_CODEPOINTS}]*$')

        # Mixed content field (car model)
        if regExType == 'carModelTextBox':
            return QRegularExpression(
                f'^[{STANDARD_ALPHA_CODEPOINTS}{SPACE_CODEPOINTS}{STANDARD_NUM_CODEPOINTS}]*$')

    def keyPressEvent(self, event):
        """
        Handle key press events with validation.

        Args:
            event: Key press event
        """
        regExField = self.persianRegValidator(self.objectName())
        validator = QRegularExpressionValidator(regExField)
        state = validator.validate(event.text(), 0)
        
        # Allow input if it matches the validator or is backspace/enter
        if state[0] == QRegularExpressionValidator.Acceptable or state[1] in ('\x08', '\r'):
            super().keyPressEvent(event)

    def focusInEvent(self, event):
        """
        Handle focus in event by changing the background color.

        Args:
            event: Focus event
        """
        self.setStyleSheet(FOCUS_STYLE)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        """
        Handle focus out event by restoring the normal background color.

        Args:
            event: Focus event
        """
        self.setStyleSheet(UNFOCUS_STYLE)
        super().focusOutEvent(event)

    def is_not_blank(self, fieldString):
        """
        Check if a string is not blank or only whitespace.

        Args:
            fieldString (str): String to check

        Returns:
            bool: True if string contains non-whitespace characters
        """
        return bool(fieldString and not fieldString.isspace())

    def getText(self):
        """
        Get the text content if it's not blank.

        Returns:
            str: Text content if not blank, None otherwise
        """
        selfText = self.text()
        if self.is_not_blank(selfText):
            return selfText
        else:
            self.setFocus()
            return None