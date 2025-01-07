# refres_table.py 

#Librerias necesarias para la creación de la tabla
from PySide6.QtWidgets import QTableWidgetItem # Para elementos de la tabla
from PySide6.QtGui import QImage, QPixmap # Para manejo de imágenes
import functools # Para funciones parciales

#Librerias necesarias del proyecto (se comentan para pruebas)

from database.db_entries_utils import dbGetAllEntries # Para obtener entradas de la BD

from database.db_resident_utils import db_get_plate_status # Para obtener estado de placas

from helper.gui_maker import create_image_label, create_styled_button, on_label_double_click # Utilidades de GUI

from helper.text_decorators import join_elements, split_string_language_specific # Procesamiento de texto


def refresh_table(self, plateNum= ""):
    
    # Get all entries from the database with a limit of 10 and where the plate number is like the given plate number
    plateNum = dbGetAllEntries(limit=10, whereLike=plateNum)
    # Set the number of rows in the table widget to the length of the plate number list
    self.tableWidget.setRowCount(len(plateNum))
    # Iterate through the plate number list
    for index, entry in enumerate(plateNum):
        # Get the plate number in English
        plateNum2 = join_elements(
            (split_string_language_specific(entry.getPlateNumber(display=True))))
        # Get the plate status from the database
        statusNum = db_get_plate_status(plateNum2)
        # Set the status of the entry in the table widget
        self.tableWidget.setItem(index, 0, QTableWidgetItem(entry.getStatus(statusNum=statusNum)))
        # Set the plate number of the entry in the table widget
        self.tableWidget.setItem(index, 1, QTableWidgetItem(entry.getPlateNumber(display=True)))
        # Set the time of the entry in the table widget
        self.tableWidget.setItem(index, 2, QTableWidgetItem(entry.getTime()))
        # Set the date of the entry in the table widget
        self.tableWidget.setItem(index, 3, QTableWidgetItem(entry.getDate()))

        # Load the plate picture
        Image = QImage()
        Image.load(entry.getPlatePic())
        # Create a QcroppedPlate from the Image
        QcroppedPlate = QPixmap.fromImage(Image)

        # Create an image label from the QcroppedPlate
        item = create_image_label(QcroppedPlate)
        # Set a mouse press event to on_label_double_click
        item.mousePressEvent = functools.partial(on_label_double_click, source_object=item)
        # Set the cell widget of the table widget to the image label
        self.tableWidget.setCellWidget(index, 4, item)
        # Set the row height of the table widget to 44
        self.tableWidget.setRowHeight(index, 44)

        # Create an info button
        infoBtnItem = create_styled_button('info')
        # Set a mouse press event to on_info_button_clicked
        infoBtnItem.mousePressEvent = functools.partial(self.on_info_button_clicked, source_object=infoBtnItem)
        # Set the cell widget of the table widget to the info button
        self.tableWidget.setCellWidget(index, 5, infoBtnItem)

        # Create an add button
        addBtnItem = create_styled_button('add')
        # Set a mouse press event to on_add_button_clicked
        addBtnItem.mousePressEvent = functools.partial(self.on_add_button_clicked, source_object=addBtnItem)
        # Set the cell widget of the table widget to the add button
        self.tableWidget.setCellWidget(index, 6, addBtnItem)
        # Disable the add button
        addBtnItem.setEnabled(False)

        # If the status is 2, enable the add button and disable the info button
        if statusNum == 2:
            addBtnItem.setEnabled(True)
            infoBtnItem.setEnabled(False)

