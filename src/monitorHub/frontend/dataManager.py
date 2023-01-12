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



def parseIncomeMsg(msg):
    req = msg.decode('UTF-8')
    reqKey = reqType = reqJsonStr= None
    try:
        reqKey, reqType, reqJsonStr = req.split(';', 2)
    except Exception as e:
        Log.error('The income message format is incorrect.')
        Log.exception(e)
    return (reqKey.strip(), reqType.strip(), reqJsonStr)

class DataManager(object):

    def __init__(self, parent) -> None:
        self.connector = udpCom.udpClient(gv.BE_IP)

    
    def getJobsState(self):
        resp = self.connector.sendMsg('GET;state;{}', resp=True)
        k, t, data = parseIncomeMsg(resp)
        result = json.loads(data)
        return result