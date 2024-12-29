# enteries_window.py
"""
Module for managing and displaying entry records in a community system.
"""

import functools
import sys

from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QTableWidgetItem, QApplication, QDialog
from qtpy.uic import loadUi

from configParams import Parameters
from database.db_entries_utils import dbGetAllEntries
from database.db_resident_utils import db_get_plate_status
from helper.gui_maker import (
    create_image_label, 
    on_label_double_click, 
    create_styled_button, 
    center_widget,
    configure_edit_table_widget
)
from helper.text_decorators import (
    convert_to_standard_format, 
    split_string_language_specific, 
    join_elements
)
from resident_view import residentView
from residents_edit import residentsAddNewWindow

params = Parameters()


class EnteriesWindow(QDialog):
    """
    Dialog window for managing and displaying community entry records.
    """

    def __init__(self, isSearching=False, residnetPlate=''):
        """
        Initialize the entries window.

        Args:
            isSearching (bool): Whether in search mode
            residnetPlate (str): License plate number to search for
        """
        super(EnteriesWindow, self).__init__()

        loadUi('./gui/edit_enteries.ui', self)
        self.setFixedSize(self.size())
        configure_edit_table_widget(self)

        if isSearching:
            self.residnetPlateEng = join_elements(
                convert_to_standard_format(split_string_language_specific(residnetPlate))
            )
            self.refresh_table(self.residnetPlateEng)
        else:
            self.refresh_table()

    def refresh_table(self, plateNum=''):
        """
        Refresh the entries table with updated data.

        Args:
            plateNum (str): Optional plate number for filtering
        """
        entries = dbGetAllEntries(limit=100, whereLike=plateNum)
        self.tableWidget.setRowCount(len(entries))

        for index, entry in enumerate(entries):
            # Process plate number
            formatted_plate = join_elements(
                convert_to_standard_format(split_string_language_specific(entry.getPlateNumber(display=True)))
            )
            status_num = db_get_plate_status(formatted_plate)

            # Populate table row
            self.tableWidget.setItem(index, 0, QTableWidgetItem(entry.getStatus(statusNum=status_num)))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(entry.getPlateNumber(display=True)))
            self.tableWidget.setItem(index, 2, QTableWidgetItem(entry.getTime()))
            self.tableWidget.setItem(index, 3, QTableWidgetItem(entry.getDate()))

            # Handle plate image
            plate_image = QImage()
            plate_image.load(entry.getPlatePic())
            plate_pixmap = QPixmap.fromImage(plate_image)

            image_label = create_image_label(plate_pixmap)
            image_label.mousePressEvent = functools.partial(on_label_double_click, source_object=image_label)
            self.tableWidget.setCellWidget(index, 4, image_label)
            self.tableWidget.setRowHeight(index, 44)

            # Set confidence values
            self.tableWidget.setItem(index, 5, QTableWidgetItem(entry.getCharPercent()))
            self.tableWidget.setItem(index, 6, QTableWidgetItem(entry.getPlatePercent()))

            # Create and configure info button
            info_button = create_styled_button('info')
            info_button.mousePressEvent = functools.partial(self.btnInfoClicked, source_object=info_button)
            self.tableWidget.setCellWidget(index, 7, info_button)

            # Handle unregistered entries (status 2)
            if status_num == 2:
                add_button = create_styled_button('add')
                add_button.mousePressEvent = functools.partial(self.btnAddClicked, source_object=add_button)
                self.tableWidget.setCellWidget(index, 8, add_button)
                info_button.setEnabled(False)

    def btnInfoClicked(self, event, source_object=None):
        """
        Handle info button click event.
        
        Args:
            event: Click event
            source_object: Button that triggered the event
        """
        row = self.tableWidget.currentRow()
        plate_field = self.tableWidget.item(row, 1)
        residentView(residnetPlate=plate_field.text()).exec_()

    def btnAddClicked(self, event, source_object=None):
        """
        Handle add button click event.
        
        Args:
            event: Click event
            source_object: Button that triggered the event
        """
        row = self.tableWidget.currentRow()
        plate_field = self.tableWidget.item(row, 1)
        self.residentAddEditWindow(isNew=True, residnetPlate=plate_field.text())

    def residentAddEditWindow(self, isEditing=False, isNew=False, isInfo=False, residnetPlate=None):
        """
        Open window for adding/editing resident information.

        Args:
            isEditing (bool): Whether in edit mode
            isNew (bool): Whether adding new resident
            isInfo (bool): Whether in info view mode
            residnetPlate (str): License plate number
        """
        resident_window = None
        if resident_window is None:
            resident_window = residentsAddNewWindow(self, isEditing, isNew, isInfo, residnetPlate)
            resident_window.exec_()
        else:
            resident_window.close()
            resident_window = None
        self.refresh_table()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EnteriesWindow()
<<<<<<< HEAD
    window.setWindowTitle('Entry List of the Complex')
=======
    window.setWindowTitle('Community Entry Records')  # Changed from Persian to English
>>>>>>> e9ef449c1c2c11323532d65843d3a6e2a4b976d6
    center_widget(window)
    window.show()
    sys.exit(app.exec_())