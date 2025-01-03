<<<<<<< HEAD
=======
# classResidents.py
"""
This module defines the Resident class for managing resident information in a building management system.
"""

>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QTableWidgetItem

from helper.gui_maker import get_status_text, get_status_color
<<<<<<< HEAD
from helper.text_decorators import convert_english_to_persian, split_string_language_specific


class Resident:

    def __init__(self, fName, lName, building, block, num, carModel, plateNum, status
                 ):
=======
from helper.text_decorators import convert_to_local_format, split_string_language_specific


class Resident:
    """
    A class to represent building residents and their associated information.

    Attributes:
        fName (str): First name of the resident
        lName (str): Last name of the resident
        building (str): Building identifier
        block (str): Block identifier
        num (str): Unit number
        carModel (str): Car model of the resident
        plateNum (str): License plate number
        status (int): Resident status code (0: Unauthorized, 1: Authorized, 2: Unregistered)
    """

    def __init__(self, fName, lName, building, block, num, carModel, plateNum, status):
        """
        Initialize a Resident object with the given parameters.

        Args:
            fName (str): First name
            lName (str): Last name
            building (str): Building identifier
            block (str): Block identifier
            num (str): Unit number
            carModel (str): Car model
            plateNum (str): License plate number
            status (int): Resident status code
        """
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
        self.fName = fName
        self.lName = lName
        self.building = building
        self.block = block
        self.num = num
        self.carModel = carModel
        self.plateNum = plateNum
        self.status = status

    def getFirstName(self):
<<<<<<< HEAD
        return self.fName

    def getLastName(self):
        return self.lName

    def getFullName(self):
        return '{} {}'.format(self.fName, self.lName)

    def getBuilding(self, appendBuilding=True):
        if appendBuilding:
            return '{}{}'.format(self.building, ' طبقه ')
        else:
            return str(self.building)

    def getBlock(self):
        return str(self.block)

    def getNum(self):
        return str(self.num)

    def getCarModel(self):
        return self.carModel

    def getPlateNumber(self, display=False):
        return convert_english_to_persian(split_string_language_specific(self.plateNum), display)

    def getStatus(self, item=True):
=======
        """
        Get the resident's first name.

        Returns:
            str: First name
        """
        return self.fName

    def getLastName(self):
        """
        Get the resident's last name.

        Returns:
            str: Last name
        """
        return self.lName

    def getFullName(self):
        """
        Get the resident's full name (first name + last name).

        Returns:
            str: Full name formatted as 'first_name last_name'
        """
        return '{} {}'.format(self.fName, self.lName)

    def getBuilding(self, appendBuilding=True):
        """
        Get the building identifier with optional floor text.

        Args:
            appendBuilding (bool): If True, appends 'Floor' to the building number

        Returns:
            str: Building identifier with or without 'Floor' text
        """
        if appendBuilding:
            return '{} {}'.format(self.building, 'Floor')
        return str(self.building)

    def getBlock(self):
        """
        Get the block identifier.

        Returns:
            str: Block identifier
        """
        return str(self.block)

    def getNum(self):
        """
        Get the unit number.

        Returns:
            str: Unit number
        """
        return str(self.num)

    def getCarModel(self):
        """
        Get the resident's car model.

        Returns:
            str: Car model
        """
        return self.carModel

    def getPlateNumber(self, display=False):
        """
        Get the license plate number in either standard or display format.

        Args:
            display (bool): If True, returns plate number in display format

        Returns:
            str: Formatted license plate number
        """
        return convert_to_local_format(split_string_language_specific(self.plateNum), display)

    def getStatus(self, item=True):
        """
        Get the resident's status as either a QTableWidgetItem or raw value.

        Args:
            item (bool): If True, returns a formatted QTableWidgetItem

        Returns:
            Union[QTableWidgetItem, str]: Status as either a formatted table item or raw string value
        """
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
        if item:
            statusData = self.status
            r, g, b = get_status_color(statusData)
            statusText = get_status_text(statusData)
            statusItem = QTableWidgetItem(statusText)
            statusItem.setBackground(QColor(r, g, b))
            return statusItem
<<<<<<< HEAD
        return str(self.status)
=======
        return str(self.status)
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
