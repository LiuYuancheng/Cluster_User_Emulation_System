#-----------------------------------------------------------------------------
# Name:        localServiceProber.py
#
# Purpose:     This module is a untility module of the lib <python- psutil> to 
#              provide some extend function. 
#              psutil doc link: https://psutil.readthedocs.io/en/latest/#system-related-functions
#
# Author:      Yuancheng Liu
#
# Version:     v_0.1.1
# Created:     2023/03/14
# Copyright:   Copyright (c) 2023 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

import os 
import time
import psutil

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class Prober(object):
    """ A simple object with a private debugPrint function. the probe lib function 
        will be inheritance of it.
    """
    def __init__(self, debugLogger=None) -> None:
        self._debugLogger = debugLogger
        self._logInfo = 0
        self._logWarning = 1
        self._logError = 2
        self._logException =3 

    def _debugPrint(self, msg, prt=True, logType=None):
        if prt: print(msg)
        if not self._debugLogger: return 
        if logType == self._logWarning:
            self._debugLogger.warning(msg)
        elif logType == self._logError:
            self._debugLogger.error(msg)
        elif logType == self._logException:
            self._debugLogger.exception(msg)
        elif logType == self._logInfo:
            self._debugLogger.info(msg)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class localServiceProber(Prober):

    def __init__(self, id, debugLogger=None) -> None:
        """ Init the obj, example: driver = networkServiceProber(debugLogger=Log)"""
        super().__init__(debugLogger=debugLogger)
        self.id = id
        self.resultDict = {}
        self._initResultDict()
        
    def _initResultDict(self):
        self.resultDict = {'target': ':'.join(('local', str(self.id))),
                           'time': time.time()}

#-----------------------------------------------------------------------------
    def getLastResult(self):
        return self.resultDict

#-----------------------------------------------------------------------------
    def getResUsage(self, configDict=None):
        """ Get the cpu, ram, login user, disk and network connction state
            Args:
                configDict (dict, optional): result config dictionary, example:
                configDict = {
                    'cpu': {'interval': 0.1, 'percpu': False},
                    'ram': 0,
                    'user': None,
                    'disk': ['C:'],
                    'network': {'connCount': 0}
                } .Defaults to None.

        Returns:
            dict() : The usage dict, example:
            resultDict = {
                'cpu': <total percent or percent list>,
                'ram': %,
                'user': user list,
                'dist': {'C:' %}
                'network': {'connCount': int }
            }
        """
        resultDict ={}
        if configDict is None: 
            configDict = {
                'cpu': {'interval': 0.1, 'percpu': False},
                'ram': 0,
                'user': None,
                'disk': [],
                'network': {'connCount': 0}
            }
        # Check CPU:
        if 'cpu' in configDict.keys():
            interval = configDict['cpu']['interval'] if 'interval' in configDict['cpu'].keys() else None
            percpuFlg = configDict['cpu']['percpu'] if 'percpu' in configDict['cpu'].keys() else False
            resultDict['cpu'] = psutil.cpu_percent(interval=interval, percpu=percpuFlg)
        
        # Check Mem usage percent
        if 'ram' in configDict.keys():
            data = psutil.virtual_memory()
            resultDict['ram'] = data.percent

        # Check current user
        if 'user' in configDict.keys():
            resultDict['user'] = [str(user.name) for user in psutil.users()]

        # Check disk
        if 'disk' in configDict.keys():
            resultDict['disk'] = {} 
            for diskTag in configDict['disk']:
                resultDict['disk'][diskTag] = psutil.disk_usage(diskTag).percent if os.path.exists(diskTag) else 0
        
        # Check network conntion
        if 'network' in configDict.keys():
            resultDict['network'] = {} 
            resultDict['network']['connCount'] = len(psutil.net_connections())

        return resultDict

#-----------------------------------------------------------------------------
    def getProcessState(self, configDict=None):
        """ Get the total process number and spec process detail (name, id , users) 
            Args:
                configDict (dict, optional): 
                 configDict = {
                    'process': {
                        'count': 0,
                        'filter': ['python.exe']
                    }
                } . Defaults to None.

            Returns:
                dict() : _description_
        """
        resultDict = {'process': {}}
        if configDict is None:
            configDict = {
                'process': {
                    'count': 0,
                    'filter': []
                }
            }
        if 'process' in configDict.keys():
            # Check total process 
            if 'count' in configDict['process'].keys():
                resultDict['process']['count'] = len(psutil.pids())
            # Check the filtered process we want to check
            if 'filter' in configDict['process'].keys():
                filterDict = {}
                for key in configDict['process']['filter']:
                    filterDict[str(key).lower()] = []
                for proc in psutil.process_iter(['pid', 'name', 'username']):
                    infoName = proc.info['name']
                    if str(infoName).lower() in filterDict.keys():
                         filterDict[str(infoName).lower()].append(proc.info)
                resultDict['process']['filter'] = filterDict

        return resultDict
    
#-----------------------------------------------------------------------------
    def getDirFiles(self, configDict=None):
        """ Get the folder contents.
            Args:
                configDict (_type_, optional): _description_. Defaults to None.

            Returns:
                _type_: _description_
        """
        resultDict ={'dir':{}}
        if configDict is None: 
            configDict = {
                'dir': []
            }
        if 'dir' in configDict.keys():
            for dirPath in configDict['dir']:
                dirPath = r'{}'.format(dirPath)
                try:
                    resultDict['dir'][dirPath] = None
                    if os.path.exists(dirPath): resultDict['dir'][dirPath] = os.listdir(dirPath)
                except Exception as err:
                    self._debugPrint("Error to ls dir [%s] : %s" %(dirPath, err), logType=self._logException)
        return resultDict

#-----------------------------------------------------------------------------
    def resetResult(self):
        for key in self.resultDict.keys():
            if key == 'target' or key == 'time': continue
            self.resultDict[key] = None

#-----------------------------------------------------------------------------
    def updateResUsage(self, configDict=None):
        self.resultDict['time'] = time.time()
        self.resultDict.update(self.getResUsage(configDict=configDict))
        self.resultDict.update(self.getProcessState(configDict=configDict))
        self.resultDict.update(self.getDirFiles(configDict=configDict))

#----------------------------------------------------------------------------- 
#-----------------------------------------------------------------------------
def testCase(mode):
    # Init the logger;
    # import os, sys
    # import Log
    # DIR_PATH = dirpath = os.path.dirname(__file__)
    # TOPDIR = 'src'
    # LIBDIR = 'lib'
    # idx = dirpath.find(TOPDIR)
    # gTopDir = dirpath[:idx + len(TOPDIR)] if idx != -1 else dirpath   # found it - truncate right after TOPDIR
    # # Config the lib folder 
    # gLibDir = os.path.join(gTopDir, LIBDIR)
    # if os.path.exists(gLibDir):
    #     sys.path.insert(0, gLibDir)
    # APP_NAME = ('TestCaseLog', 'networkServiceProber')
    # import Log
    # Log.initLogger(gTopDir, 'Logs', APP_NAME[0], APP_NAME[1], historyCnt=100, fPutLogsUnderDate=True)
    driver = localServiceProber('127.0.0.1')
    if mode == 0:
        configDict =  {
                'cpu': {'interval': 0.1, 'percpu': False},
                'ram': 0,
                'user': None,
                'disk': ['C:'],
                'network': {'connCount': 0}
            }
        result = driver.getResUsage(configDict=configDict)

    elif mode == 1:
        configDict =  {
                'process': {'count': 0, 'filter': ['python.exe', 'Fing.exe']},
            }
        result = driver.getProcessState(configDict=configDict)
    elif mode == 2:
        configDict =  {
            'dir': [r'C:\Works\NCL\Project\Openstack_Config\GPU', 'M:'],
        }
        result = driver.getDirFiles(configDict=configDict)
    elif mode == 3:
        configDict =  {
                'cpu': {'interval': 0.1, 'percpu': True},
                'ram': 0,
                'user': None,
                'disk': ['C:'],
                'network': {'connCount': 0},
                'process': {'count': 0, 'filter': ['python.exe', 'Fing.exe']},
                'dir': [r'C:\Works\NCL\Project\Openstack_Config\GPU', 'M:'],
            }
        driver.updateResUsage(configDict=configDict)
        result = driver.getLastResult()

    print(result)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
if __name__ == '__main__':
    testCase(3)
