# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settingsMain.ui'
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
from PySide6.QtWidgets import (QApplication, QCalendarWidget, QComboBox, QDateEdit,
    QFrame, QGraphicsView, QLCDNumber, QLabel,
    QMainWindow, QProgressBar, QPushButton, QSizePolicy,
    QSlider, QTextEdit, QTimeEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(874, 566)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.plateTextIR = QLabel(self.centralwidget)
        self.plateTextIR.setObjectName(u"plateTextIR")
        self.plateTextIR.setEnabled(True)
        self.plateTextIR.setGeometry(QRect(830, 140, 71, 62))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.plateTextIR.sizePolicy().hasHeightForWidth())
        self.plateTextIR.setSizePolicy(sizePolicy1)
        self.plateTextIR.setMaximumSize(QSize(300, 62))
        font = QFont()
        font.setFamilies([u"B Yekan"])
        font.setPointSize(23)
        font.setKerning(True)
        self.plateTextIR.setFont(font)
        self.plateTextIR.setLayoutDirection(Qt.LeftToRight)
        self.plateTextIR.setAutoFillBackground(False)
        self.plateTextIR.setStyleSheet(u"letter-spacing: 3px;\n"
"                        padding-bottom: 3%;\n"
"                    ")
        self.plateTextIR.setFrameShape(QFrame.NoFrame)
        self.plateTextIR.setTextFormat(Qt.PlainText)
        self.plateTextIR.setScaledContents(False)
        self.plateTextIR.setAlignment(Qt.AlignCenter)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(560, 100, 89, 25))
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(250, 90, 251, 41))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(610, 160, 89, 25))
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(400, 160, 101, 31))
        self.textEdit_2 = QTextEdit(self.centralwidget)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.textEdit_2.setGeometry(QRect(140, 140, 151, 41))
        self.textEdit_3 = QTextEdit(self.centralwidget)
        self.textEdit_3.setObjectName(u"textEdit_3")
        self.textEdit_3.setGeometry(QRect(150, 200, 171, 41))
        self.timeEdit = QTimeEdit(self.centralwidget)
        self.timeEdit.setObjectName(u"timeEdit")
        self.timeEdit.setGeometry(QRect(60, 40, 118, 26))
        self.dateEdit = QDateEdit(self.centralwidget)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setGeometry(QRect(60, 80, 110, 26))
        self.horizontalSlider = QSlider(self.centralwidget)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setGeometry(QRect(40, 280, 231, 31))
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.lcdNumber = QLCDNumber(self.centralwidget)
        self.lcdNumber.setObjectName(u"lcdNumber")
        self.lcdNumber.setGeometry(QRect(360, 230, 181, 61))
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(180, 330, 118, 23))
        self.progressBar.setValue(24)
        self.calendarWidget = QCalendarWidget(self.centralwidget)
        self.calendarWidget.setObjectName(u"calendarWidget")
        self.calendarWidget.setGeometry(QRect(330, 320, 401, 231))
        self.gv = QGraphicsView(self.centralwidget)
        self.gv.setObjectName(u"gv")
        self.gv.setGeometry(QRect(50, 391, 221, 151))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.plateTextIR.setText("")
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
    # retranslateUi

