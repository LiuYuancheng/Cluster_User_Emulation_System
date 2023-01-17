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
import json
import datetime
from datetime import datetime, timedelta
import threading
import sqlite3

import actionGlobal as gv
import Log
import udpCom

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class DataManager(threading.Thread):

    def __init__(self, parent) -> None:
        threading.Thread.__init__(self)
        self.dbConn = None
        self.parent = parent
        self.server = udpCom.udpServer(None, gv.UDP_PORT)
        self.terminate = False
        self.lastUpdate = datetime.now()

    #-----------------------------------------------------------------------------
    def run(self):
        """ Thread run() function call by start(). """
        time.sleep(1)  
        #while not self.terminate:
        self.server.serverStart(handler=self.msgHandler)
        #print('Do the daily database backup and update')
        Log.info('Do the daily database backup and update')
            
#-----------------------------------------------------------------------------
    def parseIncomeMsg(self, msg):
        req = msg.decode('UTF-8')
        reqKey = reqType = reqJsonStr= None
        try:
            reqKey, reqType, reqJsonStr = req.split(';', 2)
        except Exception as e:
            Log.error('The income message format is incorrect.')
            Log.exception(e)
        return (reqKey.strip(), reqType.strip(), reqJsonStr)

#-----------------------------------------------------------------------------
    def msgHandler(self, msg):
        print("Incomming message: %s" % str(msg))

        # request message format: 
        # data fetch: GET:<key>:<val1>:<val2>...
        # data set: POST:<key>:<val1>:<val2>...

        resp = b'REP:deny:{}'
        (reqKey, reqType, reqJsonStr) = self.parseIncomeMsg(msg)
        if reqKey=='GET':

            if reqType == 'login':
                resp = ';'.join(('REP', 'login', json.dumps({'state':'ready'})))
            elif reqType == 'jobState':
                respStr = self.fetchAllActState()
                resp =';'.join(('REP', 'jobState', respStr))
        if isinstance(resp, str): resp = resp.encode('utf-8')
        return resp

    #-----------------------------------------------------------------------------
    def _getDBconnection(self):
        conn = sqlite3.connect(gv.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    #-----------------------------------------------------------------------------
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
            actDesc = actDict['actDesc'] if 'actDesc' in actDict.keys() else ''
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

    #-----------------------------------------------------------------------------
    def updateActStat(self, actId, actState):
        conn = self._getDBconnection()
        check = conn.execute("SELECT 1 FROM dailyActions WHERE actId=%s" %str(actId))
        if check.fetchone():
            queryStr = "UPDATE dailyActions SET actState = '%s' WHERE actId = %s " %(actState, str(actId))
            conn.execute(queryStr)
            conn.commit()
        conn.close()

    #-----------------------------------------------------------------------------
    def fetchAllActState(self):
        respDict = {
            'daily': None,
            'random': [],
            'weekly':[]
        }
        conn = self._getDBconnection()
        queryStr = 'SELECT * FROM dailyActions'
        resp = conn.execute(queryStr).fetchall()
        respDict['daily'] = [dict(row) for row in resp]

        conn.close()
        respStr = json.dumps(respDict)
        print(len(respStr))
        return respStr


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
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

        dbmgr.fetchAllActState()


if __name__ == "__main__":
    testCase(0)
