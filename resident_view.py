# resident_view.py
"""
Module for displaying resident information in a community system.
Provides a dialog window to view resident details.
"""

import sys
from PySide6.QtWidgets import QApplication, QDialog
from qtpy.uic import loadUi

from configParams import Parameters
from database.db_resident_utils import dbGetResidentDatasByPlate
from helper.gui_maker import get_status_text
from helper.text_decorators import (
    convert_to_standard_format,
    split_string_language_specific,
    join_elements
)

params = Parameters()


class residentView(QDialog):
    """
    Dialog window for viewing resident information.
    Displays personal details, residence information, and vehicle data.
    """

    def __init__(self, parent=None, residnetPlate='s'):
        """
        Initialize the resident view window.

        Args:
            parent: Parent widget (optional)
            residnetPlate (str): License plate number of the resident
        """
        super(residentView, self).__init__()

        # Load UI and configure window
        loadUi('./gui/residentView.ui', self)
        self.setFixedSize(self.size())

        # Get resident data using plate number
        resident_data = dbGetResidentDatasByPlate(
            join_elements(convert_to_standard_format(split_string_language_specific(residnetPlate)))
        )

        # Populate resident information
        self.populate_resident_info(resident_data)

    def populate_resident_info(self, resident_data):
        """
        Populate the UI fields with resident information.

        Args:
            resident_data: Resident object containing all relevant information
        """
        # Personal Information
        self.labelFname.setText(resident_data.getFirstName())
        self.labelLname.setText(resident_data.getLastName())
        
        # Residence Information
        self.labelBuilding.setText(resident_data.getBuilding(appendBuilding=True))
        self.labelBlock.setText(resident_data.getBlock())
        self.labelNum.setText(resident_data.getNum())
        
        # Vehicle Information
        self.labelCarModel.setText(resident_data.getCarModel())
        self.labelPlateNum.setText(resident_data.getPlateNumber(display=True))
        
        # Status Information
        self.labelStatus.setText(get_status_text(resident_data.getStatus(item=False)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = residentView()
    window.setWindowTitle('New Resident Registration')  # Changed from Persian to English
    window.show()
    sys.exit(app.exec_())