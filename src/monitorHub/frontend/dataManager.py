#-----------------------------------------------------------------------------
# Name:        dataManage.py
#
# Purpose:     Monitor Hub data manager class used to provide specific data fetch 
#              and process functions and init the local data storage to store
#              the tasks state of 
#              
# Author:      Yuancheng Liu 
#
# Version:     v_0.2.3
# Created:     2023/01/11
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

import json
import datetime
from datetime import datetime

import cueHubGlobal as gv
import Log
import udpCom

# Define all the module local untility functions here:
#-----------------------------------------------------------------------------
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
        return('', '', json.dumps({}))

#-----------------------------------------------------------------------------
def buildPeerInfoDict(peerId):
    """ Build the peer all information dictionary based on the input peer ID.
        Args:
            peerId (int): scheduler id.
        Returns:
            _type_: scheduler all information dictionary.
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


# Define all class here:
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PeerConnector(object):
    """ Peer connector is used to connect to each scheduler and save the connection
        information. Each peer connector has one UDP connector to communicate with 
        the scheudler.
    """
    def __init__(self, id, uniqName, ipaddress, udpPort):
        """ init example: connector = PeerConnector( 1, 'scheduler1', '192.168.1.100', 5000)
            Args:
                id (int): unqiue ID map to the connected scheduler. 
                uniqName (str): connected scheduler name.
                ipaddress (str): scheduler IP address.
                udpPort (int): scheduler UDP port.
        """
        self.uniqID = id
        self.uniqName = uniqName
        self.ipaddres = ipaddress
        self.udpPort = udpPort
        self.connector = udpCom.udpClient((self.ipaddres, self.udpPort))
        self.lastUpdateT = None
        self.connReadyFlg = self._loginScheduler()
        self.taskCountDict = {
            'total':    0,
            'finish':   0,
            'running':  0,
            'pending':  0,
            'error':    0,
            'deactive': 0
        }
        gv.gDebugPrint("Peer Connector [%s]Inited." %str(uniqName), logType=gv.LOG_INFO)

    #-----------------------------------------------------------------------------
    def _fetchTaskCounts(self):
        """ Connect to the peer and fetch the peer's current tasks' count detail, 
            then update taskCountDict."""
        rqstKey = 'GET'
        rqstType = 'taskCount'
        result = self._queryToBE(rqstKey, rqstType, self.taskCountDict)
        if result: self.taskCountDict.update(result)

    #-----------------------------------------------------------------------------
    def _loginScheduler(self):
        """ Try to connect / login to the scheduler."""
        gv.gDebugPrint("Try to connnect to the scheduler [%s]..." %str(self.ipaddres), 
                       logType=gv.LOG_INFO)
        rqstKey = 'GET'
        rqstType = 'login'
        rqstDict = {'user': self.uniqName}
        result = self._queryToBE(rqstKey, rqstType, rqstDict)
        if result:
            gv.gDebugPrint("Scheduler online, state: ready", logType=gv.LOG_INFO)
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
                    if k != 'REP': gv.gDebugPrint('The msg reply key %s is invalid' % k, logType=gv.LOG_WARN)
                    if t != rqstType: gv.gDebugPrint('The reply type doesnt match.%s' %str((rqstType, t)), logType=gv.LOG_WARN)
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
        """ Control the task state.
            Args:
                jobID (int): job id
                action (str): task change action.

            Returns:
                _type_: _description_
        """
        rqstKey = 'POST'
        rqstType = 'changeTsk'
        rqstDict = {
            'taskId': jobID,
            'action': action
        }
        result = self._queryToBE(rqstKey, rqstType, rqstDict)
        if result:
            gv.gDebugPrint("Action Done")
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
            gv.gDebugPrint("getDailyJobsState(): the input jobType is not valid: %s" %str(jobType), logType=gv.LOG_WARN)
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
        self.schedulerDetailDict = {}   # dictionary to store the schduler's detail information.

#-----------------------------------------------------------------------------
    def addSchedulerPeer(self, peerName, peerIp, peerPort, linkMode=0):
        """ Add the scheduler peer in the data manager
            Args:
                peerName (str): scheduler's unique name.
                peerIp (str): ip address
                peerPort (int): udp port
                linkMode (int): the scheduler communication mode. 0-fetch, 1-reprot, 2-mix
        """
        if peerName in self.connectorDict.keys():
            Log.info("addSchedulerPeer(): The peerName: %s is exist, can not add." %str(peerName))
            return False
        for peerConnector in self.connectorDict.values():
            if peerConnector.matchInfo(peerIp, peerPort): 
                Log.info("addSchedulerPeer(): The <peerIp> and <peerPort> exist." )
                return False
        connector = PeerConnector(self.idCount, peerName, peerIp, peerPort)
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