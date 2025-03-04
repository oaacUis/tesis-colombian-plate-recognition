import datetime
import sqlite3
import time
import os

from services.send import send_data_to_external_service  # noqa
from configParams import Parameters
from database.classEntries import Entries
from helper.text_decorators import check_similarity_threshold

params = Parameters()

fieldsList = ["platePercent", "charPercent",
              "eDate", "eTime",
              "plateNum", "status"]
dbEntries = params.dbEntries


def insertEntries(entry):
    sqlConnect = sqlite3.connect(dbEntries)
    sqlCursor = sqlConnect.cursor()

    sqlCursor.execute(
        "INSERT OR IGNORE INTO entries VALUES (:platePercent, :charPercent, :eDate, :eTime, :plateNum, :status)", # noqa
        vars(entry),
    )

    sqlConnect.commit()
    sqlConnect.close()


def dbRemoveEntries(plateNumber):
    sqlConnect = sqlite3.connect(dbEntries)
    sqlCursor = sqlConnect.cursor()
    removeEntriesSQL = f"""DELETE FROM entries WHERE plateNum='{plateNumber}'"""  # noqa
    removeEntries = sqlCursor.execute(removeEntriesSQL)  # noqa
    sqlConnect.commit()
    sqlConnect.close()


def dbGetPlateLatestEntry(plateNumber):
    sqlConnect = sqlite3.connect(dbEntries)
    sqlCursor = sqlConnect.cursor()

    FullEntriesSQL = f"""SELECT * FROM entries WHERE plateNum='{plateNumber}' ORDER BY eDate DESC LIMIT 1"""  # noqa
    FullEntries = sqlCursor.execute(FullEntriesSQL).fetchall()

    if len(FullEntries) != 0:
        FullData = dict(zip([c[0] for c in sqlCursor.description], FullEntries[0]))  # noqa
        sqlConnect.commit()
        sqlConnect.close()
        return Entries(**FullData)
    return None


def dbGetPlateStatus(plateNum):
    with sqlite3.connect(dbEntries) as sqlConnect:
        sqlCursor = sqlConnect.cursor()
        plateStatusSQL = "SELECT plateNum,statusNum FROM PlateStatus WHERE plateNum = ?"  # noqa
        status = sqlCursor.execute(plateStatusSQL, (plateNum,)).fetchone()
        if status is None:
            return 0
        else:
            return status[1]


def dbGetAllEntries(limit=10, orderBy="eDate", orderType="DESC", whereLike=""):
    listAllEntries = []
    sqlConnect = sqlite3.connect(dbEntries)
    sqlCursor = sqlConnect.cursor()
    allEntriesSQL = f"""SELECT * FROM entries WHERE plateNum LIKE '%{whereLike}%' ORDER BY {orderBy} {orderType} , eTime {orderType} LIMIT {limit} """  # noqa
    allEntries = sqlCursor.execute(allEntriesSQL).fetchall()
    for i in range(len(allEntries)):
        FullData = dict(zip([c[0] for c in sqlCursor.description], allEntries[i]))  # noqa
        listAllEntries.append(Entries(**FullData))
    sqlConnect.commit()
    sqlCursor.close()
    sqlConnect.close()
    return listAllEntries


similarityTemp = ""


def db_entries_time(
    number,
    charConfAvg,
    plateConfAvg,
    croppedPlate,
    status,
    external_service_data: dict = None,
):
    global similarityTemp
    # print(f"[DEBUG] External Service Data: {external_service_data}")
    # print(f"[DEBUG] Tipo de objeto: {type(croppedPlate)}")
    isSimilar = check_similarity_threshold(similarityTemp, number)
    if not isSimilar:
        similarityTemp = number
        if True:
            timeNow = datetime.now()
            result = dbGetPlateLatestEntry(number)
            if result is not None and number != "":

                strTime = result.getTime()
                strDate = result.getDate()
                if timeDifference(strTime, strDate):
                    display_time = timeNow.strftime("%H:%M:%S")
                    display_date = timeNow.strftime("%Y-%m-%d")

                    os.makedirs("temp", exist_ok=True)
                    plateImgName = os.path.join(
                        "temp",
                        f"{number}_{datetime.now().strftime('%H-%M-%S_%Y-%m-%d')}.jpg",  # noqa
                    )
                    saved = croppedPlate.save(plateImgName, "JPEG")

                    entries = Entries(
                        plateConfAvg,
                        charConfAvg,
                        display_date,
                        display_time,
                        number,
                        status,
                    )

                    insertEntries(entries)
                    # send_data_to_external_service(external_service_data)
                else:
                    pass
            else:
                if number != "":
                    display_time = time.strftime("%H:%M:%S")
                    display_date = time.strftime("%Y-%m-%d")

                    os.makedirs("temp", exist_ok=True)
                    plateImgName = os.path.join(
                        "temp",
                        f"{number}_{datetime.now().strftime('%H-%M-%S_%Y-%m-%d')}.jpg",  # noqa
                    )

                    saved = croppedPlate.save(plateImgName, "JPEG")  # noqa

                    entries = Entries(
                        plateConfAvg,
                        charConfAvg,
                        display_date,
                        display_time,
                        number,
                        status,
                    )

                    insertEntries(entries)
                    # send_data_to_external_service(external_service_data)


def getFieldNames(fieldsList):
    fieldNamesOutput = []
    for value in fieldsList:
        fieldNamesOutput.append(params.fieldNames[value])
    return fieldNamesOutput


from datetime import datetime  # noqa


def timeDifference(strTime, strDate):
    start_time = datetime.strptime(strTime + " " + strDate, "%H:%M:%S %Y-%m-%d")  # noqa
    end_time = datetime.strptime(
        datetime.now().strftime("%H:%M:%S %Y-%m-%d"), "%H:%M:%S %Y-%m-%d"
    )
    delta = end_time - start_time

    sec = delta.total_seconds()
    min = (sec / 60).__ceil__()

    if min > 1:
        return True
    else:
        return False
