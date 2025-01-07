#classEntries.py

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QTableWidgetItem

from helper.gui_maker import get_status_color, get_status_text

from datetime import datetime



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
        # Debug prints
        print(f"eDate value: {self.eDate}")
        print(f"eDate type: {type(self.eDate)}")
        print(f"eDate format: {self.eDate.strftime('%c')}")  # Full date format   
        return self.eDate.strftime("%d/%m/%Y")

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
    

# Create test instance
entry = Entries(
    platePercent=95,
    charPercent=90,
    eDate=datetime.now(),
    eTime="10:30:00",
    plateNum="ABC123",
    status=1
)

# Test getDate
print(entry.getDate())

