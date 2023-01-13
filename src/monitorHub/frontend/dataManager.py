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

import frontendGlobal as gv
import Log
import udpCom

#-----------------------------------------------------------------------------
def parseIncomeMsg(msg):
    req = msg.decode('UTF-8')
    reqKey = reqType = reqJsonStr= None
    try:
        reqKey, reqType, reqJsonStr = req.split(';', 2)
    except Exception as e:
        Log.error('The income message format is incorrect.')
        Log.exception(e)
    return (reqKey.strip(), reqType.strip(), reqJsonStr)

#-----------------------------------------------------------------------------
class DataManager(object):

    def __init__(self, parent) -> None:
        self.connector = udpCom.udpClient(gv.BE_IP)
        gv.iConnector = self.connector
        self.connReadyFlg = False

    def schedulerConnected(self):
        return self.connReadyFlg

#-----------------------------------------------------------------------------
    def connectToScheduler(self):
        try:
            print("Try to connnect to the scheduler...")
            rqstKey = 'GET'
            rqstType = 'login'
            rqstDict = {'user': 'Bob'}
            result = self._queryToBE(rqstKey, rqstType, rqstDict)
            print("Scheduler online, state: ready")
            self.connReadyFlg = True
        except Exception as err:
            print("Connection timeout: %s" %str(err))
            self.connReadyFlg = False
        
#-----------------------------------------------------------------------------
    def getJobsState(self):
        rqstKey = 'GET'
        rqstType = 'jobState'
        rqstDict = {'filter': 'All'}

        result = self._queryToBE(rqstKey, rqstType, rqstDict)
        print(result)
        return result

#-----------------------------------------------------------------------------
    def _queryToBE(self, rqstKey, rqstType, rqstDict, dataOnly=True):
        k = t = result = None
        if rqstKey and rqstType and rqstDict:
            rqst = ';'.join((rqstKey, rqstType, json.dumps(rqstDict)))
            if gv.iConnector:
                resp = gv.iConnector.sendMsg(rqst, resp=True)
                k, t, data = parseIncomeMsg(resp)
                if k != 'REP': print('The msg reply key %s is invalid' % k)
                if t != rqstType: print('The reply type doesnt match.%s' %str((rqstType, t)))
                try:
                    result = json.loads(data)
                except Exception as err:
                    Log.exception('Exception: %s' %str(err))
                if dataOnly: return result
        else:
            Log.error("queryBE: input missing: %s" %str(rqstKey, rqstType, rqstDict))
        return (k, t, result)