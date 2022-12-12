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

TIME_OUT = 1    # ping timeout set to 1sec

class pingActor(object): 

    def __init__(self, config, parallel=False, Log=None, showConsole=False) -> None:
        
        self.pingDict = {}
        if isinstance(config, dict):
            self.pingDict = config
        elif isinstance(config, str):
            if os.path.exists(config):
                try:
                    self.pingDict = json.load(config)
                except Exception as err:
                    print("Failed to load the config file: %s" %str(err))
        else: 
            print('Input config file/parameter not valid.')
            return None
        self.parallel = parallel
        self.log = Log
        self.showConsole = showConsole
        self.jobThreadList = []
        print('__init__ finished')
        self.pingInterval = 0.1 # time between each ping

    def addPeer(self, dest, timeN):
        if self.pingDict:
            self.pingDict[str(dest)] = int(timeN)
            return True
        return False
    
    def removePeer(self, dest):
        if self.pingDict and dest in self.pingDict.keys():
            self.pingDict.pop(dest)
            return True
        return False

    def setPingInterval(self, interval):
        self.pingInterval = interval


    def runPing(self):
        print('Start to ping all the dest.')
        if self.showConsole:
            if self.parallel: self.jobThreadList = []
            # pop up the console to show the ping.
            for item in self.pingDict.items():
                dest, timeN = item
                def pingFunc(dest, timeN):
                    if timeN <= 0: timeN = randint(1, 10)
                    pingCmd = "ping -n %s %s" %(str(timeN), dest)
                    try:
                        result = subprocess.call(pingCmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
                        return result
                    except Exception as err:
                        print('Pop the console terminal failed: %s' %str(err))
                        return False
                if self.parallel:
                    jobthread = threading.Thread(target=pingFunc, args=(dest, timeN,))
                    self.jobThreadList.append(jobthread)
                else:
                    pingFunc(dest, timeN)
                    time.sleep(self.pingInterval)
            # if have job, run the parallel ping
            _ = [ job.start() for job in self.jobThreadList ] 
            _ = [ job.join() for job in self.jobThreadList ] 
        else:
            crtPingRst = {}
            if self.parallel: self.jobThreadList = []
            for item in self.pingDict.items():
                dest, timeN = item
                #print(dest)
                def pingFunc(dest, timeN): 
                    if timeN <= 0: timeN = randint(1, 10)
                    crtPingRst[str(dest)] = []
                    #print(dest)
                    for i in range(timeN):
                        data = ping(dest, timeout=TIME_OUT, verbose=False)
                        time.sleep(self.pingInterval)
                        # log the result
                        if self.log:
                            self.log.info('[%s]: min:%s,avg:%s,max:%s', dest, str(data.rtt_min_ms), str(data.rtt_avg_ms), str(data.rtt_max_ms))
                        crtPingRst[str(dest)].append(data.rtt_avg_ms)
                
                if self.parallel:
                    jobthread = threading.Thread(target=pingFunc, args=(dest, timeN,))
                    self.jobThreadList.append(jobthread)
                else:
                    pingFunc(dest, timeN)
                    time.sleep(self.pingInterval)
            # if have job, run the parallel ping
            _ = [ job.start() for job in self.jobThreadList ] 
            _ = [ job.join() for job in self.jobThreadList ] 
            return crtPingRst

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

def testCase(mode =0):
    pinDict = {
        "www.google.com.sg": 5,
        "172.18.178.10": 2,
        "202.94.70.56": 3,
        "www.singtel.com.sg": 4, 
        "gov.sg": 5,
        "BBC.CO.UK" : 5
    }
    if mode == 1:
        parallel=False
        Log=None
        showConsole=False
        actor = pingActor(pinDict,parallel=parallel, Log=Log, showConsole=showConsole)
        result = actor.runPing()
        print(result)
    elif mode == 2:
        parallel=False
        Log=None
        showConsole=True
        actor = pingActor(pinDict,parallel=parallel, Log=Log, showConsole=showConsole)
        result = actor.runPing()
        print(result)
    elif mode == 3:
        parallel=True
        Log=None
        showConsole=False
        actor = pingActor(pinDict,parallel=parallel, Log=Log, showConsole=showConsole)
        result = actor.runPing()
        print(result)
    elif mode == 4:
        parallel=True
        Log=None
        showConsole=True
        actor = pingActor(pinDict,parallel=parallel, Log=Log, showConsole=showConsole)
        result = actor.runPing()
        print(result)

if __name__ == '__main__':
    testCase(mode=4)