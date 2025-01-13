# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'residentView.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_UsersWindow(object):
    def setupUi(self, UsersWindow):
        if not UsersWindow.objectName():
            UsersWindow.setObjectName(u"UsersWindow")
        UsersWindow.resize(409, 389)
        UsersWindow.setLayoutDirection(Qt.LeftToRight)
        self.centralwidget = QWidget(UsersWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 261, 371))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.labelFname = QLabel(self.layoutWidget)
        self.labelFname.setObjectName(u"labelFname")
        font = QFont()
        font.setFamilies([u"Arial"])
        self.labelFname.setFont(font)
        self.labelFname.setLayoutDirection(Qt.RightToLeft)
        self.labelFname.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_2.addWidget(self.labelFname)

        self.labelLname = QLabel(self.layoutWidget)
        self.labelLname.setObjectName(u"labelLname")
        self.labelLname.setFont(font)
        self.labelLname.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_2.addWidget(self.labelLname)

        self.labelBuilding = QLabel(self.layoutWidget)
        self.labelBuilding.setObjectName(u"labelBuilding")
        self.labelBuilding.setFont(font)
        self.labelBuilding.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_2.addWidget(self.labelBuilding)

        self.labelBlock = QLabel(self.layoutWidget)
        self.labelBlock.setObjectName(u"labelBlock")
        self.labelBlock.setFont(font)
        self.labelBlock.setLayoutDirection(Qt.LeftToRight)
        self.labelBlock.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_2.addWidget(self.labelBlock)

        self.labelNum = QLabel(self.layoutWidget)
        self.labelNum.setObjectName(u"labelNum")
        self.labelNum.setFont(font)
        self.labelNum.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_2.addWidget(self.labelNum)

        self.labelCarModel = QLabel(self.layoutWidget)
        self.labelCarModel.setObjectName(u"labelCarModel")
        self.labelCarModel.setFont(font)
        self.labelCarModel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_2.addWidget(self.labelCarModel)

        self.labelPlateNum = QLabel(self.layoutWidget)
        self.labelPlateNum.setObjectName(u"labelPlateNum")
        self.labelPlateNum.setFont(font)
        self.labelPlateNum.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_2.addWidget(self.labelPlateNum)

        self.labelStatus = QLabel(self.layoutWidget)
        self.labelStatus.setObjectName(u"labelStatus")
        self.labelStatus.setFont(font)
        self.labelStatus.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_2.addWidget(self.labelStatus)

        self.layoutWidget1 = QWidget(self.centralwidget)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(310, 10, 91, 371))
        self.verticalLayout = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.layoutWidget1)
        self.label_4.setObjectName(u"label_4")
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(12)
        font1.setBold(True)
        self.label_4.setFont(font1)
        self.label_4.setLayoutDirection(Qt.LeftToRight)
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.label_4)

        self.line_2 = QFrame(self.layoutWidget1)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.label_10 = QLabel(self.layoutWidget1)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font1)
        self.label_10.setLayoutDirection(Qt.LeftToRight)
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.label_10)

        self.line_3 = QFrame(self.layoutWidget1)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.label_2 = QLabel(self.layoutWidget1)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)
        self.label_2.setLayoutDirection(Qt.LeftToRight)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.label_2)

        self.line_4 = QFrame(self.layoutWidget1)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_4)

        self.label_8 = QLabel(self.layoutWidget1)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font1)
        self.label_8.setLayoutDirection(Qt.LeftToRight)
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.label_8)

        self.line_5 = QFrame(self.layoutWidget1)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_5)

        self.label_7 = QLabel(self.layoutWidget1)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font1)
        self.label_7.setLayoutDirection(Qt.LeftToRight)
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.label_7)

        self.line_6 = QFrame(self.layoutWidget1)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.Shape.HLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_6)

        self.label_6 = QLabel(self.layoutWidget1)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)
        self.label_6.setLayoutDirection(Qt.LeftToRight)
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.label_6)

        self.line_7 = QFrame(self.layoutWidget1)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.Shape.HLine)
        self.line_7.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_7)

        self.label_5 = QLabel(self.layoutWidget1)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)
        self.label_5.setLayoutDirection(Qt.LeftToRight)
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.label_5)

        self.line_8 = QFrame(self.layoutWidget1)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.Shape.HLine)
        self.line_8.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_8)

        self.label_3 = QLabel(self.layoutWidget1)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)
        self.label_3.setLayoutDirection(Qt.LeftToRight)
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.label_3)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(280, 10, 20, 371))
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        UsersWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(UsersWindow)

        QMetaObject.connectSlotsByName(UsersWindow)
    # setupUi

    def retranslateUi(self, UsersWindow):
        UsersWindow.setWindowTitle(QCoreApplication.translate("UsersWindow", u"Resident Information Display", None))
        self.labelFname.setText(QCoreApplication.translate("UsersWindow", u"First Name", None))
        self.labelLname.setText(QCoreApplication.translate("UsersWindow", u"Last Name", None))
        self.labelBuilding.setText(QCoreApplication.translate("UsersWindow", u"Building", None))
        self.labelBlock.setText(QCoreApplication.translate("UsersWindow", u"Block", None))
        self.labelNum.setText(QCoreApplication.translate("UsersWindow", u"Plate Number", None))
        self.labelCarModel.setText(QCoreApplication.translate("UsersWindow", u"Car Model", None))
        self.labelPlateNum.setText(QCoreApplication.translate("UsersWindow", u"Car Plate", None))
        self.labelStatus.setText(QCoreApplication.translate("UsersWindow", u"Traffic Status", None))
        self.label_4.setText(QCoreApplication.translate("UsersWindow", u"First Name", None))
        self.label_10.setText(QCoreApplication.translate("UsersWindow", u"Last Name", None))
        self.label_2.setText(QCoreApplication.translate("UsersWindow", u"Building", None))
        self.label_8.setText(QCoreApplication.translate("UsersWindow", u"Block", None))
        self.label_7.setText(QCoreApplication.translate("UsersWindow", u"Plate", None))
        self.label_6.setText(QCoreApplication.translate("UsersWindow", u"Car Type", None))
        self.label_5.setText(QCoreApplication.translate("UsersWindow", u"Car Plate", None))
        self.label_3.setText(QCoreApplication.translate("UsersWindow", u"Traffic Status", None))
    # retranslateUi

