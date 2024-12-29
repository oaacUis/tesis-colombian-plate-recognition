# residents_main.py
"""
Main module for managing residents in a community system.
Provides a window interface for viewing and managing resident information.
"""

import functools
import sys

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QDialog, QApplication, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QMessageBox
)
from qtpy.uic import loadUi

from configParams import getFieldNames, Parameters
from database.db_resident_utils import dbGetAllResidents, dbRemoveResident
from enteries_window import EnteriesWindow
from helper.gui_maker import (
    CenterAlignDelegate,
    create_styled_button,
    center_widget
)
from helper.text_decorators import (
    convert_to_standard_format,
    split_string_language_specific,
    join_elements
)
from residents_edit import residentsAddNewWindow

params = Parameters()


class residentsWindow(QDialog):
    """
    Main window for managing community residents.
    Displays a table with resident information and provides management functions.
    """

    def __init__(self):
        """Initialize the residents management window."""
        super(residentsWindow, self).__init__()

        # Load and configure UI
        loadUi('./gui/residents.ui', self)
        self.setFixedSize(self.size())
        self.residentWindow = None
        
        # Configure add resident button
        self.setup_add_button()
        
        # Configure table
        self.setup_table()
        
        # Connect search functionality
        self.searchTextBox.textChanged.connect(self.searchLastName)

    def setup_add_button(self):
        """Configure the add resident button."""
        self.addResidentButton.clicked.connect(self.residentAddEditWindow)
        self.addResidentButton.setIcon(QPixmap("./icons/icons8-add-user-male-80.png"))
        self.addResidentButton.setStyleSheet(
            "text-align:right; padding-right: 25px; qproperty-iconSize: 25px;"
        )

    def setup_table(self):
        """Configure the residents table."""
        # Define table columns
        field_list = [
            'fName', 'lName', 'building', 'block', 'num',
            'carModel', 'plateNum', 'status', 'editBtn',
            'deleteBtn', 'findEntriesBtn'
        ]
        header_labels = getFieldNames(field_list)

        # Configure table properties
        self.tableWidget.setColumnCount(len(header_labels))
        self.tableWidget.setHorizontalHeaderLabels(header_labels)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )
        self.tableWidget.setLayoutDirection(Qt.RightToLeft)
        self.tableWidget.setSortingEnabled(True)

        # Set table delegate and behavior
        delegate = CenterAlignDelegate(self.tableWidget)
        self.tableWidget.setItemDelegate(delegate)
        self.tableWidget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Load initial data
        self.refresh_table()

    def btnDeleteClicked(self, event, source_object=None):
        """Handle delete button click event."""
        indexes = self.tableWidget.selectionModel().selectedRows(column=6)
        model = self.tableWidget.model()
        
        for index in indexes:
<<<<<<< HEAD
            selectedCellPlate = model.data(index, role)

            messageBox = QMessageBox(self)
            messageBox.setWindowTitle("Remove Resident Plate from List")
            messageBox.setIconPixmap(
                QPixmap("./icons/icons8-high-risk-80.png").scaled(50, 50, QtCore.Qt.KeepAspectRatio))
            messageBox.setText("Are you sure you want to remove " + selectedCellPlate + "?")

            buttonoptionA = messageBox.addButton("بله حذف شود", QMessageBox.YesRole)
            buttonoptionB = messageBox.addButton("خیر", QMessageBox.NoRole)
            messageBox.setDefaultButton(buttonoptionA)
            messageBox.exec_()

            if messageBox.clickedButton() == buttonoptionA:
                print(selectedCellPlate + ' has been removed.')
                dbRemoveResident(
                    join_elements(convert_persian_to_english(split_string_language_specific(selectedCellPlate))))
=======
            selected_plate = model.data(index, Qt.DisplayRole)
            
            if self.confirm_deletion(selected_plate):
                formatted_plate = join_elements(
                    convert_to_standard_format(
                        split_string_language_specific(selected_plate)
                    )
                )
                dbRemoveResident(formatted_plate)
>>>>>>> e9ef449c1c2c11323532d65843d3a6e2a4b976d6
                self.tableWidget.removeRow(index.row())
        
        self.tableWidget.setRowCount(self.tableWidget.rowCount())

    def confirm_deletion(self, plate_number):
        """Show confirmation dialog for resident deletion."""
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Delete Resident")
        message_box.setIconPixmap(
            QPixmap("./icons/icons8-high-risk-80.png").scaled(50, 50, QtCore.Qt.KeepAspectRatio)
        )
        message_box.setText(f"Are you sure you want to delete {plate_number}?")

        yes_button = message_box.addButton("Yes, Delete", QMessageBox.YesRole)
        no_button = message_box.addButton("No", QMessageBox.NoRole)
        message_box.setDefaultButton(yes_button)
        message_box.exec_()

        return message_box.clickedButton() == yes_button

    def searchLastName(self):
        """Handle last name search functionality."""
        search_text = self.searchTextBox.toPlainText()
        self.refresh_table(search_text)

    def refresh_table(self, last_name=''):
        """Refresh the residents table with current data."""
        residents = dbGetAllResidents(whereLike=f"{last_name}")
        self.tableWidget.setRowCount(len(residents))
        
        for index, resident in enumerate(residents):
            self.populate_table_row(index, resident)

    def populate_table_row(self, row_index, resident):
        """Populate a single table row with resident data."""
        # Set resident information
        self.tableWidget.setItem(row_index, 0, QTableWidgetItem(resident.getFirstName()))
        self.tableWidget.setItem(row_index, 1, QTableWidgetItem(resident.getLastName()))
        self.tableWidget.setItem(row_index, 2, QTableWidgetItem(resident.getBuilding()))
        self.tableWidget.setItem(row_index, 3, QTableWidgetItem(resident.getBlock()))
        self.tableWidget.setItem(row_index, 4, QTableWidgetItem(resident.getNum()))
        self.tableWidget.setItem(row_index, 5, QTableWidgetItem(resident.getCarModel()))
        self.tableWidget.setItem(row_index, 6, QTableWidgetItem(resident.getPlateNumber(display=True)))
        self.tableWidget.setItem(row_index, 7, resident.getStatus())

        # Add action buttons
        self.add_row_buttons(row_index)

    def add_row_buttons(self, row_index):
        """Add action buttons to table row."""
        # Edit button
        edit_button = create_styled_button('edit')
        edit_button.mousePressEvent = functools.partial(self.btnEditClicked, source_object=edit_button)
        self.tableWidget.setCellWidget(row_index, 8, edit_button)

        # Delete button
        delete_button = create_styled_button('delete')
        delete_button.mousePressEvent = functools.partial(self.btnDeleteClicked, source_object=delete_button)
        self.tableWidget.setCellWidget(row_index, 9, delete_button)

        # Search button
        search_button = create_styled_button('search')
        search_button.mousePressEvent = functools.partial(self.btnSearchClicked, source_object=search_button)
        self.tableWidget.setCellWidget(row_index, 10, search_button)

        self.tableWidget.setRowHeight(row_index, 40)

    def btnSearchClicked(self, event, source_object=None):
        """Handle search button click event."""
        row = self.tableWidget.currentRow()
        plate_cell = self.tableWidget.item(row, 6)
        EnteriesWindow(isSearching=True, residnetPlate=plate_cell.text()).exec_()

    def btnEditClicked(self, event, source_object=None):
        """Handle edit button click event."""
        row = self.tableWidget.currentRow()
        plate_cell = self.tableWidget.item(row, 6)
        self.residentAddEditWindow(isEditing=True, residnetPlate=plate_cell.text())

    def residentAddEditWindow(self, isEditing=False, residnetPlate=None):
        """Open window for adding or editing resident information."""
        resident_window = None
        if resident_window is None:
            resident_window = residentsAddNewWindow(
                self,
                isEditing,
                isNew=False,
                isInfo=False,
                residnetPlate=residnetPlate
            )
            resident_window.exec_()
        else:
            resident_window.close()
            resident_window = None
        self.refresh_table()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = residentsWindow()
<<<<<<< HEAD
    window.setWindowTitle('Residents List')
=======
    window.setWindowTitle('Community Residents List')  # Changed from Persian to English
>>>>>>> e9ef449c1c2c11323532d65843d3a6e2a4b976d6
    center_widget(window)
    window.show()
    sys.exit(app.exec_())