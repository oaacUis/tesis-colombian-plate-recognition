# residents_edit.py
"""
Module for managing resident information in a community system.
Provides functionality for adding, editing, and viewing resident details.
"""

import sys
from pathlib import Path

import pandas as pd
from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QApplication
from qtpy.uic import loadUi

from configParams import getFieldNames, Parameters
from database.classResidents import Resident
from database.db_resident_utils import insertResident, dbGetPlateExist, dbGetResidentDatasByPlate
from gui import plateQLineEdit
from helper.text_decorators import (
    convert_to_standard_format,
    split_string_language_specific,
    join_elements,
    reshape_text
)

params = Parameters()


class residentsAddNewWindow(QDialog):
    """
    Dialog window for adding and editing resident information.
    """

    def __init__(self, parent=None, isEditing=False, isNew=False, isInfo=False, residnetPlate='s'):
        """
        Initialize the resident management window.

        Args:
            parent: Parent widget
            isEditing (bool): Whether in edit mode
            isNew (bool): Whether adding new resident
            isInfo (bool): Whether in view-only mode
            residnetPlate (str): License plate number
        """
        super(residentsAddNewWindow, self).__init__()

        self.isEditing = isEditing
        self.isNew = isNew
        self.isInfo = isInfo
        self.residnetPlateEng = join_elements(
            convert_to_standard_format(split_string_language_specific(residnetPlate))
        )

        # Setup UI
        loadUi('./gui/residentNew.ui', self)
        self.setFixedSize(self.size())
        self.setup_ui_elements()

        # Configure window based on mode
        if self.isEditing:
            self.configure_edit_mode()
        if self.isNew:
            self.configure_new_mode()

    def setup_ui_elements(self):
        """Configure initial UI elements."""
        self.addResidentButton.clicked.connect(self.addUser)
        self.addResidentButton.setIcon(QPixmap("./icons/icons8-add-user-male-80.png"))
        self.addResidentButton.setIconSize(QSize(30, 30))

        self.plateTextView.setStyleSheet(
            f"""border-image: url("{Path().absolute()}/Templates/template-base.png") 0 0 0 0 stretch stretch;"""
        )

        # Setup comboboxes
        fieldsList = ['fName', 'lName', 'building', 'block', 'num', 'carModel', 'plateNum', 'status']
        fieldsList = getFieldNames(fieldsList)
        self.plateAlphabetComboBox.addItems(params.plateAlphabet.values())
        self.statusComboBox.addItems(list(params.fieldStatus.values())[:2])

    def configure_edit_mode(self):
        """Configure window for editing existing resident."""
        self.setWindowTitle('Edit Resident')
        self.addResidentButton.setText('Save Changes')
        self.addResidentButton.setIcon(QPixmap("./icons/icons8-change-user-80.png"))
        self.addResidentButton.setIconSize(QSize(30, 30))

        self.editingResident = dbGetResidentDatasByPlate(self.residnetPlateEng)
        self.populate_resident_data()

        if self.isInfo:
            self.setWindowTitle('View Resident Information')
            self.addResidentButton.hide()
            self.setEnabled(False)

    def configure_new_mode(self):
        """Configure window for adding new resident."""
        self.setWindowTitle('Add New Resident')
        self.newResident = reshape_text(self.residnetPlateEng)
        self.populate_plate_data()

    def populate_resident_data(self):
        """Populate form fields with existing resident data."""
        self.fNameTextBox.setText(self.editingResident.getFirstName())
        self.lNameTextBox.setText(self.editingResident.getLastName())
        self.buildingTextBox.setText(self.editingResident.getBuilding(appendBuilding=False))
        self.blockTextBox.setText(self.editingResident.getBlock())
        self.numTextBox.setText(self.editingResident.getNum())
        self.carModelTextBox.setText(self.editingResident.getCarModel())
        self.statusComboBox.setCurrentIndex(int(self.editingResident.getStatus(item=False)))
        
        self.populate_plate_data(self.editingResident.getPlateNumber(display=False))

    def populate_plate_data(self, plate_number=None):
        """Populate license plate fields."""
        if plate_number is None:
            plate_number = self.newResident
            
        self.plateTextNum_1.setText(plate_number[:2])
        self.plateTextNum_3.setText(plate_number[3:6])
        self.plateTextNum_4.setText(plate_number[6:8])

        if self.isEditing:
            inv_map = {v: k for k, v in params.plateAlphabet.items()}
            plate_alphabet = inv_map[plate_number[2]]
            self.plateAlphabetComboBox.setCurrentText(params.plateAlphabet[plate_alphabet])
        else:
            self.plateAlphabetComboBox.setCurrentText(plate_number[2])

    def addUser(self):
        """Handle adding or updating resident information."""
        # Collect form data
        resident_data = self.collect_form_data()
        if not all(resident_data.values()):
            self.show_status_message("Please fill all fields", "error")
            return

        # Create resident object
        resident = Resident(
            resident_data['first_name'],
            resident_data['last_name'],
            resident_data['building'],
            resident_data['block'],
            resident_data['unit'],
            resident_data['car_model'],
            resident_data['plate_number'],
            resident_data['status_index']
        )

        if self.isEditing:
            self.handle_edit_resident(resident)
        else:
            self.handle_new_resident(resident)

        # Export to CSV
        self.export_to_csv(resident_data)

    def collect_form_data(self):
        """Collect and return form field data."""
        inv_map = {v: k for k, v in params.plateAlphabet.items()}
        plate_alphabet = inv_map[self.plateAlphabetComboBox.currentText()]
        
        plate_number = f"{self.plateTextNum_1.getText()}{plate_alphabet}{self.plateTextNum_3.getText()}{self.plateTextNum_4.getText()}"
        
        return {
            'first_name': self.fNameTextBox.getText(),
            'last_name': self.lNameTextBox.getText(),
            'building': self.buildingTextBox.getText(),
            'block': self.blockTextBox.getText(),
            'unit': self.numTextBox.getText(),
            'car_model': self.carModelTextBox.getText(),
            'plate_number': plate_number,
            'status_index': self.statusComboBox.currentIndex()
        }

    def handle_edit_resident(self, resident):
        """Handle editing existing resident."""
        insertResident(resident, True, self.residnetPlateEng)
        self.show_status_message("Resident updated successfully", "success")
        self.clear_form()

    def handle_new_resident(self, resident):
        """Handle adding new resident."""
        if not dbGetPlateExist(resident.plateNum):
            insertResident(resident)
            self.show_status_message("New resident added successfully", "success")
            self.clear_form()
        else:
            self.show_status_message("License plate already exists", "error")

    def show_status_message(self, message, status):
        """Display status message with appropriate styling."""
        self.statusLabel.setText(message)
        if status == "success":
            self.statusLabel.setStyleSheet("background-color: rgb(51, 209, 122);")
        elif status == "error":
            self.statusLabel.setStyleSheet("""
                background-color: rgb(224, 27, 36);
                color: white;
                font-weight: bold;
                padding: 0 2px;
            """)

    def clear_form(self):
        """Clear all form fields."""
        for item in self.findChildren(plateQLineEdit.plateQLineEdit):
            item.setText('')

    def export_to_csv(self, data):
        """Export resident data to CSV file."""
        df = pd.DataFrame({
            'fName': [data['first_name']],
            'lName': [data['last_name']],
            'building': [data['building']],
            'block': [data['block']],
            'num': [data['unit']],
            'carModel': [data['car_model']],
            'plateNum': [data['plate_number']],
            'status': [data['status_index']]
        })
        
        df.to_csv(
            str(Path().absolute()) + '/base/residents.csv',
            header=False,
            index=False,
            mode='a',
            encoding='utf-8'
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = residentsAddNewWindow()
    window.setWindowTitle('Add New Resident')  # Changed from Persian to English
    window.show()
    sys.exit(app.exec_())