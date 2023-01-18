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
from datetime import datetime
from copy import deepcopy
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
class PeerConnector(object):

    def __init__(self, uniqName, ipaddress, udpPort):
        self.uniqName = uniqName
        self.idaddress = ipaddress
        self.udpPort = udpPort
        self.connector = udpCom.udpClient((self.idaddress, self.udpPort))
        self.lastUpdateT = None
        self.connReadyFlg = self._loginScheduler()

    #-----------------------------------------------------------------------------
    def _loginScheduler(self):
       
        print("Try to connnect to the scheduler...")
        rqstKey = 'GET'
        rqstType = 'login'
        rqstDict = {'user': self.uniqName}
        result = self._queryToBE(rqstKey, rqstType, rqstDict)
        if result:
            print("Scheduler online, state: ready")
            return True
        return False

    #-----------------------------------------------------------------------------
    def _queryToBE(self, rqstKey, rqstType, rqstDict, dataOnly=True):
        """ Query message to back end to get data.
        """
        k = t = result = None
        if rqstKey and rqstType and rqstDict:
            rqst = ';'.join((rqstKey, rqstType, json.dumps(rqstDict)))
            if self.connector:
                resp = self.connector.sendMsg(rqst, resp=True)
                if resp:
                    k, t, data = parseIncomeMsg(resp)
                    if k != 'REP': print('The msg reply key %s is invalid' % k)
                    if t != rqstType: print('The reply type doesnt match.%s' %str((rqstType, t)))
                    try:
                        result = json.loads(data)
                        self.lastUpdateT = datetime.now()
                    except Exception as err:
                        Log.exception('Exception: %s' %str(err))
                        return None
                else:
                    return None
                if dataOnly: return result
        else:
            Log.error("queryBE: input missing: %s" %str(rqstKey, rqstType, rqstDict))
        return (k, t, result)

    #-----------------------------------------------------------------------------
    def getJobsState(self, jobType):
        if jobType in ('all', 'daily', 'random', 'weekly'):
            rqstKey = 'GET'
            rqstType = 'jobState'
            rqstDict = {'filter': jobType}
            result = self._queryToBE(rqstKey, rqstType, rqstDict)
            return result
        else:
            print("getDailyJobsState(): the input jobType is not valid: %s" %str(jobType))
            return None

    #-----------------------------------------------------------------------------
    def getConnState(self):
        """ Get the connection state."""
        return (self.connReadyFlg, self.lastUpdateT)

    #-----------------------------------------------------------------------------
    def matchInfo(self, ipaddress, udpPort):
        return (self.idaddress == ipaddress) and (self.udpPort == udpPort)

    #-----------------------------------------------------------------------------
    def close(self):
        self.connector.close()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class DataManager(object):

    def __init__(self, parent) -> None:
        self.connectorDict = {} # the connector dict.

#-----------------------------------------------------------------------------
    def addSchedulerPeer(self, peerName, peerIp, peerPort):
        """ Add the scheduler peer in the data manager

        Args:
            peerName (_type_): _description_
            peerIp (_type_): _description_
            peerPort (_type_): _description_
        """
        if peerName in self.connectorDict.keys():
            Log.info("addSchedulerPeer(): The peerName: %s is exist, can not add." %str(peerName))
            return False
        for peerConnector in self.connectorDict.values():
            if peerConnector.matchInfo(peerIp, peerPort): 
                Log.info("addSchedulerPeer(): The <peerIp> and <peerPort> exist." )
                return False
        connector = PeerConnector(peerName, peerIp, peerPort)
        if connector.getConnState()[0]:
            self.connectorDict[peerName] = connector
            return True
        return False

#----------------------------------------------  -------------------------------
    def removeSchedulerPeer(self, peerName):
        if peerName in self.connectorDict.keys():
            self.connectorDict[peerName].close()
            self.connectorDict[peerName] = None
            self.connectorDict.pop(peerName)
            return True  
        return False

#-----------------------------------------------------------------------------
    def getPeerConnInfo(self, peerName):
        print(self.connectorDict.keys()     )
        if peerName in self.connectorDict.keys():
            return self.connectorDict[peerName].getConnState()
            print(data)
        return None


#-----------------------------------------------------------------------------
    def getPeerTaskInfo(self, peerName, infoType):
        if peerName in self.connectorDict.keys():
            return self.connectorDict[peerName].getJobsState(infoType)
        return None
            