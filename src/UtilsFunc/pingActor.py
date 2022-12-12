#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        pingActor.py
#
# Purpose:     This module will ping the destination ip/url dict periodically 
#              one by one in sequential or ping the destinations parallel at the 
#              same time. If passed in the Logger the module will save the ping 
#              result in local disk. 
#
# Author:      Yuancheng Liu
#
# Version:     v_0.1
# Created:     2022/12/12
# Copyright:   n.a
# License:     n.a
#-----------------------------------------------------------------------------

import os 
import time
import json
import threading
import subprocess
from random import randint
from pythonping import ping

TIME_OUT = 1    # ping timeout setting, default set to 1 sec.
TIME_INT = 0.1    # sleep interval between each 2 ping, default set to 0.1 sec.

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

class pingActor(object): 

    def __init__(self, config, parallel=False, Log=None, showConsole=False) -> None:
        """ Init the ping Actor: 
            actor = pingActor({'127.0.0.1':10},parallel=True, Log=None, showConsole=False)
        Args:
            config (_type_): ping destination config dictionary or the dictionary json file path. 
                             json item format 'dest ip/url': int(pingtime)
            parallel (bool, optional): Ping the dest in sequential or parallel threading 
                            (multi-thread). Defaults to False.
            Log (_type_, optional): a logger object. Defaults to None.
            showConsole (bool, optional): flag to whether pop-up the os console. Defaults to False.

        Returns:
            _type_: pingActor obj.
        """
        self.pingDict = {}
        if isinstance(config, dict):
            self.pingDict = config
        elif isinstance(config, str):
            if os.path.exists(config):
                try:
                    self.pingDict = json.load(config)
                except Exception as err:
                    print("Failed to load the json config file: %s" %str(err))
                    return None
        else: 
            print('The input <config> file/parameter is not valid.')
            return None
        self.parallel = parallel
        self.jobThreadList = []
        self.log = Log
        self.showConsole = showConsole
        print('__init__ finished')
        self._pingInterval = TIME_INT # time between each ping
        self._pingTimeout = TIME_OUT

#-----------------------------------------------------------------------------
    def addDest(self, dest, timeN):
        if self.pingDict:
            self.pingDict[str(dest)] = int(timeN)
            return True
        return False

#-----------------------------------------------------------------------------
    def removeDest(self, dest):
        if self.pingDict and dest in self.pingDict.keys():
            self.pingDict.pop(dest)
            return True
        return False

#-----------------------------------------------------------------------------
    def setPingInterval(self, interval):
        self._pingInterval = interval

#-----------------------------------------------------------------------------
    def setPingTimeout(self, timeout):
        self._pingTimeout = timeout

#-----------------------------------------------------------------------------
    def repeatPingJobs(self):
        """ Repeat the ping jobs saved in the job list."""
        print("Weekup the ping jobs in the job list")
        _ = [ job.start() for job in self.jobThreadList ] 
        _ = [ job.join() for job in self.jobThreadList ] 

#-----------------------------------------------------------------------------
    def runPing(self):
        """ load the config and do the ping."""
        print('Start to ping all the dest ...')
        if self.parallel: self.jobThreadList = []
        if self.showConsole:
            # Pop up the console to show the ping.In this function no data recorded.
            for item in self.pingDict.items():
                dest, timeN = item
                def pingFunc(dest, timeN):
                    if timeN < 0: timeN = randint(1, 10)
                    pingCmd = "ping -n %s %s" % (str(timeN), dest)
                    try:
                        result = subprocess.call(pingCmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
                        return result
                    except Exception as err:
                        print('Pop the console terminal failed: %s' % str(err))
                        return False
                if self.parallel:
                    jobthread = threading.Thread(target=pingFunc, args=(dest, timeN,))
                    self.jobThreadList.append(jobthread)
                else:
                    pingFunc(dest, timeN)
                    time.sleep(self._pingInterval)
            # if have job, run the parallel ping
            self.repeatPingJobs()
        else:
            # Run the ping action in back ground and record the result.
            crtPingRst = {}
            for item in self.pingDict.items():
                dest, timeN = item
                #print(dest)
                def pingFunc(dest, timeN): 
                    if timeN < 0: timeN = randint(1, 10)
                    crtPingRst[str(dest)] = []
                    #print(dest)
                    for i in range(timeN):
                        data = ping(dest, timeout=self._pingTimeout, verbose=False)
                        time.sleep(self._pingInterval)
                        # log the result
                        if self.log:
                            self.log.info('[%s]: min:%s,avg:%s,max:%s', dest, str(data.rtt_min_ms), str(data.rtt_avg_ms), str(data.rtt_max_ms))
                        crtPingRst[str(dest)].append(data.rtt_avg_ms)
                
                if self.parallel:
                    jobthread = threading.Thread(target=pingFunc, args=(dest, timeN,))
                    self.jobThreadList.append(jobthread)
                else:
                    pingFunc(dest, timeN)
                    time.sleep(self._pingInterval)
            # if have job, run the parallel ping
            self.repeatPingJobs()
            return crtPingRst

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def testCase(mode =0):
    pinDict = {
        "www.google.com.sg": 5,
        "172.18.178.10": 2,
        "202.94.70.56": -1,
        "www.singtel.com.sg": 4, 
        "gov.sg": 5,
        "BBC.CO.UK" : 5
    }
    if mode == 1:
        parallel = False
        Log = None
        showConsole = False
        actor = pingActor(pinDict, parallel=parallel,
                          Log=Log, showConsole=showConsole)
        result = actor.runPing()
        print(result)
    elif mode == 2:
        parallel = False
        Log = None
        showConsole = True
        actor = pingActor(pinDict, parallel=parallel,
                          Log=Log, showConsole=showConsole)
        result = actor.runPing()
        print(result)
    elif mode == 3:
        parallel = True
        Log = None
        showConsole = False
        actor = pingActor(pinDict, parallel=parallel,
                          Log=Log, showConsole=showConsole)
        result = actor.runPing()
        print(result)
    elif mode == 4:
        parallel = True
        Log = None
        showConsole = True
        actor = pingActor(pinDict, parallel=parallel,
                          Log=Log, showConsole=showConsole)
        result = actor.runPing()
        print(result)

if __name__ == '__main__':
    testCase(mode=4)
