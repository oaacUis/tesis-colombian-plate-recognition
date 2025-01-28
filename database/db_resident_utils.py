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
from helper.text_decorators import check_similarity_threshold

params = Parameters()

fieldsList = ['fName', 'lName', 'building', 'block', 'num', 'carModel', 'plateNum', 'status']
dbResidents = params.dbResidents


# def insertResident(resident, update=False, editingPlate=''):
#     """Insert or update resident in database"""
#     try:
#         sqlConnect = sqlite3.connect(dbResidents)
#         sqlCursor = sqlConnect.cursor()

#         # Debug prints
#         print(f"Inserting resident data: {vars(resident)}")
#         print(f"Update mode: {update}")
#         print(f"Editing plate: {editingPlate}")

#         if update:
#             pltNum = resident.plateNum
#             updateResidentSQL = """UPDATE residents 
#                                SET fName=:fName, lName=:lName, building=:building,
#                                block=:block, num=:num, carModel=:carModel,
#                                plateNum=:plateNum, status=:status
#                                WHERE plateNum=:editingPlate"""
#             dlist = vars(resident)
#             dlist['editingPlate'] = editingPlate
#             sqlCursor.execute(updateResidentSQL, dlist)
#             print(f"Updated resident with plate: {pltNum}")
#         else:
#             # Insert new resident
#             insert_sql = """INSERT INTO residents 
#                           (fName, lName, building, block, num, carModel, plateNum, status)
#                           VALUES (:fName, :lName, :building, :block, :num, :carModel, :plateNum, :status)"""
#             sqlCursor.execute(insert_sql, vars(resident))
#             print(f"Inserted new resident with plate: {resident.plateNum}")

#         sqlConnect.commit()
#         print("Database transaction committed successfully")
        
#     except sqlite3.Error as error:
#         print(f"SQLite error: {error}")
#         print(f"Failed query params: {vars(resident)}")
#         raise
#     finally:
#         if sqlConnect:
#             sqlConnect.close()

def insertResident(resident, update=False, editingPlate=''):
    """Insert or update resident in database"""
    try:
        sqlConnect = sqlite3.connect(dbResidents)
        sqlCursor = sqlConnect.cursor()

        if update:
            updateResidentSQL = """
                UPDATE residents 
                SET fName=:fName, 
                    lName=:lName, 
                    building=:building,
                    block=:block, 
                    num=:num, 
                    carModel=:carModel,
                    plateNum=:plateNum, 
                    status=:status
                WHERE plateNum=:editingPlate
            """
            params = vars(resident)
            params['editingPlate'] = editingPlate
            sqlCursor.execute(updateResidentSQL, params)
        else:
            # Insert new resident
            insert_sql = """INSERT INTO residents 
                          (fName, lName, building, block, num, carModel, plateNum, status)
                          VALUES (:fName, :lName, :building, :block, :num, :carModel, :plateNum, :status)"""
            sqlCursor.execute(insert_sql, vars(resident))
            #print(f"Inserted new resident with plate: {resident.plateNum}")    
    
        sqlConnect.commit()
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise
    finally:
        sqlConnect.close()

def getResidentByName(conn, cur, lastname):
    """
    Retrieve resident information by last name.
    """
    cur.execute("SELECT * FROM residents WHERE last=:last", {'last': lastname})
    return cur.fetchall()


def updateResident(conn, cur, resident, pay):
    """
    Update resident payment information.
    """
    with conn:
        cur.execute("""UPDATE residents SET pay=:pay
                    WHERE first=:first AND last=:last""",
                    {'first': resident.first, 'last': resident.last, 'pay': pay})


def dbRemoveResident(plateNumber):
    """
    Remove a resident from the database by plate number.
    """
    sqlConnect = sqlite3.connect(dbResidents)
    sqlCursor = sqlConnect.cursor()
    removeResidentSQL = f"""DELETE FROM residents WHERE plateNum='{plateNumber}'"""
    sqlCursor.execute(removeResidentSQL)
    sqlConnect.commit()
    sqlConnect.close()


def dbGetPlateExist(plateNumber):
    """
    Check if a plate number exists in the database.
    """
    sqlConnect = sqlite3.connect(dbResidents)
    sqlCursor = sqlConnect.cursor()
    PlateExistSQL = f"""SELECT status FROM residents WHERE plateNum='{plateNumber}'"""
    PlateExist = sqlCursor.execute(PlateExistSQL).fetchone()
    sqlConnect.commit()
    sqlConnect.close()
    return PlateExist is not None


def db_get_plate_status(plateNumber):
    """
    Get the status of a plate number.
    Returns 2 if plate not found (Unregistered).
    """
    sqlConnect = sqlite3.connect(dbResidents)
    sqlCursor = sqlConnect.cursor()
    PlateStatusSQL = f"""SELECT status FROM residents WHERE plateNum='{plateNumber}'"""
    PlateStatus = sqlCursor.execute(PlateStatusSQL).fetchone()
    sqlConnect.commit()
    sqlConnect.close()
    return PlateStatus[0] if PlateStatus is not None else 2


def db_get_plate_owner_name(plateNumber):
    """
    Get the owner's full name by plate number.
    """
    sqlConnect = sqlite3.connect(dbResidents)
    sqlCursor = sqlConnect.cursor()
    OwnerNameSQL = f"""SELECT fName, lName FROM residents WHERE plateNum='{plateNumber}'"""
    OwnerName = sqlCursor.execute(OwnerNameSQL).fetchone()
    sqlConnect.commit()
    sqlConnect.close()
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
        return Resident(**FullData)
    return None


def dbGetResidentDatasBylName(lName):
    """
    Get resident information by last name.
    """
    sqlConnect = sqlite3.connect(dbResidents)
    sqlCursor = sqlConnect.cursor()
    FullResidentSQL = f"""SELECT * FROM residents WHERE lName LIKE '%{lName}%'"""
    FullResident = sqlCursor.execute(FullResidentSQL).fetchall()
    
    if FullResident:
        FullData = dict(zip([c[0] for c in sqlCursor.description], FullResident[0]))
        sqlConnect.commit()
        sqlConnect.close()
        return Resident(**FullData)
    return None


def dbGetAllResidents(limit=100, orderBy='lName', orderType='ASC', whereLike=''):
    """
    Get all residents with filtering and ordering options.
    """
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