#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        run.py
#
# Purpose:     Config the scheduler as one user then run the program.
#
# Author:      Yuancheng Liu
#
# Version:     v_0.1
# Created:     2023/01/13
# Copyright:   n.a
# License:     n.a
#-----------------------------------------------------------------------------

import actionGlobal as gv
import actionScheduler
from actionScheduler import UserAction, RandomAction, WeeklyAction

# Import the user's profile.
import scheduleProfile as sProfiling

ACTOR_NAME = sProfiling.ACTOR_NAME

#-----------------------------------------------------------------------------
def addOneAction(actionConfig):
    actor = UserAction(actionName=actionConfig['name'],
                       timeStr=actionConfig['time'],
                       runFunc=actionConfig['actionFunc'],
                       threadFlg=actionConfig['parallelTH'])
    if 'actDetail' in actionConfig.keys():
        actor.addActionInfo('actDetail', actionConfig['actDetail'])

    if 'actDesc' in actionConfig.keys():
        actor.addActionInfo('actDesc', actionConfig['actDesc'])

    owner = actionConfig['actOwner'] if 'actOwner' in actionConfig.keys() else ACTOR_NAME
    actor.addActionInfo('actOwner', owner)

    dependentAct = actionConfig['depend'] if 'depend' in actionConfig.keys() else 0
    actor.addActionInfo('depend', dependentAct)

    gv.iScheduler.registerDailyAction(actor)

#-----------------------------------------------------------------------------
def addRandomAction(actionConfig):
    actor = RandomAction(actionName=actionConfig['name'],
                       randInt=actionConfig['randomInt'],
                       runFunc=actionConfig['actionFunc'],
                       threadFlg=True)

    if 'actDetail' in actionConfig.keys():
        actor.addActionInfo('actDetail', actionConfig['actDetail'])

    if 'actDesc' in actionConfig.keys():
        actor.addActionInfo('actDesc', actionConfig['actDesc'])

    owner = actionConfig['actOwner'] if 'actOwner' in actionConfig.keys() else ACTOR_NAME
    actor.addActionInfo('actOwner', owner)

    dependentAct = actionConfig['depend'] if 'depend' in actionConfig.keys() else 0
    actor.addActionInfo('depend', dependentAct)
    
    gv.iScheduler.registerRandomAction(actor)

#-----------------------------------------------------------------------------
def addWeeklyAction(actionConfig):
    actor = WeeklyAction(actionName=actionConfig['name'],
                       weekIdxList=actionConfig['weeklist'],
                       timeStr=actionConfig['time'],
                       runFunc=actionConfig['actionFunc'],
                       threadFlg=True)

    if 'actDetail' in actionConfig.keys():
        actor.addActionInfo('actDetail', actionConfig['actDetail'])

    if 'actDesc' in actionConfig.keys():
        actor.addActionInfo('actDesc', actionConfig['actDesc'])

    owner = actionConfig['actOwner'] if 'actOwner' in actionConfig.keys() else ACTOR_NAME
    actor.addActionInfo('actOwner', owner)

    dependentAct = actionConfig['depend'] if 'depend' in actionConfig.keys() else 0
    actor.addActionInfo('depend', dependentAct)
    
    gv.iScheduler.registerWeeklyAction(actor)

#-----------------------------------------------------------------------------
def main():
    gv.iScheduler = actionScheduler.actionScheduler(actorName=ACTOR_NAME)
    gv.gDebugPrint("Add %s daily actions to scheduler: " %str(len(sProfiling.dailyTaskList)), logType=gv.LOG_INFO)
    for dailyAction in sProfiling.dailyTaskList:
        addOneAction(dailyAction)

    gv.gDebugPrint("Add %s random actions to scheduler: " %str(len(sProfiling.randomTaskList)), logType=gv.LOG_INFO)
    for randomAction in sProfiling.randomTaskList:
        addRandomAction(randomAction)

    gv.gDebugPrint("Add %s weekly actions to scheduler: " %str(len(sProfiling.weeklyTaskList)), logType=gv.LOG_INFO)
    for weeklyAction in sProfiling.weeklyTaskList:
        addWeeklyAction(weeklyAction)

    gv.iScheduler.startSimulate()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
