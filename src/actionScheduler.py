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
import actorFunctions
import Log

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
        Log.info('Start to run job: %s' %str(self.name))
        if self.func:
            try:
                if self.threadFlg:
                    self._jobthread = threading.Thread(target=self.func)
                    self._jobthread.start()
                else:
                    self.func()
            except Exception as err:
                Log.error("Run job %s error :" %str(self.name))
                Log.exception(err)
        else:
            Log.info('No function is added.')

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
        for job in schedule.get_jobs():
            print(job.__str__)
       
        while not self.terminate:
            schedule.run_pending()
            time.sleep(1)

#-----------------------------------------------------------------------------
def scheduleBobActions():
    # 09:01 ping the config peers
    timeStr = "09:01"
    userAction_0901 = userAction(actionName='09:01_ping', timeStr=timeStr, runFunc=actorFunctions.func_0901, threadFlg=False)
    gv.iScheduler.addAction(userAction_0901)

    # 09:10 ping all the ip in a range
    timeStr = "09:10"
    userAction_0910 = userAction(actionName='09:10_ping', timeStr=timeStr, runFunc=actorFunctions.func_0910, threadFlg=True)
    gv.iScheduler.addAction(userAction_0910)

    # 09:13 run window newtork cmds (this part will take long time)
    timeStr = "09:13"
    userAction_0913 = userAction(actionName='09:13_cmd', timeStr=timeStr, runFunc=actorFunctions.func_0913, threadFlg=True)
    gv.iScheduler.addAction(userAction_0913)

    # 09:20 ssh to the ncl gateway and run commands
    timeStr = "09:20"
    userAction_0920 = userAction(actionName='09:20_ssh', timeStr=timeStr, runFunc=actorFunctions.func_0920, threadFlg=False)
    gv.iScheduler.addAction(userAction_0920)

    # 09:32 do file searchinng system dir-structure check
    timeStr = "09:32"
    userAction_0932 = userAction(actionName='09:32_fileOp', timeStr=timeStr, runFunc=actorFunctions.func_0932, threadFlg=False)
    gv.iScheduler.addAction(userAction_0932)

    # 09:35 do zoom meeting.
    timeStr = "09:35"
    userAction_0935 = userAction(actionName='09:35_zoom', timeStr=timeStr, runFunc=actorFunctions.func_0935, threadFlg=False)
    gv.iScheduler.addAction(userAction_0935)

    # 10:15 download cert, image, css file , js file from a list of webs.
    timeStr = "10:15"
    userAction_1015 = userAction(actionName='10:15_downloadWeb', timeStr=timeStr, runFunc=actorFunctions.func_1015, threadFlg=True)
    gv.iScheduler.addAction(userAction_1015)

    # 10:40 watch some youTube video
    timeStr = "10:40"
    userAction_1040 = userAction(actionName='10:45_Youtube', timeStr=timeStr, runFunc=actorFunctions.func_1040, threadFlg=False)
    gv.iScheduler.addAction(userAction_1040)

    # 10:50 edit word doc
    timeStr = "10:50"
    userAction_1050 = userAction(actionName='10:50_OfficeWord', timeStr=timeStr, runFunc=actorFunctions.func_1050, threadFlg=False)
    gv.iScheduler.addAction(userAction_1050)

    # 11:25 edit word doc
    timeStr = "11:25"
    userAction_1125 = userAction(actionName='11:25_OfficePPT', timeStr=timeStr, runFunc=actorFunctions.func_1125, threadFlg=False)
    gv.iScheduler.addAction(userAction_1125)

    # 11:35 playgame
    timeStr = "11:35"
    userAction_1135 = userAction(actionName='11:35_playgame', timeStr=timeStr, runFunc=actorFunctions.func_1135, threadFlg=False)
    gv.iScheduler.addAction(userAction_1135)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main(actorName):
    gv.iScheduler = actionScheduler()
    
    if actorName == 'Bob':
        scheduleBobActions()
        gv.iScheduler.startSimulate()



def testCase(mode):

    timeData = datetime.datetime.now() 
    minDelay = datetime.timedelta(seconds = 60)
    
    # Task 1: ping

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

    #while True:
    #    schedule.run_pending()
    #    time.sleep(1)

if __name__ == '__main__':
    #testCase(1)
    main('Bob')

