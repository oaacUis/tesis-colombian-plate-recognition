# gui_maker.py

import functools

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import QSize
from PySide6.QtGui import QColor, QImage, QPixmap, Qt, QScreen
from PySide6.QtWidgets import (
    QLabel,
    QTableWidgetItem,
    QAbstractItemView,
    QVBoxLayout,
    QDialog,
    QApplication,
    QTableWidget,
)

from configParams import getFieldNames
from helper import jalali
from helper.text_decorators import (
    convert_to_local_format,
    split_string_language_specific,
)  # type: ignore


class CenterAlignDelegate(QtWidgets.QStyledItemDelegate):
    """
    Custom delegate for aligning table items to the center.
    """

    def initStyleOption(self, option, index):
        super(CenterAlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter


class ReadOnlyDelegate(QtWidgets.QStyledItemDelegate):
    """
    Custom delegate to make table cells read-only.
    """

    def createEditor(self, *args, **kwargs):
        return


def create_image_label(image):
    """
    Creates a QLabel with a given image.
    """
    imageLabel = QLabel()
    imageLabel.setText("")
    imageLabel.setScaledContents(True)
    imageLabel.setFixedSize(200, 44)
    imageLabel.setPixmap(image)
    return imageLabel


def create_styled_button(type):
    """
    Generates a styled QPushButton based on the specified type.
    """
    button = QtWidgets.QPushButton()
    button.setFlat(True)
    button.setStyleSheet(
        "QPushButton { background-color: transparent; border: 0px }"
    )
    if type == "edit":
        button.setIcon(QPixmap("./icons/icons8-edit-80.png"))
    elif type == "delete":
        button.setIcon(QPixmap("./icons/icons8-trash-can-80.png"))
    elif type == "info":
        button.setIcon(QPixmap("./icons/icons8-info-80.png"))
    elif type == "add":
        button.setIcon(QPixmap("./icons/icons8-add-80.png"))
    elif type == "search":
        button.setIcon(QPixmap("./icons/icons8-find-user-male-80.png"))
    button.setIconSize(QSize(24, 24))
    return button


def get_status_color(number):
    """
    Returns RGB color based on a status number.
    """
    if number == 0:
        return 224, 27, 36  # Red
    elif number == 1:
        return 51, 209, 122  # Green
    elif number == 2:
        return 246, 211, 45  # Yellow


def get_status_text(number):
    """
    Converts a status number to its corresponding text.
    """
    if int(number) == 0:
        return "Unauthorized"
    elif int(number) == 1:
        return "Authorized"
    elif int(number) == 2:
        return "Unregistered"


def configure_edit_table_widget(self):
    """
    Configures table widget for editing mode.
    """
    fieldsList = [
        "status",
        "plateNum",
        "time",
        "date",
        "platePic",
        "charPercent",
        "platePercent",
        "moreInfo",
        "addNew",
    ]
    fieldsList = getFieldNames(fieldsList)

    self.tableWidget.setColumnCount(len(fieldsList))
    self.tableWidget.setRowCount(20)
    self.tableWidget.setHorizontalHeaderLabels(fieldsList)
    self.tableWidget.horizontalHeader().setSectionResizeMode(
        QtWidgets.QHeaderView.ResizeToContents
    )
    # Changed from RightToLeft
    self.tableWidget.setLayoutDirection(Qt.LeftToRight)
    self.tableWidget.setSortingEnabled(True)

    delegate = CenterAlignDelegate(self.tableWidget)
    self.tableWidget.setItemDelegate(delegate)
    self.tableWidget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
    self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)


def configure_main_table_widget(self):
    """
    Configures the main table widget.
    """
    fieldsList = [
        "status",
        "plateNum",
        "time",
        "date",
        "platePic",
        "moreInfo",
        "addNew",
    ]
    fieldsList = getFieldNames(fieldsList)

    self.tableWidget.setColumnCount(len(fieldsList))
    self.tableWidget.setRowCount(20)
    self.tableWidget.setHorizontalHeaderLabels(fieldsList)
    self.tableWidget.horizontalHeader().setSectionResizeMode(
        QtWidgets.QHeaderView.ResizeToContents
    )
    # Changed from RightToLeft
    self.tableWidget.setLayoutDirection(Qt.LeftToRight)
    self.tableWidget.setSortingEnabled(True)

    delegate = CenterAlignDelegate(self.tableWidget)
    self.tableWidget.setItemDelegate(delegate)
    self.tableWidget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
    self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)


def populate_main_table_with_data(self, dfReadEnteries):
    """
    Populates the main table widget with data.
    """
    delegate = CenterAlignDelegate(self.tableWidget)
    self.tableWidget.setItemDelegate(delegate)
    for each_row in range(len(dfReadEnteries)):
        statusItem = dfReadEnteries.iloc[each_row][0]

        r, g, b = get_status_color(statusItem)
        statusText = get_status_text(statusItem)

        self.tableWidget.setItem(each_row, 0, QTableWidgetItem(statusText))
        self.tableWidget.item(each_row, 0).setBackground(QColor(r, g, b))

        self.tableWidget.setItem(
            each_row,
            1,
            QTableWidgetItem(
                convert_to_local_format(
                    split_string_language_specific(
                        dfReadEnteries.iloc[each_row][1]
                    )
                )
            ),
        )
        self.tableWidget.setItem(
            each_row, 2, QTableWidgetItem((dfReadEnteries.iloc[each_row][2]))
        )
        self.tableWidget.setItem(
            each_row,
            3,
            QTableWidgetItem(
                jalali.Gregorian(dfReadEnteries.iloc[each_row][3])
            ),
        )

        Image = QImage()
        Image.load(dfReadEnteries.iloc[each_row][4])
        QcroppedPlate = QPixmap.fromImage(Image)

        item = create_image_label(QcroppedPlate)
        item.mousePressEvent = functools.partial(
            on_label_double_click, source_object=item
        )

        self.tableWidget.setCellWidget(each_row, 4, item)
        self.tableWidget.setRowHeight(each_row, 44)

        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)


def center_widget(wid):
    """
    Centers a widget on the screen.
    """
    center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
    geo = wid.frameGeometry()
    geo.moveCenter(center)
    wid.move(geo.topLeft())


def on_label_double_click(event, source_object=None):
    """
    Handles double-click event on label to show image in a dialog.
    """
    w = QDialog()
    w.setFixedSize(600, 132)
    w.setWindowTitle("License Plate View")  # Changed from RegValidator

    imageLabel = QLabel(w)
    imageLabel.setText("")
    imageLabel.setScaledContents(True)
    imageLabel.setFixedSize(600, 132)
    imageLabel.setPixmap(source_object.pixmap())

    layout = QVBoxLayout()
    layout.addWidget(imageLabel)
    w.exec()


def on_item_double_click(tableWidget, item):
    """
    Handles item double-click event in the table widget.
    """
    row = item.row()
    column = item.column()
    text = tableWidget.item(row, column).text()  # noqa: F841


class ProxyStyle(QtWidgets.QProxyStyle):
    """
    Custom drawing of control elements, especially buttons with icons.
    """

    def drawControl(self, element, option, painter, widget=None):
        if element == QtWidgets.QStyle.CE_PushButtonLabel:
            icon = QtGui.QIcon(option.icon)
            option.icon = QtGui.QIcon()
        super(ProxyStyle, self).drawControl(element, option, painter, widget)
        if element == QtWidgets.QStyle.CE_PushButtonLabel:
            if not icon.isNull():
                iconSpacing = 4
                mode = (
                    QtGui.QIcon.Normal
                    if option.state & QtWidgets.QStyle.State_Enabled
                    else QtGui.QIcon.Disabled
                )
                if (
                    mode == QtGui.QIcon.Normal
                    and option.state & QtWidgets.QStyle.State_HasFocus
                ):
                    mode = QtGui.QIcon.Active
                state = QtGui.QIcon.Off
                if option.state & QtWidgets.QStyle.State_On:
                    state = QtGui.QIcon.On
                window = (
                    widget.window().windowHandle()
                    if widget is not None else None
                )
                pixmap = icon.pixmap(window, option.iconSize, mode, state)
                pixmapWidth = pixmap.width() / pixmap.devicePixelRatio()
                pixmapHeight = pixmap.height() / pixmap.devicePixelRatio()
                iconRect = QtCore.QRect(
                    QtCore.QPoint(), QtCore.QSize(pixmapWidth, pixmapHeight)
                )
                iconRect.moveCenter(option.rect.center())
                iconRect.moveLeft(option.rect.left() + iconSpacing)
                iconRect = self.visualRect(
                    option.direction, option.rect, iconRect
                    )
                iconRect.translate(
                    self.proxy().pixelMetric(
                        QtWidgets.QStyle.PM_ButtonShiftHorizontal, option, widget  # noqa: E501
                    ),
                    self.proxy().pixelMetric(
                        QtWidgets.QStyle.PM_ButtonShiftVertical, option, widget
                    ),
                )
                painter.drawPixmap(iconRect, pixmap)
