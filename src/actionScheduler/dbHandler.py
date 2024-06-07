#-----------------------------------------------------------------------------
# Name:        dbBaseHandler.py
#
# Purpose:     This program is used to reset the dataBase and test the querys.
#              
# Author:      Yuancheng Liu 
#
# Version:     v_0.2
# Created:     2023/01/11
# Copyright:   Copyright (c) 2023 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

import sqlite3
from datetime import datetime, timedelta

from actionGlobal import DB_PATH, SQL_PATH

connection = sqlite3.connect(DB_PATH)

def resetDB():
    print("Clean and reset all the tables.")
    with open(SQL_PATH) as fh:
        connection.executescript(fh.read())
    
def testCase(mode):

    if mode == 0:
        resetDB()
    elif mode == 1:
        print("Reset DB and test insert data")
        resetDB()
        cur = connection.cursor()
        actId = 1
        actName = '09:01_ping'
        actDetail = 'Ping 30 destinations'
        actDesc = ''
        actOwner = ''
        actType = 1
        startT = '09:01:00'
        depend = 0
        threadType = 1
        actState = 'pending'
        tomorrow = datetime.now() + timedelta(1)
        nextT =  tomorrow.strftime('%Y-%m-%d') + ' ' + startT
        
        cur.execute('INSERT INTO dailyActions \
            (actId, actName, actDetail, actDesc, actOwner, actType, startT, depend, threadType, actState, nextT)\
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (actId, actName, actDetail, actDesc, actOwner, actType, startT, depend, threadType, actState, nextT))
    else:
        pass
        # Add your test code here and change the mode part to active it.
    connection.commit()
    connection.close()

if __name__ == '__main__':
    mode = int(input("Input the function mode: 0 for reset DB, 1 for test insert data:"))
    testCase(mode)
