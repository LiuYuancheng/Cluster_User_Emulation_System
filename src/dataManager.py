#-----------------------------------------------------------------------------
# Name:        dataManage.py
#
# Purpose:     Data manager class to store the specific functions and init the 
#              data class.
#              
# Author:      Yuancheng Liu 
#
# Version:     v_0.1
# Created:     2023/01/11
# Copyright:   
# License:     
#-----------------------------------------------------------------------------

import time
import datetime
from datetime import datetime, timedelta
import threading
import sqlite3

import actionGlobal as gv

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class DataManager(threading.Thread):

    def __init__(self, parent) -> None:
        threading.Thread.__init__(self)
        self.dbConn = None
        self.parent = parent
        self.terminate = False
        self.lastUpdate = datetime.now()

    #-----------------------------------------------------------------------------
    def run(self):
        """ Thread run() function call by start(). """
        time.sleep(1)  
        while not self.terminate:
            print('Do the daily database backup and update')
            Log.info('Do the daily database backup and update')
            self._checkGpuRequest()
            time.sleep(gv.ONE_HOUR)

    def _getDBconnection(self):
        conn = sqlite3.connect(gv.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def registerActions(self, actDict):
        
        conn = self._getDBconnection()
        actId = actDict['actId']

        check = conn.execute("SELECT 1 FROM dailyActions WHERE actId=%s" %str(actId))
        if check.fetchone():
            print("The action task is registered")
        else:
            actId = actDict['actId']
            actName = actDict['actName']
            actDetail = actDict['actDetail']
            actDesc = actDict['actDetail'] if 'actDetail' in actDict.keys() else ''
            actOwner = actDict['actOwner'] if 'actOwner' in actDict.keys() else ''
            actType = actDict['actType']
            startT = actDict['startT']
            depend = actDict['depend'] if 'depend' in actDict.keys() else 0
            threadType = actDict['threadType']
            actState = actDict['actState']
            tomorrow = datetime.now() + timedelta(1)
            nextT =  tomorrow.strftime('%Y-%m-%d') + ' ' + startT
            
            conn.execute('INSERT INTO dailyActions \
                (actId, actName, actDetail, actDesc, actOwner, actType, startT, depend, threadType, actState, nextT)\
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (actId, actName, actDetail, actDesc, actOwner, actType, startT, depend, threadType, actState, nextT))
            
            # comit the insert.
            conn.commit()

        conn.close()

    def updateActStat(self, actId, actState):
        conn = self._getDBconnection()
        check = conn.execute("SELECT 1 FROM dailyActions WHERE actId=%s" %str(actId))
        if check.fetchone():
            queryStr = "UPDATE dailyActions SET actState = '%s' WHERE actId = %s " %(actState, str(actId))
            conn.execute(queryStr)
            conn.commit()
        conn.close()


def testCase(mode):

    if mode == 0:
        dbmgr = DataManager(None)
        testDict = {
            'actId' : 2,
            'actName': '09:10_ping [MT]',
            'actDetail': 'Ping 100+ destinations',
            'actDesc': 'Bob runs the ping client program',
            'actOwner': 'Bob',
            'actType': 1,
            'startT' : '09:10:00',
            'depend' :0,
            'threadType':1,
            'actState': 'pending'
        }
        dbmgr.registerActions(testDict)


if __name__ == "__main__":
    testCase(0)
