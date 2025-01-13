# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'residentNew.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QWidget)

from gui.plateQLineEdit import plateQLineEdit

class Ui_UsersWindow(object):
    def setupUi(self, UsersWindow):
        if not UsersWindow.objectName():
            UsersWindow.setObjectName(u"UsersWindow")
        UsersWindow.resize(1064, 235)
        UsersWindow.setLayoutDirection(Qt.RightToLeft)
        self.centralwidget = QWidget(UsersWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(440, 130, 91, 29))
        font = QFont()
        font.setFamilies([u"B Yekan"])
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignCenter)
        self.plateTextView = QLabel(self.centralwidget)
        self.plateTextView.setObjectName(u"plateTextView")
        self.plateTextView.setEnabled(True)
        self.plateTextView.setGeometry(QRect(540, 160, 300, 62))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plateTextView.sizePolicy().hasHeightForWidth())
        self.plateTextView.setSizePolicy(sizePolicy)
        self.plateTextView.setMaximumSize(QSize(300, 62))
        font1 = QFont()
        font1.setFamilies([u"B Yekan"])
        font1.setPointSize(29)
        font1.setKerning(True)
        self.plateTextView.setFont(font1)
        self.plateTextView.setLayoutDirection(Qt.LeftToRight)
        self.plateTextView.setAutoFillBackground(False)
        self.plateTextView.setStyleSheet(u"")
        self.plateTextView.setFrameShape(QFrame.Box)
        self.plateTextView.setTextFormat(Qt.PlainText)
        self.plateTextView.setScaledContents(False)
        self.plateTextView.setAlignment(Qt.AlignCenter)
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(890, 130, 141, 29))
        self.label_6.setFont(font)
        self.label_6.setAlignment(Qt.AlignCenter)
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(610, 130, 181, 21))
        self.label_5.setFont(font)
        self.label_5.setAlignment(Qt.AlignCenter)
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 1041, 31))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)

        self.label_10 = QLabel(self.layoutWidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)
        self.label_10.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_10, 0, 1, 1, 1)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)

        self.label_7 = QLabel(self.layoutWidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)
        self.label_7.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_7, 0, 4, 1, 1)

        self.label_8 = QLabel(self.layoutWidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)
        self.label_8.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_8, 0, 3, 1, 1)

        self.addResidentButton = QPushButton(self.centralwidget)
        self.addResidentButton.setObjectName(u"addResidentButton")
        self.addResidentButton.setGeometry(QRect(10, 170, 131, 41))
        self.addResidentButton.setFont(font)
        self.fNameTextBox = plateQLineEdit(self.centralwidget)
        self.fNameTextBox.setObjectName(u"fNameTextBox")
        self.fNameTextBox.setGeometry(QRect(850, 50, 200, 50))
        self.fNameTextBox.setBaseSize(QSize(200, 50))
        self.fNameTextBox.setFont(font)
        self.fNameTextBox.setCursor(QCursor(Qt.ArrowCursor))
        self.fNameTextBox.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"                        border-color: rgb(0, 0, 0);\n"
"                        border-width: 1px;\n"
"                        border-style: solid;\n"
"                    ")
        self.fNameTextBox.setMaxLength(50)
        self.fNameTextBox.setFrame(False)
        self.lNameTextBox = plateQLineEdit(self.centralwidget)
        self.lNameTextBox.setObjectName(u"lNameTextBox")
        self.lNameTextBox.setGeometry(QRect(640, 50, 200, 50))
        self.lNameTextBox.setBaseSize(QSize(200, 50))
        self.lNameTextBox.setFont(font)
        self.lNameTextBox.setCursor(QCursor(Qt.ArrowCursor))
        self.lNameTextBox.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"                        border-color: rgb(0, 0, 0);\n"
"                        border-width: 1px;\n"
"                        border-style: solid;\n"
"                    ")
        self.lNameTextBox.setMaxLength(50)
        self.lNameTextBox.setFrame(False)
        self.buildingTextBox = plateQLineEdit(self.centralwidget)
        self.buildingTextBox.setObjectName(u"buildingTextBox")
        self.buildingTextBox.setGeometry(QRect(430, 50, 200, 50))
        self.buildingTextBox.setBaseSize(QSize(200, 50))
        self.buildingTextBox.setFont(font)
        self.buildingTextBox.setCursor(QCursor(Qt.ArrowCursor))
        self.buildingTextBox.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"                        border-color: rgb(0, 0, 0);\n"
"                        border-width: 1px;\n"
"                        border-style: solid;\n"
"                    ")
        self.buildingTextBox.setMaxLength(3)
        self.buildingTextBox.setFrame(False)
        self.blockTextBox = plateQLineEdit(self.centralwidget)
        self.blockTextBox.setObjectName(u"blockTextBox")
        self.blockTextBox.setGeometry(QRect(220, 50, 200, 50))
        self.blockTextBox.setBaseSize(QSize(200, 50))
        self.blockTextBox.setFont(font)
        self.blockTextBox.setCursor(QCursor(Qt.ArrowCursor))
        self.blockTextBox.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"                        border-color: rgb(0, 0, 0);\n"
"                        border-width: 1px;\n"
"                        border-style: solid;\n"
"                    ")
        self.blockTextBox.setMaxLength(3)
        self.blockTextBox.setFrame(False)
        self.numTextBox = plateQLineEdit(self.centralwidget)
        self.numTextBox.setObjectName(u"numTextBox")
        self.numTextBox.setGeometry(QRect(10, 50, 200, 50))
        self.numTextBox.setBaseSize(QSize(200, 50))
        self.numTextBox.setFont(font)
        self.numTextBox.setCursor(QCursor(Qt.ArrowCursor))
        self.numTextBox.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"                        border-color: rgb(0, 0, 0);\n"
"                        border-width: 1px;\n"
"                        border-style: solid;\n"
"                    ")
        self.numTextBox.setMaxLength(7)
        self.numTextBox.setFrame(False)
        self.carModelTextBox = plateQLineEdit(self.centralwidget)
        self.carModelTextBox.setObjectName(u"carModelTextBox")
        self.carModelTextBox.setGeometry(QRect(850, 170, 200, 50))
        self.carModelTextBox.setBaseSize(QSize(200, 50))
        self.carModelTextBox.setFont(font)
        self.carModelTextBox.setCursor(QCursor(Qt.ArrowCursor))
        self.carModelTextBox.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"                        border-color: rgb(0, 0, 0);\n"
"                        border-width: 1px;\n"
"                        border-style: solid;\n"
"                    ")
        self.carModelTextBox.setMaxLength(50)
        self.carModelTextBox.setFrame(False)
        self.plateTextNum_4 = plateQLineEdit(self.centralwidget)
        self.plateTextNum_4.setObjectName(u"plateTextNum_4")
        self.plateTextNum_4.setGeometry(QRect(700, 170, 51, 41))
        self.plateTextNum_4.setBaseSize(QSize(400, 50))
        font2 = QFont()
        font2.setFamilies([u"B Yekan"])
        font2.setPointSize(14)
        self.plateTextNum_4.setFont(font2)
        self.plateTextNum_4.setCursor(QCursor(Qt.ArrowCursor))
        self.plateTextNum_4.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"                        border-color: rgb(0, 0, 0);\n"
"                        border-width: 1px;\n"
"                        border-style: solid;\n"
"\n"
"                        letter-spacing: 3px;\n"
"                        text-align: center;\n"
"                    ")
        self.plateTextNum_4.setMaxLength(3)
        self.plateTextNum_4.setFrame(False)
        self.plateTextNum_1 = plateQLineEdit(self.centralwidget)
        self.plateTextNum_1.setObjectName(u"plateTextNum_1")
        self.plateTextNum_1.setGeometry(QRect(600, 170, 51, 41))
        self.plateTextNum_1.setBaseSize(QSize(400, 50))
        self.plateTextNum_1.setFont(font2)
        self.plateTextNum_1.setCursor(QCursor(Qt.ArrowCursor))
        self.plateTextNum_1.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"                        border-color: rgb(0, 0, 0);\n"
"                        border-width: 1px;\n"
"                        border-style: solid;\n"
"\n"
"                        letter-spacing: 3px;\n"
"                        text-align: center;\n"
"                    ")
        self.plateTextNum_1.setMaxLength(3)
        self.plateTextNum_1.setFrame(False)
        self.statusComboBox = QComboBox(self.centralwidget)
        self.statusComboBox.setObjectName(u"statusComboBox")
        self.statusComboBox.setGeometry(QRect(400, 170, 120, 41))
        sizePolicy.setHeightForWidth(self.statusComboBox.sizePolicy().hasHeightForWidth())
        self.statusComboBox.setSizePolicy(sizePolicy)
        self.statusComboBox.setMinimumSize(QSize(120, 41))
        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")
        self.statusLabel.setGeometry(QRect(150, 180, 281, 29))
        self.statusLabel.setFont(font)
        self.statusLabel.setStyleSheet(u"")
        self.statusLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        UsersWindow.setCentralWidget(self.centralwidget)
        self.layoutWidget.raise_()
        self.label_3.raise_()
        self.plateTextView.raise_()
        self.label_6.raise_()
        self.label_5.raise_()
        self.addResidentButton.raise_()
        self.fNameTextBox.raise_()
        self.lNameTextBox.raise_()
        self.buildingTextBox.raise_()
        self.blockTextBox.raise_()
        self.numTextBox.raise_()
        self.carModelTextBox.raise_()
        self.plateTextNum_4.raise_()
        self.plateTextNum_1.raise_()
        self.statusComboBox.raise_()
        self.statusLabel.raise_()

        self.retranslateUi(UsersWindow)

        QMetaObject.connectSlotsByName(UsersWindow)
    # setupUi

    def retranslateUi(self, UsersWindow):
        UsersWindow.setWindowTitle(QCoreApplication.translate("UsersWindow", u"List of residents of the town", None))
        self.label_3.setText(QCoreApplication.translate("UsersWindow", u"Traffic status", None))
        self.plateTextView.setText("")
        self.label_6.setText(QCoreApplication.translate("UsersWindow", u"Vehicle type", None))
        self.label_5.setText(QCoreApplication.translate("UsersWindow", u"License plate", None))
        self.label_4.setText(QCoreApplication.translate("UsersWindow", u"Name", None))
        self.label_10.setText(QCoreApplication.translate("UsersWindow", u"Last name", None))
        self.label_2.setText(QCoreApplication.translate("UsersWindow", u"Building", None))
        self.label_7.setText(QCoreApplication.translate("UsersWindow", u"License plate", None))
        self.label_8.setText(QCoreApplication.translate("UsersWindow", u"Block", None))
        self.addResidentButton.setText(QCoreApplication.translate("UsersWindow", u" \u00ad Resident registration", None))
        self.fNameTextBox.setText("")
        self.lNameTextBox.setText("")
        self.buildingTextBox.setText("")
        self.blockTextBox.setText("")
        self.numTextBox.setText("")
        self.carModelTextBox.setText("")
        self.plateTextNum_4.setText("")
        self.plateTextNum_1.setText("")
        self.statusLabel.setText("")
    # retranslateUi

