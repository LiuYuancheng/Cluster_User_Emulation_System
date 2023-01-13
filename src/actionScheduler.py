#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        scheduler.py
#
# Purpose:     This module is a script use python <schedule> module to scheduler 
#              the user's regular or random tasks (call different actor module 
#              to simulate a normal user's daily action or generate random network 
#              traffic comm or local operation event).   
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
import schedule

import actionGlobal as gv
import dataManager 
import Log

DIR_PATH = os.path.dirname(__file__)
print("Current source code location : %s" % DIR_PATH)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class userAction(object):

    def __init__(self, actionName='', timeStr=None, runFunc=None, threadFlg=False) -> None:
        self.id = -1                    # The action ID, only a valid id (>0) action can be actived. 
        self.name = actionName
        self.timeStr = timeStr          # Fmt HH:MM or HH:MM:SS
        self.func = runFunc
        self.jobType = 0
        self.activeFunc = True
        self.state = gv.JB_ST_PENDING
        self.threadFlg = threadFlg
        self.optionalInfo = {}          # optional info in the action such as (action detail, description, Owner and dependency)
        
        self.scheduleJobRef = None
        self._jobthread = None

#-----------------------------------------------------------------------------
    def setID(self,newId):
        self.id = newId

#-----------------------------------------------------------------------------
    def activeAction(self):
        if self.id > 0:
            self.scheduleJobRef = schedule.every().day.at(self.timeStr).do(self.runFunc)
            self.activeFunc = True
            #if gv.iDataMgr: gv.iDataMgr.updateActStat(self.id, self.state)
        else:
            print("The Action id is not valid: %s" % str(self.id))

#-----------------------------------------------------------------------------
    def runFunc(self):
        Log.info('Start to run job [%s]: %s' %(str(self.id), str(self.name)))
        if self.func:
            self.state = gv.JB_ST_RUNNING
            if gv.iDataMgr: gv.iDataMgr.updateActStat(self.id, self.state)
            try:
                if self.threadFlg:
                    self._jobthread = threading.Thread(target=self.func)
                    self._jobthread.start()
                    Log.info('Running...')
                else:
                    self.func()
                self.state = gv.JB_ST_FINISH
                if gv.iDataMgr: gv.iDataMgr.updateActStat(self.id, self.state)
                Log.info('=> Finish job[%s]:%s' %(str(self.id), str(self.name)))
            except Exception as err:
                Log.error("Run job %s error :" %str(self.name))
                Log.exception(err)
                self.state = gv.JB_ST_ERROR
                if gv.iDataMgr: gv.iDataMgr.updateActStat(self.id, self.state)
        else:
            Log.info('No function is added.')

#-----------------------------------------------------------------------------
    def getJobState(self):
        if self.activeFunc:
            return self.state
        return None

#-----------------------------------------------------------------------------
    def jobThreadJoin(self):
        """ Join the job thread """
        if self._jobthread and self._jobthread.isAlive():
            self._jobthread.join()

#-----------------------------------------------------------------------------
    def addActionInfo(self, key, val):
        self.optionalInfo[key] = val

#-----------------------------------------------------------------------------
    def getActionInfo(self, key):
        if key in self.optionalInfo.keys():
            return self.optionalInfo[key]
        return None

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class actionScheduler(object):

    def __init__(self, actorName=None) -> None:
        # The action dictionary
        self.actorName = actorName if actorName else 'localHost'
        self.actionDictD = {}
        self.actionDictR = {}
        self.actionDictW = {}
        
        self.terminate = False
        self.taskCount = 0

        # start the datamanager to handler the monitor and database 
        gv.iDataMgr = dataManager.DataManager(self)
        gv.iDataMgr .start()
        Log.info("Scheduler: %s init ready." %str(self.actorName ))

    def getNewId(self):
        self.taskCount += 1
        return self.taskCount

    def registerDailyAction(self, actionObj):
        if actionObj:
            newId = self.getNewId()
            actionObj.setID(newId)
            actionObj.activeAction()
            regInfoDict = {
                'actId': actionObj.id,
                'actName': actionObj.name,
                'actDetail': actionObj.getActionInfo('actDetail'),
                'actDesc': actionObj.getActionInfo('actDesc'),
                'actOwner': actionObj.getActionInfo('actOwner'),
                'actType': actionObj.jobType,
                'startT': actionObj.timeStr,
                'depend': actionObj.getActionInfo('depend'),
                'threadType': 1 if actionObj.threadFlg else 0,
                'actState': actionObj.state
            }

            gv.iDataMgr.registerActions(regInfoDict)
            #self.actionDictD[str(actionObj.id)] = actionObj
            Log.info("Registered action id: %s , name: %s in DB." %(str(regInfoDict['actId']), regInfoDict['actId']))

    def addAction(self, actionObj):
        if actionObj:
            #self.actionDict[actionObj.name] = actionObj
            schedule.every().day.at(actionObj.timeStr).do(actionObj.runFunc)

    def startSimulate(self):
        print("Actor: %s start all the below jobs:" %str(self.actorName) )
        for job in schedule.get_jobs():
            print(job.__str__)
       
        while not self.terminate:
            schedule.run_pending()
            time.sleep(1)

