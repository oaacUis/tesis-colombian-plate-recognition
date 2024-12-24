from PySide6.QtGui import QColor
from PySide6.QtWidgets import QTableWidgetItem

from helper import jalali
from helper.gui_maker import get_status_color, get_status_text


class Entries:

    def __init__(self, platePercent, charPercent, eDate, eTime, plateNum, status):
        self.status = status
        self.plateNum = plateNum
        self.eTime = eTime
        self.eDate = eDate

        self.charPercent = charPercent
        self.platePercent = platePercent

    def getTime(self):
        return self.eTime

    def getDate(self):
        # if persian:
        #     return jalali.Gregorian(self.eDate).get_date_str()
        return jalali.Gregorian(self.eDate).get_date_str()
        # return self.eDate

    def getPlatePic(self):
        return 'temp/{}_{}_{}.jpg'.format(self.plateNum, self.eTime, self.eDate)

    def getCharPercent(self):
        return "{}%".format(self.charPercent)

    def getPlatePercent(self):
        return "{}%".format(self.platePercent)

    def getPlateNumber(self):
        return self.plateNum

    def getStatus(self, item=True, statusNum='', selfNum=False):
        if item:

            if selfNum:
                statusData = self.status
            else:
                statusData = statusNum

            r, g, b = get_status_color(statusData)

            statusText = get_status_text(statusData)
            statusItem = QTableWidgetItem(statusText)

            statusItem.setBackground(QColor(r, g, b))
            return statusItem
        return self.status
