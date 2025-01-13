# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plateView.ui'
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
    QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(704, 262)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.plateView = QLabel(self.centralwidget)
        self.plateView.setObjectName(u"plateView")
        self.plateView.setGeometry(QRect(50, 30, 600, 132))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.plateView.sizePolicy().hasHeightForWidth())
        self.plateView.setSizePolicy(sizePolicy1)
        self.plateView.setMaximumSize(QSize(600, 132))
        self.plateView.setFrameShape(QFrame.Box)
        self.plateView.setAlignment(Qt.AlignCenter)
        self.plateTextView = QLabel(self.centralwidget)
        self.plateTextView.setObjectName(u"plateTextView")
        self.plateTextView.setEnabled(True)
        self.plateTextView.setGeometry(QRect(210, 180, 300, 62))
        sizePolicy1.setHeightForWidth(self.plateTextView.sizePolicy().hasHeightForWidth())
        self.plateTextView.setSizePolicy(sizePolicy1)
        self.plateTextView.setMaximumSize(QSize(300, 62))
        font = QFont()
        font.setFamilies([u"B Yekan"])
        font.setPointSize(29)
        font.setKerning(True)
        self.plateTextView.setFont(font)
        self.plateTextView.setLayoutDirection(Qt.LeftToRight)
        self.plateTextView.setAutoFillBackground(False)
        self.plateTextView.setStyleSheet(u"border-image:\n"
"                        url(/media/mt/Files/vs-code/Final/ShahrakAmir/resource/img/template-base.png) 0 0 0 0 stretch\n"
"                        stretch;\n"
"                        letter-spacing: 3px;\n"
"\n"
"                        padding-right: 5%;\n"
"                        padding-left: 5%;\n"
"\n"
"                        padding-bottom: 5%;\n"
"                        clear: both;\n"
"                    ")
        self.plateTextView.setFrameShape(QFrame.Box)
        self.plateTextView.setTextFormat(Qt.PlainText)
        self.plateTextView.setScaledContents(False)
        self.plateTextView.setAlignment(Qt.AlignCenter)
        self.plateTextIR = QLabel(self.centralwidget)
        self.plateTextIR.setObjectName(u"plateTextIR")
        self.plateTextIR.setEnabled(True)
        self.plateTextIR.setGeometry(QRect(730, 190, 71, 62))
        sizePolicy1.setHeightForWidth(self.plateTextIR.sizePolicy().hasHeightForWidth())
        self.plateTextIR.setSizePolicy(sizePolicy1)
        self.plateTextIR.setMaximumSize(QSize(300, 62))
        font1 = QFont()
        font1.setFamilies([u"B Yekan"])
        font1.setPointSize(23)
        font1.setKerning(True)
        self.plateTextIR.setFont(font1)
        self.plateTextIR.setLayoutDirection(Qt.LeftToRight)
        self.plateTextIR.setAutoFillBackground(False)
        self.plateTextIR.setStyleSheet(u"letter-spacing: 3px;\n"
"                        padding-bottom: 3%;\n"
"                    ")
        self.plateTextIR.setFrameShape(QFrame.NoFrame)
        self.plateTextIR.setTextFormat(Qt.PlainText)
        self.plateTextIR.setScaledContents(False)
        self.plateTextIR.setAlignment(Qt.AlignCenter)
        self.plateTextNum = QLabel(self.centralwidget)
        self.plateTextNum.setObjectName(u"plateTextNum")
        self.plateTextNum.setEnabled(True)
        self.plateTextNum.setGeometry(QRect(240, 180, 201, 62))
        sizePolicy1.setHeightForWidth(self.plateTextNum.sizePolicy().hasHeightForWidth())
        self.plateTextNum.setSizePolicy(sizePolicy1)
        self.plateTextNum.setMaximumSize(QSize(300, 62))
        font2 = QFont()
        font2.setFamilies([u"B Yekan"])
        font2.setPointSize(28)
        font2.setKerning(True)
        self.plateTextNum.setFont(font2)
        self.plateTextNum.setLayoutDirection(Qt.LeftToRight)
        self.plateTextNum.setAutoFillBackground(False)
        self.plateTextNum.setStyleSheet(u"letter-spacing: 3px;\n"
"                        padding-bottom: 5%;\n"
"                    ")
        self.plateTextNum.setFrameShape(QFrame.NoFrame)
        self.plateTextNum.setTextFormat(Qt.PlainText)
        self.plateTextNum.setScaledContents(False)
        self.plateTextNum.setAlignment(Qt.AlignCenter)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"License plate image", None))
        self.plateView.setText("")
        self.plateTextView.setText("")
        self.plateTextIR.setText("")
        self.plateTextNum.setText("")
    # retranslateUi

