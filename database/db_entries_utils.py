<<<<<<< HEAD
=======
# db_entries_utils.py
"""
This module contains functions for database interactions and entry management.
It handles database operations for vehicle entries, including status tracking and time-based operations.
"""

>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
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
<<<<<<< HEAD
=======
    """
    Insert a new entry into the database.

    Args:
        entry (Entries): Entry object containing vehicle data
    """
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
    sqlConnect = sqlite3.connect(dbEntries)
    sqlCursor = sqlConnect.cursor()

    sqlCursor.execute(
        "INSERT OR IGNORE INTO entries VALUES (:platePercent, :charPercent, :eDate, :eTime, :plateNum, :status)",
        vars(entry))

    sqlConnect.commit()
    sqlConnect.close()


def dbRemoveEntries(plateNumber):
<<<<<<< HEAD
    sqlConnect = sqlite3.connect(dbEntries)
    sqlCursor = sqlConnect.cursor()
    removeEntriesSQL = f"""DELETE FROM entries WHERE plateNum='{plateNumber}'"""
    removeEntries = sqlCursor.execute(removeEntriesSQL)
=======
    """
    Remove all entries for a specific plate number.

    Args:
        plateNumber (str): License plate number to remove
    """
    sqlConnect = sqlite3.connect(dbEntries)
    sqlCursor = sqlConnect.cursor()
    removeEntriesSQL = f"""DELETE FROM entries WHERE plateNum='{plateNumber}'"""
    sqlCursor.execute(removeEntriesSQL)
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
    sqlConnect.commit()
    sqlConnect.close()


def dbGetPlateLatestEntry(plateNumber):
<<<<<<< HEAD
=======
    """
    Get the most recent entry for a specific plate number.

    Args:
        plateNumber (str): License plate number to search

    Returns:
        Entries: Latest entry object if found, None otherwise
    """
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
    sqlConnect = sqlite3.connect(dbEntries)
    sqlCursor = sqlConnect.cursor()

    FullEntriesSQL = f"""SELECT * FROM entries WHERE plateNum='{plateNumber}' ORDER BY eDate DESC LIMIT 1"""
    FullEntries = sqlCursor.execute(FullEntriesSQL).fetchall()

    if len(FullEntries) != 0:
        FullData = dict(zip([c[0] for c in sqlCursor.description], FullEntries[0]))
        sqlConnect.commit()
        sqlConnect.close()
<<<<<<< HEAD

=======
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
        return Entries(**FullData)
    return None


def dbGetPlateStatus(plateNum):
<<<<<<< HEAD
=======
    """
    Get the current status of a license plate.

    Args:
        plateNum (str): License plate number

    Returns:
        int: Status code (0: Unauthorized, 1: Authorized, 2: Unregistered)
    """
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
    with sqlite3.connect(dbEntries) as sqlConnect:
        sqlCursor = sqlConnect.cursor()
        plateStatusSQL = "SELECT plateNum,statusNum FROM PlateStatus WHERE plateNum = ?"
        status = sqlCursor.execute(plateStatusSQL, (plateNum,)).fetchone()
<<<<<<< HEAD
        if status is None:
            return 0
        else:
            return status[1]


def dbGetAllEntries(limit=10, orderBy='eDate', orderType='DESC', whereLike=''):
=======
        return 0 if status is None else status[1]


def dbGetAllEntries(limit=10, orderBy='eDate', orderType='DESC', whereLike=''):
    """
    Retrieve all entries with specified filtering and ordering.

    Args:
        limit (int): Maximum number of entries to retrieve
        orderBy (str): Column to order results by
        orderType (str): Order direction ('ASC' or 'DESC')
        whereLike (str): Filter string for plate numbers

    Returns:
        list[Entries]: List of entry objects matching criteria
    """
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
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
<<<<<<< HEAD

=======
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
    return listAllEntries


similarityTemp = ''


def db_entries_time(number, charConfAvg, plateConfAvg, croppedPlate, status, external_service_data: dict = None):
<<<<<<< HEAD
=======
    """
    Process and store a new entry with time-based validation.

    Args:
        number (str): License plate number
        charConfAvg (float): Character recognition confidence
        plateConfAvg (float): Plate detection confidence
        croppedPlate: Image of the license plate
        status (int): Entry status code
        external_service_data (dict, optional): Data to send to external service
    """
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
    global similarityTemp
    isSimilar = check_similarity_threshold(similarityTemp, number)
    if not isSimilar:
        similarityTemp = number
<<<<<<< HEAD
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
=======
        timeNow = datetime.now()
        result = dbGetPlateLatestEntry(number)
        
        if result is not None and number != '':
            strTime = result.getTime()
            strDate = result.getDate()
            if timeDifference(strTime, strDate):
                display_time = timeNow.strftime("%H:%M:%S")
                display_date = timeNow.strftime("%Y-%m-%d")

                plateImgName = 'temp/{}_{}.jpg'.format(
                    number,
                    datetime.now().strftime("%H:%M:%S_%Y-%m-%d")
                )
                croppedPlate.save(plateImgName, format='jpg')

                entries = Entries(plateConfAvg, charConfAvg, display_date, display_time, number, status)
                insertEntries(entries)
                send_data_to_external_service(external_service_data)
        elif number != '':
            display_time = time.strftime("%H:%M:%S")
            display_date = time.strftime("%Y-%m-%d")

            plateImgName = 'temp/{}_{}.jpg'.format(
                number,
                datetime.now().strftime("%H:%M:%S_%Y-%m-%d")
            )
            croppedPlate.save(plateImgName, format='jpg')

            entries = Entries(plateConfAvg, charConfAvg, display_date, display_time, number, status)
            insertEntries(entries)
            send_data_to_external_service(external_service_data)


def getFieldNames(fieldsList):
    """
    Get display names for database fields.

    Args:
        fieldsList (list): List of field names

    Returns:
        list: List of translated field names
    """
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
    fieldNamesOutput = []
    for value in fieldsList:
        fieldNamesOutput.append(params.fieldNames[value])
    return fieldNamesOutput


<<<<<<< HEAD
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
=======
def timeDifference(strTime, strDate):
    """
    Check if enough time has passed between entries.

    Args:
        strTime (str): Time string in format "HH:MM:SS"
        strDate (str): Date string in format "YYYY-MM-DD"

    Returns:
        bool: True if more than 1 minute has passed, False otherwise
    """
    start_time = datetime.strptime(f"{strTime} {strDate}", "%H:%M:%S %Y-%m-%d")
    end_time = datetime.strptime(
        datetime.now().strftime("%H:%M:%S %Y-%m-%d"),
        "%H:%M:%S %Y-%m-%d"
    )
    delta = end_time - start_time
    minutes = (delta.total_seconds() / 60).__ceil__()
    return minutes > 1
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
