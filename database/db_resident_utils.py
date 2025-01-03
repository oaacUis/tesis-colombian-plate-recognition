<<<<<<< HEAD
import datetime
import sqlite3
import time

from configParams import Parameters
from database.classResidents import Resident
from helper.text_decorators import convert_persian_to_english, join_elements
=======
# db_resident_utils.py
"""
This module manages database operations for resident information.
It provides utilities for CRUD operations on resident data.
"""

import datetime
import sqlite3
import time
import pandas as pd
from pathlib import Path

from configParams import Parameters
from database.classResidents import Resident
from helper.text_decorators import convert_to_standard_format, join_elements, check_similarity_threshold
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388

params = Parameters()

fieldsList = ['fName', 'lName', 'building', 'block', 'num', 'carModel', 'plateNum', 'status']
dbResidents = params.dbResidents


def insertResident(resident, update=False, editingPlate=''):
<<<<<<< HEAD
=======
    """
    Insert or update resident information in the database.

    Args:
        resident (Resident): Resident object containing data
        update (bool): If True, updates existing record; if False, inserts new record
        editingPlate (str): Original plate number for update operations
    """
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
    try:
        sqlConnect = sqlite3.connect(dbResidents)
        sqlCursor = sqlConnect.cursor()

        if update:
<<<<<<< HEAD
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

=======
            pltNum = join_elements(convert_to_standard_format(resident.getPlateNumber()))
            updateResidentSQL = """UPDATE residents 
                               SET fName=:fName, lName=:lName, building=:building,
                               block=:block, num=:num, carModel=:carModel,
                               plateNum=:plateNum, status=:status
                               WHERE plateNum=:editingPlate"""
            dlist = vars(resident)
            dlist['editingPlate'] = editingPlate
            sqlCursor.execute(updateResidentSQL, dlist)
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
        else:
            sqlCursor.execute(
                "INSERT OR IGNORE INTO residents VALUES (:fName, :lName, :building, :block, :num, :carModel, :plateNum, :status)",
                vars(resident))

        sqlCursor.close()
    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
<<<<<<< HEAD

=======
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
    finally:
        if sqlConnect:
            sqlConnect.commit()
            sqlConnect.close()


def getResidentByName(conn, cur, lastname):
<<<<<<< HEAD
=======
    """
    Retrieve resident information by last name.
    """
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
    cur.execute("SELECT * FROM residents WHERE last=:last", {'last': lastname})
    return cur.fetchall()


def updateResident(conn, cur, resident, pay):
<<<<<<< HEAD
    with conn:
        cur.execute("""UPDATE residents SET pay = :pay
                    WHERE first = :first AND last = :last""",
=======
    """
    Update resident payment information.
    """
    with conn:
        cur.execute("""UPDATE residents SET pay=:pay
                    WHERE first=:first AND last=:last""",
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
                    {'first': resident.first, 'last': resident.last, 'pay': pay})


def dbRemoveResident(plateNumber):
<<<<<<< HEAD
    sqlConnect = sqlite3.connect(dbResidents)
    sqlCursor = sqlConnect.cursor()
    removeResidentSQL = f"""DELETE FROM residents WHERE plateNum='{plateNumber}'"""
    removeResident = sqlCursor.execute(removeResidentSQL)
=======
    """
    Remove a resident from the database by plate number.
    """
    sqlConnect = sqlite3.connect(dbResidents)
    sqlCursor = sqlConnect.cursor()
    removeResidentSQL = f"""DELETE FROM residents WHERE plateNum='{plateNumber}'"""
    sqlCursor.execute(removeResidentSQL)
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
    sqlConnect.commit()
    sqlConnect.close()


def dbGetPlateExist(plateNumber):
<<<<<<< HEAD
=======
    """
    Check if a plate number exists in the database.
    """
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
    sqlConnect = sqlite3.connect(dbResidents)
    sqlCursor = sqlConnect.cursor()
    PlateExistSQL = f"""SELECT status FROM residents WHERE plateNum='{plateNumber}'"""
    PlateExist = sqlCursor.execute(PlateExistSQL).fetchone()
    sqlConnect.commit()
    sqlConnect.close()
<<<<<<< HEAD
    if PlateExist is not None:
        return True
    else:
        return False


def db_get_plate_status(plateNumber):
=======
    return PlateExist is not None


def db_get_plate_status(plateNumber):
    """
    Get the status of a plate number.
    Returns 2 if plate not found (Unregistered).
    """
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
    sqlConnect = sqlite3.connect(dbResidents)
    sqlCursor = sqlConnect.cursor()
    PlateStatusSQL = f"""SELECT status FROM residents WHERE plateNum='{plateNumber}'"""
    PlateStatus = sqlCursor.execute(PlateStatusSQL).fetchone()
    sqlConnect.commit()
    sqlConnect.close()
<<<<<<< HEAD

    if PlateStatus is not None:
        return PlateStatus[0]
    return 2


def db_get_plate_owner_name(plateNumber):
=======
    return PlateStatus[0] if PlateStatus is not None else 2


def db_get_plate_owner_name(plateNumber):
    """
    Get the owner's full name by plate number.
    """
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
    sqlConnect = sqlite3.connect(dbResidents)
    sqlCursor = sqlConnect.cursor()
    OwnerNameSQL = f"""SELECT fName, lName FROM residents WHERE plateNum='{plateNumber}'"""
    OwnerName = sqlCursor.execute(OwnerNameSQL).fetchone()
    sqlConnect.commit()
    sqlConnect.close()
<<<<<<< HEAD
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
=======
    return '{} {}'.format(OwnerName[0], OwnerName[1]) if OwnerName else None


def dbGetResidentDatasByPlate(plateNumber):
    """
    Get complete resident information by plate number.
    """
    sqlConnect = sqlite3.connect(dbResidents)
    sqlCursor = sqlConnect.cursor()
    FullResidentSQL = f"""SELECT * FROM residents WHERE plateNum='{plateNumber}'"""
    FullResident = sqlCursor.execute(FullResidentSQL).fetchall()
    
    if FullResident:
        FullData = dict(zip([c[0] for c in sqlCursor.description], FullResident[0]))
        sqlConnect.commit()
        sqlConnect.close()
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
        return Resident(**FullData)
    return None


def dbGetResidentDatasBylName(lName):
<<<<<<< HEAD
=======
    """
    Get resident information by last name.
    """
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
    sqlConnect = sqlite3.connect(dbResidents)
    sqlCursor = sqlConnect.cursor()
    FullResidentSQL = f"""SELECT * FROM residents WHERE lName LIKE '%{lName}%'"""
    FullResident = sqlCursor.execute(FullResidentSQL).fetchall()
<<<<<<< HEAD
    FullData = dict(zip([c[0] for c in sqlCursor.description], FullResident[0]))
    sqlConnect.commit()
    sqlConnect.close()
    if FullResident is not None:
=======
    
    if FullResident:
        FullData = dict(zip([c[0] for c in sqlCursor.description], FullResident[0]))
        sqlConnect.commit()
        sqlConnect.close()
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
        return Resident(**FullData)
    return None


def dbGetAllResidents(limit=100, orderBy='lName', orderType='ASC', whereLike=''):
<<<<<<< HEAD
=======
    """
    Get all residents with filtering and ordering options.
    """
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
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
<<<<<<< HEAD
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
=======
    """
    Record entry time for a vehicle with similarity checking.

    Args:
        number (str): License plate number
        charConfAvg (float): Character recognition confidence average
        plateConfAvg (float): Plate detection confidence average
        croppedPlate: Image of the license plate
        status (int): Status code of the entry

    Returns:
        None
    """
    global similarityTemp
    dfReadEnteries = pd.read_csv(str(Path().absolute()) + '/base/enteries.csv')

    # Cambiamos similarityChecker por check_similarity_threshold
    if not check_similarity_threshold(similarityTemp, number):
        similarityTemp = number
        timeNow = datetime.now()
        result = dfReadEnteries[dfReadEnteries['plateNum'] == number]
        
        if result is not None and not result.empty and number != '':
            inn = result.index.to_list()[len(result.index) - 1]
            strTime = dfReadEnteries.at[dfReadEnteries.index[inn], 'time']
            strDate = dfReadEnteries.at[dfReadEnteries.index[inn], 'date']
            
            if timeDifference(strTime, strDate):
                _save_entry(number, charConfAvg, plateConfAvg, croppedPlate, status, timeNow)
        elif number != '':
            _save_entry(number, charConfAvg, plateConfAvg, croppedPlate, status, datetime.now())

def _save_entry(number, charConfAvg, plateConfAvg, croppedPlate, status, timeNow):
    """
    Helper function to save entry data.
    """
    display_time = timeNow.strftime("%H:%M:%S")
    display_date = timeNow.strftime("%Y-%m-%d")
    plateImgName = f'temp/{number}-{timeNow.strftime("%H:%M:%S-%Y-%m-%d")}.jpg'
    croppedPlate.save(plateImgName, format='jpg')
    
    enteriesExport = {
        'status': [status],
        'plateNum': [number],
        'time': [display_time],
        'date': [display_date],
        'platePic': plateImgName,
        'charPercent': [charConfAvg],
        'platePercent': [plateConfAvg]
    }
    df = pd.DataFrame(enteriesExport)
    df.to_csv(str(Path().absolute()) + '/base/enteries.csv', 
              header=False, index=False, mode='a', encoding='utf-8')


def dbRefreshTable():
    """
    Refresh the entries table with the most recent 20 records.
    """
    dfReadEnteries = pd.read_csv(str(Path().absolute()) + '/base/enteries.csv')
    return dfReadEnteries.iloc[-20:].sort_index(ascending=False)


def getFieldNames(fieldsList):
    """
    Get display names for database fields.
    """
    return [params.fieldNames[value] for value in fieldsList]


def timeDifference(strTime, strDate):
    """
    Calculate time difference and check if it's more than 1 minute.
    """
    start_time = datetime.strptime(f"{strTime} {strDate}", "%H:%M:%S %Y-%m-%d")
    end_time = datetime.strptime(datetime.now().strftime("%H:%M:%S %Y-%m-%d"), 
                                "%H:%M:%S %Y-%m-%d")
    delta = end_time - start_time
    minutes = (delta.total_seconds() / 60).__ceil__()
    return minutes > 1
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
