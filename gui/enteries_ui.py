# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'enteries.ui'
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
    QMainWindow, QPushButton, QSizePolicy, QTableWidget,
    QTableWidgetItem, QTextEdit, QWidget)

class Ui_EnteriesWindow(object):
    def setupUi(self, EnteriesWindow):
        if not EnteriesWindow.objectName():
            EnteriesWindow.setObjectName(u"EnteriesWindow")
        EnteriesWindow.resize(629, 480)
        self.centralwidget = QWidget(EnteriesWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tableWidget = QTableWidget(self.centralwidget)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        if (self.tableWidget.rowCount() < 15):
            self.tableWidget.setRowCount(15)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(10, 10, 611, 341))
        font = QFont()
        font.setFamilies([u"B Yekan"])
        self.tableWidget.setFont(font)
        self.tableWidget.setLayoutDirection(Qt.RightToLeft)
        self.tableWidget.setAlternatingRowColors(False)
        self.tableWidget.setRowCount(15)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(420, 440, 201, 34))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_2 = QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setFont(font)

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(self.layoutWidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setFont(font)

        self.horizontalLayout.addWidget(self.pushButton)

        self.layoutWidget1 = QWidget(self.centralwidget)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(10, 391, 611, 72))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.textEdit_3 = QTextEdit(self.layoutWidget1)
        self.textEdit_3.setObjectName(u"textEdit_3")
        self.textEdit_3.setFont(font)

        self.horizontalLayout_2.addWidget(self.textEdit_3)

        self.textEdit_2 = QTextEdit(self.layoutWidget1)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.textEdit_2.setFont(font)

        self.horizontalLayout_2.addWidget(self.textEdit_2)

        self.textEdit = QTextEdit(self.layoutWidget1)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setFont(font)

        self.horizontalLayout_2.addWidget(self.textEdit)

        self.layoutWidget2 = QWidget(self.centralwidget)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(10, 360, 611, 26))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.layoutWidget2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_3)

        self.label = QLabel(self.layoutWidget2)
        self.label.setObjectName(u"label")
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label)

        self.label_2 = QLabel(self.layoutWidget2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_2)

        EnteriesWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(EnteriesWindow)

        QMetaObject.connectSlotsByName(EnteriesWindow)
    # setupUi

    def retranslateUi(self, EnteriesWindow):
        EnteriesWindow.setWindowTitle(QCoreApplication.translate("EnteriesWindow", u"\u0644\u06cc\u0633\u062a \u062a\u0631\u062f\u062f \u062e\u0648\u062f\u0631\u0648\u0647\u0627\u06cc \u0634\u0647\u0631\u06a9", None))
        self.pushButton_2.setText(QCoreApplication.translate("EnteriesWindow", u"\u062d\u0630\u0641 \u062a\u0631\u062f\u062f", None))
        self.pushButton.setText(QCoreApplication.translate("EnteriesWindow", u"New traffic registration", None))
        self.label_3.setText(QCoreApplication.translate("EnteriesWindow", u"\u062a\u0627\u0631\u06cc\u062e", None))
        self.label.setText(QCoreApplication.translate("EnteriesWindow", u"\u0633\u0627\u0639\u062a", None))
        self.label_2.setText(QCoreApplication.translate("EnteriesWindow", u"License plate", None))
    # retranslateUi

