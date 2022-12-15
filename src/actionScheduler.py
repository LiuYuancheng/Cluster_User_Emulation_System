#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        scheduler.py
#
# Purpose:     This module is a script use python <schedule> module to scheduler 
#              the user's tasks (call different actor module to simulate a normal 
#              user's daily action).   
#              <schedule> reference link: https://schedule.readthedocs.io/en/stable/
#
# Author:      Yuancheng Liu
#
# Version:     v_0.1
# Created:     2022/12/09
# Copyright:   n.a
# License:     n.a
#-----------------------------------------------------------------------------

# https://schedule.readthedocs.io/en/stable/

import os
import time
import datetime
import threading
import subprocess

import schedule

import actionGlobal as gv

DIR_PATH = os.path.dirname(__file__)
print("Current source code location : %s" % DIR_PATH)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class userAction(object):
    def __init__(self, actionName='', timeStr=None, runFunc=None, threadFlg=False) -> None:
        self.name = actionName
        self.timeStr = timeStr
        self.func = runFunc
        self.threadFlg = threadFlg
        self._jobthread = None

#-----------------------------------------------------------------------------
    def runFunc(self):
        print('Start to run job: %s' %str(self.name))
        if self.func:
            if self.threadFlg:
                self._jobthread = threading.Thread(target=self.func)
                self._jobthread.start()
            else:
                self.func()
        else:
            print('No function is added.')

#-----------------------------------------------------------------------------
    def jobThreadJoin(self):
        """ Join the job thread """
        if self._jobthread and self._jobthread.isAlive():
            self._jobthread.join()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class actionScheduler(object):

    def __init__(self) -> None:
        # The action dictionary
        self.actionDict = {}
        self.terminate = False 

    def addAction(self, actionObj):
        if actionObj:
            #self.actionDict[actionObj.name] = actionObj
            schedule.every().day.at(actionObj.timeStr).do(actionObj.runFunc)

    def startSimulate(self):
        while not self.terminate:
            schedule.run_pending()
            time.sleep(1)



def testCase(mode):

    timeData = datetime.datetime.now() 
    minDelay = datetime.timedelta(seconds = 60)
    
    # Task 1: ping
    def func1():
        appFolder = 'UtilsFunc'
        appName = 'pingActor.py'
        appPath = os.path.join(DIR_PATH, appFolder, appName)
        cmd = "python %s" %str(appPath)
        subprocess.call(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
    timeData+= datetime.timedelta(seconds = 10)
    nextMin = timeData.strftime("%H:%M:%S")
    print(nextMin)
    userAction1 = userAction(actionName='action1', timeStr=nextMin, runFunc=func1, threadFlg=False)
    

    # Task 1_1: run server windows cmds.
    def func1_1():
        appFolder = 'UtilsFunc'
        appName = 'funcActor.py'
        appPath = os.path.join(DIR_PATH, appFolder, appName)
        cmd = "python %s" %str(appPath)
        subprocess.call(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
    timeData+= datetime.timedelta(seconds = 10)
    nextMin = timeData.strftime("%H:%M:%S")
    print(nextMin)
    userAction1 = userAction(actionName='action1_1', timeStr=nextMin, runFunc=func1_1, threadFlg=False)
    schedule.every().day.at(userAction1.timeStr).do(userAction1.runFunc)

    # start Zoom meeting
    def func2():
        appFolder = 'UtilsFunc'
        appName = 'zoomActor.py'
        appPath = os.path.join(DIR_PATH, appFolder, appName)
        cmd = "python %s" %str(appPath)
        subprocess.call(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
    timeData += minDelay
    nextMin = timeData.strftime("%H:%M:%S")
    userAction2 = userAction(actionName='action2', timeStr=nextMin, runFunc=func2, threadFlg=False)
    schedule.every().day.at(userAction2.timeStr).do(userAction2.runFunc)

    # Draw picture
    def func3():
        os.startfile("C:\\Works\\NCL\\Project\\Windows_User_Simulator\\src\\dist\\actionSimulator.exe")

    timeData += minDelay
    nextMin = timeData.strftime("%H:%M:%S")
    userAction3 = userAction(actionName='action3', timeStr=nextMin, runFunc=func3, threadFlg=True)
    schedule.every().day.at(userAction3.timeStr).do(userAction3.runFunc)
    
    # playgame
    def func4():
        appFolder = 'UtilsFunc'
        appName = 'dinoActor.py'
        appPath = os.path.join(DIR_PATH, appFolder, appName)
        cmd = "python %s" %str(appPath)
        subprocess.call(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
        #subprocess.call('python C:\\Works\\NCL\\Project\\Windows_User_Simulator\\src\\UtilsFunc\\dinoActor.py', creationflags=subprocess.CREATE_NEW_CONSOLE)

    timeData += minDelay
    nextMin = timeData.strftime("%H:%M:%S")
    userAction3 = userAction(actionName='action4', timeStr=nextMin, runFunc=func4, threadFlg=True)
    schedule.every().day.at(userAction3.timeStr).do(userAction3.runFunc)

    print(schedule.get_jobs())

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    testCase(1)

