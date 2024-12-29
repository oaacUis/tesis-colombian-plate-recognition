# classEntries.py
# This class manages database entry data for display in the main window table.
# It provides methods to format and retrieve data in specific formats.

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QTableWidgetItem

from helper import jalali
from helper.gui_maker import get_status_color, get_status_text
from helper.text_decorators import convert_to_local_format, split_string_language_specific


class Entries:
    """
    A class to represent database entries and their display formatting.
    
    Attributes:
        status (int): Entry status code (0: Unauthorized, 1: Authorized, 2: Unregistered)
        plateNum (str): License plate number
        eTime (str): Entry time
        eDate (str): Entry date
        charPercent (float): Character recognition confidence percentage
        platePercent (float): Plate detection confidence percentage
    """

    def __init__(self, platePercent, charPercent, eDate, eTime, plateNum, status):
        """
        Initialize an Entries object with the given parameters.

        Args:
            platePercent (float): Plate detection confidence percentage
            charPercent (float): Character recognition confidence percentage
            eDate (str): Entry date
            eTime (str): Entry time
            plateNum (str): License plate number
            status (int): Entry status code
        """
        self.status = status
        self.plateNum = plateNum
        self.eTime = eTime
        self.eDate = eDate
        self.charPercent = charPercent
        self.platePercent = platePercent

    def getTime(self):
        """
        Get the entry time.

        Returns:
            str: The entry time
        """
        return self.eTime

    def getDate(self, persian=True):
        """
        Get the entry date in either Persian or Gregorian format.

        Args:
            persian (bool): If True, returns date in Persian format, otherwise Gregorian

        Returns:
            str: The formatted date string
        """
        if persian:
            return jalali.Gregorian(self.eDate).persian_string()
        return self.eDate

    def getPlatePic(self):
        """
        Get the path to the license plate image.

        Returns:
            str: Path to the plate image file
        """
        return 'temp/{}_{}_{}.jpg'.format(self.plateNum, self.eTime, self.eDate)

    def getCharPercent(self):
        """
        Get the character recognition confidence percentage.

        Returns:
            str: Formatted percentage string
        """
        return "{}%".format(self.charPercent)

    def getPlatePercent(self):
        """
        Get the plate detection confidence percentage.

        Returns:
            str: Formatted percentage string
        """
        return "{}%".format(self.platePercent)

    def getPlateNumber(self, display=False):
        """
        Get the license plate number in either standard or display format.

        Args:
            display (bool): If True, returns plate number in display format

        Returns:
            str: Formatted license plate number
        """
        return convert_to_local_format(split_string_language_specific(self.plateNum), display)

    def getStatus(self, item=True, statusNum='', selfNum=False):
        """
        Get the entry status as either a QTableWidgetItem or raw value.

        Args:
            item (bool): If True, returns a formatted QTableWidgetItem
            statusNum (str): Optional status number to use instead of self.status
            selfNum (bool): If True, uses self.status instead of statusNum

        Returns:
            Union[QTableWidgetItem, int]: Status as either a formatted table item or raw value
        """
        if item:
            statusData = self.status if selfNum else statusNum
            r, g, b = get_status_color(statusData)
            statusText = get_status_text(statusData)
            statusItem = QTableWidgetItem(statusText)
            statusItem.setBackground(QColor(r, g, b))
            return statusItem
        return self.status