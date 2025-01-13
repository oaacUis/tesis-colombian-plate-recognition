# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'residents.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QMainWindow, QPushButton, QRadioButton, QSizePolicy,
    QTableWidget, QTableWidgetItem, QTextEdit, QWidget)

class Ui_UsersWindow(object):
    def setupUi(self, UsersWindow):
        if not UsersWindow.objectName():
            UsersWindow.setObjectName(u"UsersWindow")
        UsersWindow.resize(1041, 533)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(UsersWindow.sizePolicy().hasHeightForWidth())
        UsersWindow.setSizePolicy(sizePolicy)
        UsersWindow.setLayoutDirection(Qt.RightToLeft)
        self.centralwidget = QWidget(UsersWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.searchTextBox = QTextEdit(self.centralwidget)
        self.searchTextBox.setObjectName(u"searchTextBox")
        self.searchTextBox.setGeometry(QRect(580, 480, 381, 41))
        font = QFont()
        font.setFamilies([u"B Yekan"])
        self.searchTextBox.setFont(font)
        self.searchTextBox.setLayoutDirection(Qt.RightToLeft)
        self.searchTextBox.setInputMethodHints(Qt.ImhNone)
        self.addResidentButton = QPushButton(self.centralwidget)
        self.addResidentButton.setObjectName(u"addResidentButton")
        self.addResidentButton.setGeometry(QRect(10, 480, 171, 41))
        self.addResidentButton.setFont(font)
        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(960, 480, 71, 41))
        self.label_9.setFont(font)
        self.label_9.setAlignment(Qt.AlignCenter)
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(310, 550, 251, 26))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.radioLName = QRadioButton(self.layoutWidget)
        self.radioLName.setObjectName(u"radioLName")

        self.horizontalLayout.addWidget(self.radioLName)

        self.radioPlateNum = QRadioButton(self.layoutWidget)
        self.radioPlateNum.setObjectName(u"radioPlateNum")

        self.horizontalLayout.addWidget(self.radioPlateNum)

        self.tableWidget = QTableWidget(self.centralwidget)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        if (self.tableWidget.rowCount() < 15):
            self.tableWidget.setRowCount(15)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(10, 10, 1011, 461))
        self.tableWidget.setFont(font)
        self.tableWidget.setLayoutDirection(Qt.RightToLeft)
        self.tableWidget.setAlternatingRowColors(False)
        self.tableWidget.setRowCount(15)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        UsersWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(UsersWindow)

        QMetaObject.connectSlotsByName(UsersWindow)
    # setupUi

    def retranslateUi(self, UsersWindow):
        UsersWindow.setWindowTitle(QCoreApplication.translate("UsersWindow", u"List of residents of the town", None))
        self.searchTextBox.setPlaceholderText("")
        self.addResidentButton.setText(QCoreApplication.translate("UsersWindow", u"New resident registration", None))
        self.label_9.setText(QCoreApplication.translate("UsersWindow", u"Search", None))
        self.radioLName.setText(QCoreApplication.translate("UsersWindow", u"Last name", None))
        self.radioPlateNum.setText(QCoreApplication.translate("UsersWindow", u"License plate", None))
    # retranslateUi

