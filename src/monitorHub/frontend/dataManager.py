#-----------------------------------------------------------------------------
# Name:        dataManage.py
#
# Purpose:     Data manager class used to provide specific data fetch and process 
#              functions and init the local data storage.
#              
# Author:      Yuancheng Liu 
#
# Version:     v_0.2
# Created:     2023/01/11
# Copyright:   
# License:     
#-----------------------------------------------------------------------------

import json
import datetime
from datetime import datetime
from copy import deepcopy

import frontendGlobal as gv
import Log
import udpCom

# Define all the module local untility functions here:
#-----------------------------------------------------------------------------
def parseIncomeMsg(msg):
    """ parse the income message to tuple with 3 element: request key, type and jsonString
        Args: msg (str): example: 'GET;dataType;{"user":"<username>"}'
    """
    req = msg.decode('UTF-8') if not isinstance(msg, str) else msg
    reqKey = reqType = reqJsonStr= None
    try:
        reqKey, reqType, reqJsonStr = req.split(';', 2)
    except Exception as err:
        Log.error('parseIncomeMsg(): The income message format is incorrect.')
        Log.exception(err)
    return (reqKey.strip(), reqType.strip(), reqJsonStr)


# Define all class here:
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PeerConnector(object):
    """ Peer connector is used to connect to each scheduler and save the connectors
        information. Each peer connector has one UPD connector to communicate with 
        the scheudler.
    """
    def __init__(self, id, uniqName, ipaddress, udpPort):
        self.uniqID = id
        self.uniqName = uniqName
        self.ipaddres = ipaddress
        self.udpPort = udpPort
        self.connector = udpCom.udpClient((self.ipaddres, self.udpPort))
        self.lastUpdateT = None
        self.connReadyFlg = self._loginScheduler()
        self.taskCountDict = {
            'total': 0,
            'finish': 0,
            'running':0,
            'pending': 0,
            'error': 0,
            'deactive': 0
        }
        print("Peer Connector Inited.")

    #-----------------------------------------------------------------------------
    def _fetchTaskCounts(self):
        """ Connect to the peer and fetch the peer's current tasks' count, then update
            taskCountDict."""
        rqstKey = 'GET'
        rqstType = 'taskCount'
        result = self._queryToBE(rqstKey, rqstType, self.taskCountDict)
        if result: self.taskCountDict.update(result)

    #-----------------------------------------------------------------------------
    def _loginScheduler(self):
        """ Try to connect to the scheduler."""
        print("Try to connnect to the scheduler [%s]..." %str(self.ipaddres))
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
            Args:
                rqstKey (str): request key (GET/POST/REP)
                rqstType (_type_): request type string.
                rqstDict (_type_): request detail dictionary.
                dataOnly (bool, optional): flag to indentify whether only return the 
                    data. Defaults to True. return (responseKey, responseType, responseJson) if set
                    to False.
        Returns:
            _type_: refer to <dataOnly> flag's explaination.
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
    def changeTask(self, jobID, action):
        rqstKey = 'POST'
        rqstType = 'changeTsk'
        rqstDict = {
            'taskId': jobID,
            'action': action
        }
        result = self._queryToBE(rqstKey, rqstType, rqstDict)
        if result:
            print("Action Done")
            return True
        return False

    #-----------------------------------------------------------------------------
    def getJobsState(self, jobType):
        """ Connect to schduler peer to get the current task state json.
            Args:
                jobType (str): currently support 4 types: 'all', 'daily', 'random', 'weekly'
        """
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
    def getOwnInfo(self, taskContFlg=True):
        """ Get the connector's info. 
            Args:
                taskContFlg (bool, optional): flag to indentify whether return the task info. 
                Defaults to True.
            Returns:
                json: _description_
        """
        infoDict = {
            'id': self.uniqID,
            'peerName': self.uniqName,
            'ipAddr':   self.ipaddres,
            'updPort':  self.udpPort,
            'connected': self.connReadyFlg
        }
        if taskContFlg:
            self._fetchTaskCounts()
            infoDict.update(self.taskCountDict)
        infoDict['updateT'] = self.lastUpdateT
        return infoDict

    #-----------------------------------------------------------------------------
    def getConnState(self):
        """ Get the connection state."""
        return (self.connReadyFlg, self.lastUpdateT)

    #-----------------------------------------------------------------------------
    def matchInfo(self, ipaddress, udpPort):
        """ Check the input ip:port are same as the peer.
            Args:
                ipaddress (str): _description_
                udpPort (int): _description_
        """
        return (self.ipaddres == ipaddress) and (self.udpPort == udpPort)

    #-----------------------------------------------------------------------------
    def close(self):
        """ close the connector."""
        self.connector.close()
        self.connReadyFlg
        self.connector = None

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class DataManager(object):
    """ The data manager is the module contents all the connectors obj and control 
        all the data display on the web.
    """
    def __init__(self, parent) -> None:
        self.idCount = 0 
        self.schedulerIds = {}  # the id -> name mapping dict.
        self.connectorDict = {} # the connector dict.

#-----------------------------------------------------------------------------
    def addSchedulerPeer(self, peerName, peerIp, peerPort):
        """ Add the scheduler peer in the data manager

            Args:
                peerName (str): scheduler's unique name.
                peerIp (str): ip address
                peerPort (int): udp port
        """
        if peerName in self.connectorDict.keys():
            Log.info("addSchedulerPeer(): The peerName: %s is exist, can not add." %str(peerName))
            return False
        for peerConnector in self.connectorDict.values():
            if peerConnector.matchInfo(peerIp, peerPort): 
                Log.info("addSchedulerPeer(): The <peerIp> and <peerPort> exist." )
                return False
        connector = PeerConnector( self.idCount, peerName, peerIp, peerPort)
        #if connector.getConnState()[0]:
        self.connectorDict[peerName] = connector
        self.schedulerIds[str(self.idCount)] = peerName
        self.idCount += 1
        return True
        #return False

#-----------------------------------------------------------------------------
    def changeTaskState(self, peerName, jobID, action):
        if peerName in self.connectorDict.keys():
            self.connectorDict[peerName].changeTask(jobID, action)

#-----------------------------------------------------------------------------
    def removeSchedulerPeer(self, peerName):
        """ Remove the scheduler based on the input peer name."""
        if peerName in self.connectorDict.keys():
            self.connectorDict[peerName].close()
            self.connectorDict[peerName] = None
            self.connectorDict.pop(peerName)
            return True  
        return False

#-----------------------------------------------------------------------------
    def getOnePeerDetail(self, peerName):
        if peerName in self.connectorDict.keys():
            return self.connectorDict[peerName].getOwnInfo()
        return {}

#-----------------------------------------------------------------------------
    def getPeersInfo(self, NameList=None):
        if NameList is None: NameList = self.connectorDict.keys() 
        return [self.getOnePeerDetail(pName) for pName in NameList] 

#-----------------------------------------------------------------------------
    def getPeerConnInfo(self, peerName):
        #print(self.connectorDict.keys())
        if peerName in self.connectorDict.keys():
            return self.connectorDict[peerName].getConnState()
        return None

#-----------------------------------------------------------------------------
    def getPeerTaskInfo(self, peerName, infoType):
        if peerName in self.connectorDict.keys():
            return self.connectorDict[peerName].getJobsState(infoType)
        return None
            
#-----------------------------------------------------------------------------
    def getPeerName(self, id):
        if str(id) in self.schedulerIds.keys():
            return self.schedulerIds[str(id)]
        return None

# Define all general function and test case here:
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

def buildPeerInfoDict(peerId):
    """ Build the peer all information dictionary based on the input peer ID.
    Args:
        peerId (_type_): _description_

    Returns:
        _type_: _description_
    """
    peerName = gv.iDataMgr.getPeerName(peerId)
    peerInfoDict = {
        "name": peerName,
        "connected" : False,
        "updateT"   : None,
        "daily"     : [],
        "random"    : [],
        "weekly"    : []
    }
    result = gv.iDataMgr.getPeerConnInfo(peerName)
    taskInfoDict = gv.iDataMgr.getPeerTaskInfo(peerName, 'all')
    if result: peerInfoDict['connected'] = result[0]
    if result: peerInfoDict['updateT'] = result[1]
    if taskInfoDict and taskInfoDict['daily']: peerInfoDict['daily'] = taskInfoDict['daily']
    if taskInfoDict and taskInfoDict['random']: peerInfoDict['random'] = taskInfoDict['random']
    if taskInfoDict and taskInfoDict['weekly']: peerInfoDict['weekly'] = taskInfoDict['weekly']
    return peerInfoDict