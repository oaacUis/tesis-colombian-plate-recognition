# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edit_enteries.ui'
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QMainWindow, QPushButton,
    QSizePolicy, QTableWidget, QTableWidgetItem, QWidget)

class Ui_EnteriesWindow(object):
    def setupUi(self, EnteriesWindow):
        if not EnteriesWindow.objectName():
            EnteriesWindow.setObjectName(u"EnteriesWindow")
        EnteriesWindow.resize(1068, 427)
        self.centralwidget = QWidget(EnteriesWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tableWidget = QTableWidget(self.centralwidget)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        if (self.tableWidget.rowCount() < 15):
            self.tableWidget.setRowCount(15)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(10, 10, 1051, 411))
        font = QFont()
        font.setFamilies([u"B Yekan"])
        self.tableWidget.setFont(font)
        self.tableWidget.setLayoutDirection(Qt.RightToLeft)
        self.tableWidget.setAlternatingRowColors(False)
        self.tableWidget.setRowCount(15)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(760, 430, 199, 32))
        self.pushButton.setFont(font)
        EnteriesWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(EnteriesWindow)

        QMetaObject.connectSlotsByName(EnteriesWindow)
    # setupUi

    def retranslateUi(self, EnteriesWindow):
        EnteriesWindow.setWindowTitle(QCoreApplication.translate("EnteriesWindow", u"Vehicle Traffic List of the Complex", None))
        self.pushButton.setText(QCoreApplication.translate("EnteriesWindow", u"Register new traffic", None))
    # retranslateUi

