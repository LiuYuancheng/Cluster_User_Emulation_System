#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        scheduler.py
#
# Purpose:     This module is a script use python <schedule> module to manage 
#              the regular or random tasks (call the different actor modules to 
#              simulate a normal user's daily action, generate random network 
#              comm traffic or local operation event).   
#              <schedule> reference link: https://schedule.readthedocs.io/en/stable/
#
# Author:      Yuancheng Liu
#
# Version:     v_0.2
# Created:     2022/12/09
# Copyright:   n.a
# License:     n.a
#-----------------------------------------------------------------------------

import os
import time
import threading
import schedule

import actionGlobal as gv
import Log
import dataManager

WAIT_INTERVAL = 1 

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class UserAction(object):
    """ The user action class is used to package the detailed task functions so the 
        task-function can be executed parallel with the main thread, controlled by 
        the scheduler and registered in database.
    """

    def __init__(self, actionName='', timeStr=None, runFunc=None, threadFlg=False) -> None:
        """ Init example:
            => if we want to print the time on 9:00 am in the main thread, init the action obj
            as below: 
            actor = userAction(actionName="test", timeStr="9:00",runFunc=print(time.time()),
                    threadFlg=False)
        Args:
            actionName (str, optional): Action name. Defaults to ''.
            timeStr (_type_, optional): Time to execute. Defaults to None.
            runFunc (_type_, optional): task function's ref. Defaults to None.
            threadFlg (bool, optional): flag to identify whether run the task in sub-thread. 
                                        Defaults to False.
        """
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
    def activeAction(self, flg=True):
        """ Active and de-active the action execution."""
        if self.id > 0:
            self.scheduleJobRef = schedule.every().day.at(self.timeStr).do(self.runFunc)
            self.activeFunc = flg
            #if gv.iDataMgr: gv.iDataMgr.updateActStat(self.id, self.state)
        else:
            gv.gDebugPrint("The Action id is not valid: %s" % str(self.id), logType=gv.LOG_WARN)

#-----------------------------------------------------------------------------
    def addActionInfo(self, key, val):
        """ Public interface to add additional parameters in the <optionalInfo>"""
        self.optionalInfo[key] = val

#-----------------------------------------------------------------------------
    def cancelAction(self):
        """ Remove the action from the scheduler."""
        if self.id > 0 and self.scheduleJobRef:
            schedule.cancel_job(self.scheduleJobRef)
            self.activeFunc = False
        else:
            gv.gDebugPrint("The Action id is not valid: %s" % str(self.id), logType=gv.LOG_WARN)

#-----------------------------------------------------------------------------
    def getActionInfo(self, key):
        """ Return the related optional parameter val based on the input key, return
            None if the key is not found. 
        """
        return self.optionalInfo[key] if key in self.optionalInfo.keys() else None

#-----------------------------------------------------------------------------
    def getJobState(self):
        """ Return the current Job state if the task is actived, else None."""
        return self.state if self.activeFunc else None

#-----------------------------------------------------------------------------
    def jobThreadJoin(self):
        """ Join the job thread to the execute thread, this function is used for 
            cascaded thread chain/three.
        """
        if self._jobthread and self._jobthread.isAlive():
            self._jobthread.join()

#-----------------------------------------------------------------------------
    def runFunc(self):
        """ Execute the packaged task function."""
        gv.gDebugPrint('Start to run job [%s]: %s' %(str(self.id), str(self.name)), logType=gv.LOG_INFO)
        if self.func:
            self.state = gv.JB_ST_RUNNING
            if gv.iDataMgr: gv.iDataMgr.updateActStat(self.id, self.state)
            try:
                if self.threadFlg:
                    self._jobthread = threading.Thread(target=self.func)
                    self._jobthread.start()
                    gv.gDebugPrint('Running in sub-thread...', logType=gv.LOG_INFO)
                else:
                    gv.gDebugPrint('Running under main-thread...', logType=gv.LOG_INFO)
                    self.func()
                self.state = gv.JB_ST_FINISH
                if gv.iDataMgr: gv.iDataMgr.updateActStat(self.id, self.state)
                gv.gDebugPrint('=> Finish job[%s]:%s' %(str(self.id), str(self.name)), logType=gv.LOG_INFO)
            except Exception as err:
                gv.gDebugPrint("Run job %s error :" %str(self.name), logType=gv.LOG_ERR)
                Log.exception(err)
                self.state = gv.JB_ST_ERROR
                if gv.iDataMgr: gv.iDataMgr.updateActStat(self.id, self.state)
        else:
            gv.gDebugPrint('No function is added.', logType=gv.LOG_WARN)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class RandomAction(UserAction):

    def __init__(self, actionName='', randInt=(5,10), runFunc=None, threadFlg=False) -> None:
        super().__init__(actionName=actionName, timeStr=None, runFunc=runFunc, threadFlg=threadFlg)
        self.randInt = randInt  # random execution task interval 

#-----------------------------------------------------------------------------
    def activeAction(self, flg=True):
        """ Active and de-active the action execution."""
        if self.id > 0:
            self.scheduleJobRef = schedule.every(5).to(10).seconds.do(self.runFunc)
            self.activeFunc = flg
            #if gv.iDataMgr: gv.iDataMgr.updateActStat(self.id, self.state)
        else:
            gv.gDebugPrint("The Action id is not valid: %s" % str(self.id), logType=gv.LOG_WARN)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class WeeklyAction(UserAction):

    def __init__(self, actionName='', weekIdxList=None, timeStr=None, runFunc=None, threadFlg=False) -> None:
        super().__init__(actionName=actionName, timeStr=timeStr, runFunc=runFunc, threadFlg=threadFlg)
        self.weekIdxList = weekIdxList

    #-----------------------------------------------------------------------------
    def activeAction(self, flg=True):
        """ Active and de-active the action execution."""
        if self.id > 0 and self.weekIdxList:
            for weekIdx in self.weekIdxList:
                if weekIdx == 1: 
                    schedule.every().monday.at(self.timeStr).do(self.runFunc)
                elif weekIdx == 2:
                    schedule.every().tuesday.at(self.timeStr).do(self.runFunc)
                elif weekIdx == 3:
                    schedule.every().wednesday.at(self.timeStr).do(self.runFunc)
                elif weekIdx == 4:
                    schedule.every().thursday.at(self.timeStr).do(self.runFunc)
                elif weekIdx == 5:
                    schedule.every().friday.at(self.timeStr).do(self.runFunc)
                elif weekIdx == 6:
                    schedule.every().saturday.at(self.timeStr).do(self.runFunc)
                else:
                    schedule.every().sunday.at(self.timeStr).do(self.runFunc)
            self.scheduleJobRef = schedule.every(5).to(10).seconds.do(self.runFunc)
            self.activeFunc = flg
            #if gv.iDataMgr: gv.iDataMgr.updateActStat(self.id, self.state)
        else:
            gv.gDebugPrint("The Action id is not valid: %s" % str(self.id), logType=gv.LOG_WARN)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class actionScheduler(object):
    """ Register the <userAction> in database and schedule the tasks. Each scheduler
        will emulate one user's action.
    """
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
        gv.iDataMgr.start()
        gv.gDebugPrint("Scheduler: %s init ready." %str(self.actorName), logType=gv.LOG_INFO)

#-----------------------------------------------------------------------------
    def _getNewId(self):
        self.taskCount += 1
        return self.taskCount

#-----------------------------------------------------------------------------
    def _getActionRegInfo(self, actionObj):
        newId = self._getNewId()
        actionObj.setID(newId)
        actionObj.activeAction()
        return {'actId': actionObj.id,
                'actName': actionObj.name,
                'actDetail': actionObj.getActionInfo('actDetail'),
                'actDesc': actionObj.getActionInfo('actDesc'),
                'actOwner': actionObj.getActionInfo('actOwner'),
                'actType': actionObj.jobType, 
                'depend': actionObj.getActionInfo('depend'),
                'threadType': 1 if actionObj.threadFlg else 0,
                'actState': actionObj.state}

#-----------------------------------------------------------------------------
    def _printAllJobs(self):
        gv.gDebugPrint("Actor: %s will execute all current jobs:" %str(self.actorName), logType=gv.LOG_INFO)
        for job in schedule.get_jobs():
            gv.gDebugPrint(job.__str__, logType=gv.LOG_INFO)

#-----------------------------------------------------------------------------
    def startSimulate(self):
        """ Start to execute the jobs based on the scheduled profile."""
        gv.gDebugPrint("Actor: %s start to execute scheduled jobs" %str(self.actorName), logType=gv.LOG_INFO)
        self._printAllJobs()
        while not self.terminate:
            schedule.run_pending()
            time.sleep(WAIT_INTERVAL)

#-----------------------------------------------------------------------------
    def stopSimulate(self):
        self.terminate = True

#-----------------------------------------------------------------------------
    def registerDailyAction(self, actionObj):
        if actionObj:
            regInfoDict = self._getActionRegInfo(actionObj)
            regInfoDict['startT'] = actionObj.timeStr
            gv.iDataMgr.registerActions(regInfoDict, actType=gv.JB_TP_DAILY)
            self.actionDictD[str(actionObj.id)] = actionObj
            gv.gDebugPrint("Registered daily-action id:[%s], name:[%s] in DB." %(str(regInfoDict['actId']), regInfoDict['actName']), 
                            logType=gv.LOG_INFO)

#-----------------------------------------------------------------------------
    def registerRandomAction(self, actionObj):
        if actionObj:
            regInfoDict = self._getActionRegInfo(actionObj)
            regInfoDict['startT'] = str(actionObj.randInt)
            gv.iDataMgr.registerActions(regInfoDict, actType=gv.JB_TP_RANDOM)
            self.actionDictR[str(actionObj.id)] = actionObj
            gv.gDebugPrint("Registered random-action id:[%s] , name:[%s] in DB." %(str(regInfoDict['actId']), regInfoDict['actName']), 
                            logType=gv.LOG_INFO)

#-----------------------------------------------------------------------------
    def registerWeeklyAction(self, actionObj):
        if actionObj:
            regInfoDict = self._getActionRegInfo(actionObj)
            regInfoDict['startT'] = ';'.join((str(actionObj.weekIdxList), str(actionObj.timeStr)))
            gv.iDataMgr.registerActions(regInfoDict, actType=gv.JB_TP_WEEKLY)
            self.actionDictW[str(actionObj.id)] = actionObj
            gv.gDebugPrint("Registered weekly-action id:[%s] , name:[%s] in DB." %(str(regInfoDict['actId']), regInfoDict['actName']), 
                            logType=gv.LOG_INFO)

#-----------------------------------------------------------------------------
    def removeAction(self, actionID):
        if str(actionID) in self.actionDictD.keys():
            gv.gDebugPrint("Try to remove the action [ %s ]" %str(actionID), logType=gv.LOG_WARN)
            try:
                actionObj = self.actionDictD[str(actionID)]
                actionObj.cancelAction()
                self._printAllJobs()
                return True
            except Exception as error: 
                gv.gDebugPrint("Cancel jobs error: %s" %str(error), logType=gv.LOG_EXCEPT)
                return False
        else:
            gv.gDebugPrint("The id is not registered", logType=gv.LOG_ERR)
            return False
