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
        self.residnetPlate = residnetPlate
       

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
        # Configurar el statusComboBox
        
        self.statusComboBox.setFrame(True)
        self.statusComboBox.addItems(list(params.fieldStatus.values())[:3])

    def configure_edit_mode(self):
        """Configure window for editing existing resident."""
        self.setWindowTitle('Edit Resident')
        self.addResidentButton.setText('Save Changes')
        self.addResidentButton.setIcon(QPixmap("./icons/icons8-change-user-80.png"))
        self.addResidentButton.setIconSize(QSize(30, 30))

        self.editingResident = dbGetResidentDatasByPlate(self.residnetPlate)
        self.populate_resident_data()

        if self.isInfo:
            self.setWindowTitle('View Resident Information')
            self.addResidentButton.hide()
            self.setEnabled(False)

    def configure_new_mode(self):
        """Configure window for adding new resident."""
        self.setWindowTitle('Add New Resident')
        self.newResident = self.residnetPlate
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
        self.populate_plate_data(self.residnetPlate)
        #print(f"Status: {self.editingResident.getStatus(item=False)}")
        
        # # Get plate directly from database
        # entries = dbGetAllEntries(limit=10, whereLike='')
        # if entries and len(entries) > 0:
        #     plate_number = entries[0].getPlateNumber(display=True)
        #     print(f"Plate from db: {plate_number}")
        #     self.populate_plate_data(plate_number)

    def populate_plate_data(self, plate_number=None):
        """
        Populate license plate fields with plate number.
        Args:
            plate_number (str): License plate number in display format
        """
        if plate_number is None:
            # print(f"Plate number is None")
            # print(f"residnetPlate: {self.residnetPlate}")
            plate_number = self.residnetPlate
            self.plateTextNum_1.setText(plate_number[:3])
            self.plateTextNum_4.setText(plate_number[-3:])
            

        
        if plate_number:
            #print(f"Si hay plate number: {plate_number}")
            self.plateTextNum_1.setText(plate_number[:3])
            self.plateTextNum_4.setText(plate_number[-3:])


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

        #print(f"Resident data: {resident_data}")   
        # Export to CSV
        self.export_to_csv(resident_data)

    def collect_form_data(self):
        """Collect and return form field data."""
        
        
        plate_number = f"{self.plateTextNum_1.getText()}{self.plateTextNum_4.getText()}"
        #print(f"plate_number en collect_form_data: {plate_number}")
        
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
        try:
            # Asegurar que tenemos la placa correcta para la actualización
            old_plate = self.residnetPlate
            insertResident(resident, True, old_plate)
            self.show_status_message("Resident updated successfully", "success")
            self.close()  # Cerrar la ventana después de actualizar
        except Exception as e:
            print(f"Error updating resident: {e}")
            self.show_status_message("Error updating resident", "error")

    def handle_new_resident(self, resident):
        """Handle adding new resident."""
        if not dbGetPlateExist(self.residnetPlate):
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
    window.setWindowTitle('Add New Resident')  
    window.show()
    sys.exit(app.exec_())