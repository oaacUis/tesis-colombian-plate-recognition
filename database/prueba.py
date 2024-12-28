#classEntries

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QTableWidgetItem

from helper import jalali
from helper.gui_maker import get_status_color, get_status_text
from helper.text_decorators import convert_english_to_persian, split_string_language_specific


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

    def getDate(self, persian=True):
        if persian:
            return jalali.Gregorian(self.eDate).persian_string()
        return self.eDate

    def getPlatePic(self):
        return 'temp/{}_{}_{}.jpg'.format(self.plateNum, self.eTime, self.eDate)

    def getCharPercent(self):
        return "{}%".format(self.charPercent)

    def getPlatePercent(self):
        return "{}%".format(self.platePercent)

    def getPlateNumber(self, display=False):
        return convert_english_to_persian(split_string_language_specific(self.plateNum), display)

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














































#classResidents
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QTableWidgetItem

from helper.gui_maker import get_status_text, get_status_color
from helper.text_decorators import convert_english_to_persian, split_string_language_specific


class Resident:

    def __init__(self, fName, lName, building, block, num, carModel, plateNum, status
                 ):
        self.fName = fName
        self.lName = lName
        self.building = building
        self.block = block
        self.num = num
        self.carModel = carModel
        self.plateNum = plateNum
        self.status = status

    def getFirstName(self):
        return self.fName

    def getLastName(self):
        return self.lName

    def getFullName(self):
        return '{} {}'.format(self.fName, self.lName)

    def getBuilding(self, appendBuilding=True):
        if appendBuilding:
            return '{}{}'.format(self.building, ' طبقه ')
        else:
            return str(self.building)

    def getBlock(self):
        return str(self.block)

    def getNum(self):
        return str(self.num)

    def getCarModel(self):
        return self.carModel

    def getPlateNumber(self, display=False):
        return convert_english_to_persian(split_string_language_specific(self.plateNum), display)

    def getStatus(self, item=True):
        if item:
            statusData = self.status
            r, g, b = get_status_color(statusData)
            statusText = get_status_text(statusData)
            statusItem = QTableWidgetItem(statusText)
            statusItem.setBackground(QColor(r, g, b))
            return statusItem
        return str(self.status)
    






























#db_entries_utils.py
import datetime
import sqlite3
import time

from services.send import send_data_to_external_service
from configParams import Parameters
from database.classEntries import Entries
from helper.text_decorators import check_similarity_threshold

params = Parameters()

fieldsList = ['platePercent', 'charPercent', 'eDate', 'eTime', 'plateNum', 'status']
dbEntries = params.dbEntries


def insertEntries(entry):
    sqlConnect = sqlite3.connect(dbEntries)
    sqlCursor = sqlConnect.cursor()

    sqlCursor.execute(
        "INSERT OR IGNORE INTO entries VALUES (:platePercent, :charPercent, :eDate, :eTime, :plateNum, :status)",
        vars(entry))

    sqlConnect.commit()
    sqlConnect.close()


def dbRemoveEntries(plateNumber):
    sqlConnect = sqlite3.connect(dbEntries)
    sqlCursor = sqlConnect.cursor()
    removeEntriesSQL = f"""DELETE FROM entries WHERE plateNum='{plateNumber}'"""
    removeEntries = sqlCursor.execute(removeEntriesSQL)
    sqlConnect.commit()
    sqlConnect.close()


def dbGetPlateLatestEntry(plateNumber):
    sqlConnect = sqlite3.connect(dbEntries)
    sqlCursor = sqlConnect.cursor()

    FullEntriesSQL = f"""SELECT * FROM entries WHERE plateNum='{plateNumber}' ORDER BY eDate DESC LIMIT 1"""
    FullEntries = sqlCursor.execute(FullEntriesSQL).fetchall()

    if len(FullEntries) != 0:
        FullData = dict(zip([c[0] for c in sqlCursor.description], FullEntries[0]))
        sqlConnect.commit()
        sqlConnect.close()

        return Entries(**FullData)
    return None


def dbGetPlateStatus(plateNum):
    with sqlite3.connect(dbEntries) as sqlConnect:
        sqlCursor = sqlConnect.cursor()
        plateStatusSQL = "SELECT plateNum,statusNum FROM PlateStatus WHERE plateNum = ?"
        status = sqlCursor.execute(plateStatusSQL, (plateNum,)).fetchone()
        if status is None:
            return 0
        else:
            return status[1]


def dbGetAllEntries(limit=10, orderBy='eDate', orderType='DESC', whereLike=''):
    listAllEntries = []
    sqlConnect = sqlite3.connect(dbEntries)
    sqlCursor = sqlConnect.cursor()
    allEntriesSQL = f"""SELECT * FROM entries WHERE plateNum LIKE '%{whereLike}%' ORDER BY {orderBy} {orderType} , eTime {orderType} LIMIT {limit} """
    allEntries = sqlCursor.execute(allEntriesSQL).fetchall()
    for i in range(len(allEntries)):
        FullData = dict(zip([c[0] for c in sqlCursor.description], allEntries[i]))
        listAllEntries.append(Entries(**FullData))
    sqlConnect.commit()
    sqlCursor.close()
    sqlConnect.close()

    return listAllEntries


similarityTemp = ''


def db_entries_time(number, charConfAvg, plateConfAvg, croppedPlate, status, external_service_data: dict = None):
    global similarityTemp
    isSimilar = check_similarity_threshold(similarityTemp, number)
    if not isSimilar:
        similarityTemp = number
        if True:
            timeNow = datetime.now()
            result = dbGetPlateLatestEntry(number)
            if result is not None and number != '':

                strTime = result.getTime()
                strDate = result.getDate()
                if timeDifference(strTime, strDate):
                    display_time = timeNow.strftime("%H:%M:%S")
                    display_date = timeNow.strftime("%Y-%m-%d")

                    plateImgName = 'temp/{}_{}.jpg'.format(number,
                                                           datetime.now().strftime("%H:%M:%S_%Y-%m-%d"))
                    croppedPlate.save(plateImgName, format='jpg')

                    entries = Entries(plateConfAvg, charConfAvg, display_date, display_time, number, status)

                    insertEntries(entries)
                    send_data_to_external_service(external_service_data)
                else:
                    pass
            else:
                if number != '':
                    display_time = time.strftime("%H:%M:%S")
                    display_date = time.strftime("%Y-%m-%d")

                    plateImgName = 'temp/{}_{}.jpg'.format(number, datetime.now().strftime("%H:%M:%S_%Y-%m-%d"))
                    croppedPlate.save(plateImgName, format='jpg')

                    entries = Entries(plateConfAvg, charConfAvg, display_date, display_time, number, status)

                    insertEntries(entries)
                    send_data_to_external_service(external_service_data)


def getFieldNames(fieldsList):
    fieldNamesOutput = []
    for value in fieldsList:
        fieldNamesOutput.append(params.fieldNames[value])
    return fieldNamesOutput


from datetime import datetime


def timeDifference(strTime, strDate):
    start_time = datetime.strptime(strTime + ' ' + strDate, "%H:%M:%S %Y-%m-%d")
    end_time = datetime.strptime(datetime.now().strftime("%H:%M:%S %Y-%m-%d"), "%H:%M:%S %Y-%m-%d")
    delta = end_time - start_time

    sec = delta.total_seconds()
    min = (sec / 60).__ceil__()

    if min > 1:
        return True
    else:
        return False






































#db_resident_utils.py
import datetime
import sqlite3
import time

from configParams import Parameters
from database.classResidents import Resident
from helper.text_decorators import convert_persian_to_english, join_elements

params = Parameters()

fieldsList = ['fName', 'lName', 'building', 'block', 'num', 'carModel', 'plateNum', 'status']
dbResidents = params.dbResidents


def insertResident(resident, update=False, editingPlate=''):
    try:
        sqlConnect = sqlite3.connect(dbResidents)
        sqlCursor = sqlConnect.cursor()

        if update:
            pltNum = join_elements(convert_persian_to_english(resident.getPlateNumber()))

            updateResidentSQL = f"""UPDATE
                                residents
                                SET
                                fName = :fName,
                                lName= :lName,
                                building= :building,
                                block= :block,
                                num= :num,
                                carModel= :carModel,
                                plateNum= :plateNum,
                                status = :status
                                WHERE
                                plateNum= :editingPlate"""
            dlist = vars(resident)
            dlist['editingPlate'] = editingPlate
            sqlCursor.execute(updateResidentSQL, dlist)

        else:
            sqlCursor.execute(
                "INSERT OR IGNORE INTO residents VALUES (:fName, :lName, :building, :block, :num, :carModel, :plateNum, :status)",
                vars(resident))

        sqlCursor.close()
    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)

    finally:
        if sqlConnect:
            sqlConnect.commit()
            sqlConnect.close()


def getResidentByName(conn, cur, lastname):
    cur.execute("SELECT * FROM residents WHERE last=:last", {'last': lastname})
    return cur.fetchall()


def updateResident(conn, cur, resident, pay):
    with conn:
        cur.execute("""UPDATE residents SET pay = :pay
                    WHERE first = :first AND last = :last""",
                    {'first': resident.first, 'last': resident.last, 'pay': pay})


def dbRemoveResident(plateNumber):
    sqlConnect = sqlite3.connect(dbResidents)
    sqlCursor = sqlConnect.cursor()
    removeResidentSQL = f"""DELETE FROM residents WHERE plateNum='{plateNumber}'"""
    removeResident = sqlCursor.execute(removeResidentSQL)
    sqlConnect.commit()
    sqlConnect.close()


def dbGetPlateExist(plateNumber):
    sqlConnect = sqlite3.connect(dbResidents)
    sqlCursor = sqlConnect.cursor()
    PlateExistSQL = f"""SELECT status FROM residents WHERE plateNum='{plateNumber}'"""
    PlateExist = sqlCursor.execute(PlateExistSQL).fetchone()
    sqlConnect.commit()
    sqlConnect.close()
    if PlateExist is not None:
        return True
    else:
        return False


def db_get_plate_status(plateNumber):
    sqlConnect = sqlite3.connect(dbResidents)
    sqlCursor = sqlConnect.cursor()
    PlateStatusSQL = f"""SELECT status FROM residents WHERE plateNum='{plateNumber}'"""
    PlateStatus = sqlCursor.execute(PlateStatusSQL).fetchone()
    sqlConnect.commit()
    sqlConnect.close()

    if PlateStatus is not None:
        return PlateStatus[0]
    return 2


def db_get_plate_owner_name(plateNumber):
    sqlConnect = sqlite3.connect(dbResidents)
    sqlCursor = sqlConnect.cursor()
    OwnerNameSQL = f"""SELECT fName, lName FROM residents WHERE plateNum='{plateNumber}'"""
    OwnerName = sqlCursor.execute(OwnerNameSQL).fetchone()
    sqlConnect.commit()
    sqlConnect.close()
    if OwnerName is not None:
        return '{} {}'.format(OwnerName[0], OwnerName[1])
    return None


def dbGetResidentDatasByPlate(plateNumber):
    sqlConnect = sqlite3.connect(dbResidents)
    sqlCursor = sqlConnect.cursor()

    FullResidentSQL = f"""SELECT * FROM residents WHERE plateNum='{plateNumber}'"""
    FullResident = sqlCursor.execute(FullResidentSQL).fetchall()

    FullData = dict(zip([c[0] for c in sqlCursor.description], FullResident[0]))
    sqlConnect.commit()
    sqlConnect.close()
    if FullResident is not None:
        return Resident(**FullData)
    return None


def dbGetResidentDatasBylName(lName):
    sqlConnect = sqlite3.connect(dbResidents)
    sqlCursor = sqlConnect.cursor()
    FullResidentSQL = f"""SELECT * FROM residents WHERE lName LIKE '%{lName}%'"""
    FullResident = sqlCursor.execute(FullResidentSQL).fetchall()
    FullData = dict(zip([c[0] for c in sqlCursor.description], FullResident[0]))
    sqlConnect.commit()
    sqlConnect.close()
    if FullResident is not None:
        return Resident(**FullData)
    return None


def dbGetAllResidents(limit=100, orderBy='lName', orderType='ASC', whereLike=''):
    listAllResidents = []
    sqlConnect = sqlite3.connect(dbResidents)
    sqlCursor = sqlConnect.cursor()
    allResidentSQL = f"""SELECT * FROM residents WHERE lName LIKE '%{whereLike}%' ORDER BY {orderBy} {orderType} LIMIT {limit} """
    allResident = sqlCursor.execute(allResidentSQL).fetchall()
    for i in range(len(allResident)):
        FullData = dict(zip([c[0] for c in sqlCursor.description], allResident[i]))
        listAllResidents.append(Resident(**FullData))
    sqlConnect.commit()
    sqlConnect.close()
    return listAllResidents


similarityTemp = ''


def dbEnteriesTime(number, charConfAvg, plateConfAvg, croppedPlate, status):
    global similarityTemp
    dfReadEnteries = pd.read_csv(str(Path().absolute()) + '/base/enteries.csv')

    isSimilar = similarityChecker(similarityTemp, number)

    if not isSimilar:
        similarityTemp = number
        if True:

            timeNow = datetime.now()
            result = dfReadEnteries[dfReadEnteries['plateNum'] == number]
            if result is not None and not result.empty and number != '':

                inn = result.index.to_list()[len(result.index) - 1]
                strTime = dfReadEnteries.at[dfReadEnteries.index[inn], 'time']
                strDate = dfReadEnteries.at[dfReadEnteries.index[inn], 'date']
                if timeDifference(strTime, strDate):
                    display_time = timeNow.strftime("%H:%M:%S")
                    display_date = timeNow.strftime("%Y-%m-%d")

                    plateImgName = 'temp/{}-{}.jpg'.format(number,
                                                           datetime.now().strftime("%H:%M:%S %Y-%m-%d"))
                    croppedPlate.save(plateImgName, format='jpg')

                    enteriesExport = {'status': [status], 'plateNum': [number], 'time': [display_time],
                                      'date': [display_date]
                        , 'platePic': plateImgName, 'charPercent': [charConfAvg], 'platePercent': [plateConfAvg]
                                      }
                    df = pd.DataFrame(enteriesExport)
                    df.to_csv(str(Path().absolute()) + '/base/enteries.csv', header=False, index=False, mode='a',
                              encoding='utf-8')

                else:
                    pass
            else:
                if number != '':
                    display_time = time.strftime("%H:%M:%S")
                    display_date = time.strftime("%Y-%m-%d")

                    plateImgName = 'temp/{}-{}.jpg'.format(number, datetime.now().strftime("%H:%M:%S-%Y-%m-%d"))
                    croppedPlate.save(plateImgName, format='jpg')

                    enteriesExport = {'status': [status], 'plateNum': [number], 'time': [display_time],
                                      'date': [display_date]
                        , 'platePic': plateImgName, 'charPercent': [charConfAvg], 'platePercent': [plateConfAvg]
                                      }
                    df = pd.DataFrame(enteriesExport)
                    df.to_csv(str(Path().absolute()) + '/base/enteries.csv', header=False, index=False, mode='a',
                              encoding='utf-8')
    else:
        pass


def dbRefreshTable():
    dfReadEnteries = pd.read_csv(str(Path().absolute()) + '/base/enteries.csv')
    dfReadEnteries = dfReadEnteries.iloc[-20:].sort_index(ascending=False)
    return dfReadEnteries


def getFieldNames(fieldsList):
    fieldNamesOutput = []
    for value in fieldsList:
        fieldNamesOutput.append(params.fieldNames[value])
    return fieldNamesOutput


from datetime import datetime


def timeDifference(strTime, strDate):
    start_time = datetime.strptime(strTime + ' ' + strDate, "%H:%M:%S %Y-%m-%d")
    end_time = datetime.strptime(datetime.now().strftime("%H:%M:%S %Y-%m-%d"), "%H:%M:%S %Y-%m-%d")
    delta = end_time - start_time

    sec = delta.total_seconds()
    min = (sec / 60).__ceil__()

    if min > 1:
        return True
    else:
        return False

