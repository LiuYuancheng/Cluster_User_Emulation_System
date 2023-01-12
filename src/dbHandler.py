
import sqlite3
from datetime import datetime, timedelta

import actionGlobal as gv

mode = 0
connection = sqlite3.connect(gv.DB_PATH)

if mode == 0:
    print("Clean and reset the data jobs table.")
    with open(gv.SQL_PATH) as fh:
        connection.executescript(fh.read())
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
connection.commit()
connection.close()