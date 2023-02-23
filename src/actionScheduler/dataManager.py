#-----------------------------------------------------------------------------
# Name:        dataManage.py
#
# Purpose:     Data manager class used to provide specific data fetch and process 
#              functions and init the local data storage/DB. This manager is used 
#              by the scheduler(<actionScheduler>) obj.
#              
# Author:      Yuancheng Liu 
#
# Version:     v_0.2
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

# Define all the local untility functions here:
#-----------------------------------------------------------------------------
def parseIncomeMsg(msg):
    """ parse the income message to tuple with 3 elements: request key, type and jsonString
        Args: msg (str): example: 'GET;dataType;{"user":"<username>"}'
    """
    req = msg.decode('UTF-8') if not isinstance(msg, str) else msg
    try:
        reqKey, reqType, reqJsonStr = req.split(';', 2)
        return (reqKey.strip(), reqType.strip(), reqJsonStr)
    except Exception as err:
        Log.error('parseIncomeMsg(): The income message format is incorrect.')
        Log.exception(err)
        return('','',json.dumps({}))

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class DataManager(threading.Thread):
    """ The data manager is a module running parallel with the main thread to 
        handle the data-IO with dataBase and the monitor hub's data fetching/
        changing request.
    """
    def __init__(self, parent) -> None:
        threading.Thread.__init__(self)
        self.parent = parent
        self.terminate = False
        self.server = udpCom.udpServer(None, gv.UDP_PORT)
        self.lastUpdate = datetime.now()

    #-----------------------------------------------------------------------------
    def run(self):
        """ Thread run() function will be called by start(). """
        time.sleep(1)
        self.server.serverStart(handler=self.msgHandler)
        gv.gDebugPrint("DataManager running finished.", logType=gv.LOG_INFO)

    # define all the private function here:
    #-----------------------------------------------------------------------------
    def _getDBconnection(self):
        """ Connect to the database """
        conn = sqlite3.connect(gv.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    #-----------------------------------------------------------------------------
    def _deleteTask(self, taskID):
        """ Cancel the task in the scheduler and remove the task record from the DB 
            based on the input task id(unique)
            Args:
                taskID (int): task ID in DB
            Returns:
                _type_: _description_
        """
        # delete from the scheduler: 
        if gv.iScheduler and gv.iScheduler.removeAction(taskID):
            conn = self._getDBconnection()
            queryStr = "SELECT actId FROM dailyActions WHERE actId =%s " %(taskID)
            result = conn.execute(queryStr).fetchone()
            conn.commit()
            if result is None: return None
            # delete the action from daily-action table. 
            queryStr =  "DELETE FROM dailyActions WHERE actId =%s " %(taskID)
            conn.execute(queryStr)
            conn.commit()
            conn.close()
            return True
        return False

    #-----------------------------------------------------------------------------
    def changeTask(self, reqJsonStr):
        """ Change the scheduler's task state.
            Args:
                reqJsonStr (_type_): _description_
            Returns:
                _type_: _description_
        """
        reqDict = json.loads(reqJsonStr)
        respDict = {
            'taskId': reqDict['taskId'],
            'action': reqDict['action'],
        }
        if reqDict['action'] == 'delete':
            result = self._deleteTask(reqDict['taskId'])
            print(result)
        else:
            pass
        respStr = json.dumps(respDict)
        return respStr

    #-----------------------------------------------------------------------------
    def fetchAllActState(self):
        respDict = {
            'daily': None,
            'random': [],
            'weekly':[]
        }
        conn = self._getDBconnection()
        # fetch the daily action 
        queryStr = 'SELECT * FROM dailyActions'
        resp = conn.execute(queryStr).fetchall()
        respDict['daily'] = [dict(row) for row in resp]
        # fetch the random action
        queryStr = 'SELECT * FROM randomActions'
        resp = conn.execute(queryStr).fetchall()
        respDict['random'] = [dict(row) for row in resp]
        # fetch the weekly action
        queryStr = 'SELECT * FROM weeklyActions'
        resp = conn.execute(queryStr).fetchall()
        respDict['weekly'] = [dict(row) for row in resp]

        conn.close()
        respStr = json.dumps(respDict)
        #print(len(respStr))
        return respStr

    #-----------------------------------------------------------------------------
    def fetchCrtActCount(self, reqJsonStr):
        """ fetch the current requests count.
            Args:
                reqJsonStr (_type_): _description_
        """
        reqDict = json.loads(reqJsonStr)
        respDict = {'total': 0,
                    'finish': 0,
                    'running': 0,
                    'pending': 0,
                    'error': 0,
                    'deactive': 0
                    }

        conn = self._getDBconnection()
        queryStr = 'SELECT actState, count(*) FROM dailyActions GROUP BY actState'
        resp = conn.execute(queryStr).fetchall()
        if resp:
            resp = dict(resp)
            respDict.update(resp)
            totalNum = sum(resp.values())
            respDict['total'] = totalNum
        conn.close()
        respStr = json.dumps(respDict)
        #print(len(respStr))
        return respStr

    #-----------------------------------------------------------------------------
    def msgHandler(self, msg):
        """ Function to handle the data-fetch/control request from the monitor-hub.
            Args:
                msg (str/bytes): _description_
            Returns:
                bytes: message bytes reply to the monitor hub side.
        """
        gv.gDebugPrint("Incomming message: %s" % str(msg), logType=gv.LOG_INFO)
        # request message format: 
        # data fetch: GET:<key>:<val1>:<val2>...
        # data set: POST:<key>:<val1>:<val2>...
        resp = b'REP:deny:{}'
        (reqKey, reqType, reqJsonStr) = parseIncomeMsg(msg)
        if reqKey=='GET':
            if reqType == 'login':
                resp = ';'.join(('REP', 'login', json.dumps({'state':'ready'})))
            elif reqType == 'jobState':
                respStr = self.fetchAllActState()
                resp =';'.join(('REP', 'jobState', respStr))
            elif reqType == 'taskCount':
                respStr = self.fetchCrtActCount(reqJsonStr)
                resp =';'.join(('REP', 'taskCount', respStr))
        elif reqKey=='POST':
            if reqType == 'changeTsk':
                respStr = self.changeTask(reqJsonStr)
                resp =';'.join(('REP', 'changeTsk', respStr))
            pass
            # TODO: Handle all the control request here.
        if isinstance(resp, str): resp = resp.encode('utf-8')
        return resp

    #-----------------------------------------------------------------------------
    def registerActions(self, actDict, jobType=gv.JB_TP_DAILY):
        """ Added the action in database.
            input <actDict> example:
            regInfoDict = {
                'actId': actionObj.id,
                'actName': actionObj.name,
                'actDetail': actionObj.getActionInfo('actDetail'),
                'actDesc': actionObj.getActionInfo('actDesc'),
                'actOwner': actionObj.getActionInfo('actOwner'),
                'actType': actionObj.jobType,
                'startT': actionObj.timeStr,
                'depend': actionObj.getActionInfo('depend'),
                'threadType': 1 if actionObj.threadFlg else 0,
                'actState': actionObj.state
            }
        
        """
        conn = self._getDBconnection()
        actId = actDict['actId']
        tableList = ('dailyActions', 'randomActions', 'weeklyActions')
        queryStr = "SELECT 1 FROM %s WHERE actId=%s" %(tableList[jobType], str(actId))
        check = conn.execute(queryStr)
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
            queryStr = 'INSERT INTO %s \
                (actId, actName, actDetail, actDesc, actOwner, actType, startT, depend, threadType, actState, nextT)\
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)' %str(tableList[jobType])

            conn.execute(queryStr,(actId, actName, actDetail, actDesc, actOwner, actType, startT, depend, threadType, actState, nextT))
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
#-----------------------------------------------------------------------------
def testCase(mode):
    dbmgr = DataManager(None)
    if mode == 0:
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
    elif mode == 2:
        dbmgr.fetchCrtActCount(json.dumps({}))
    elif mode == 3:
        rqstDict = {
            'taskId': 1,
            'action': 'delete'
        
        }
        dbmgr.changeTask(json.dumps(rqstDict))

#-----------------------------------------------------------------------------
if __name__ == "__main__":
    testCase(3)
