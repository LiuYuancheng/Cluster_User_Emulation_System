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
import importlib
import pyfiglet
import actionGlobal as gv
import actionScheduler
from actionScheduler import UserAction, RandomAction, WeeklyAction

# Import the user's profile.
sProfiling = importlib.import_module(gv.CONFIG_DICT['PROFILE'])
ACTOR_NAME = sProfiling.ACTOR_NAME

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def _addInfo2Actor(actor, actionConfig):
    if 'actDetail' in actionConfig.keys():
        actor.addActionInfo('actDetail', actionConfig['actDetail'])

    if 'actDesc' in actionConfig.keys():
        actor.addActionInfo('actDesc', actionConfig['actDesc'])

    owner = actionConfig['actOwner'] if 'actOwner' in actionConfig.keys() else ACTOR_NAME
    actor.addActionInfo('actOwner', owner)

    dependentAct = actionConfig['depend'] if 'depend' in actionConfig.keys() else 0
    actor.addActionInfo('depend', dependentAct)

#-----------------------------------------------------------------------------
def addOneAction(actionConfig):
    """ Add action which will be executed everyday. 
        Args:
            actionConfig (dict): action config dictionary. 
            example:
            actionDict = { 'time': '09:01',
                            'name': '09:01_ping',
                            'actionFunc': actorFunctions.func_0901,
                            'parallelTH': False,
                            'actDetail': 'Ping 30 destinations', # (optional)
                            'actDesc': 'Ping and show in OS terminal.', #(optional)
                            'actOwner': 'admin:LYC' #(optional)} 
    """
    actor = UserAction(actionName=actionConfig['name'],
                       timeStr=actionConfig['time'],
                       runFunc=actionConfig['actionFunc'],
                       threadFlg=actionConfig['parallelTH'])
    _addInfo2Actor(actor, actionConfig)
    gv.iScheduler.registerDailyAction(actor)

#-----------------------------------------------------------------------------
def addRandomAction(actionConfig):
    """ Add action which will be executed random in every time interval. 
        Args:
            actionConfig (dict): action config dictionary.
            example: 
            action_rand = {
                'name': 'random_print_time ',
                'randomInt': (5, 10), # evey 10 sec run once in a random time point between 5s and 10s.
                'actionFunc': lambda: print(datetime.datetime.now()),
                'parallelTH': True,
                'actDetail': 'just a print',#(optional)
                'actDesc': 'Print the time in a time period to test the randome task.',#(optional)
                'actOwner': 'admin:LYC' #(optional)}
    """
    actor = RandomAction(actionName=actionConfig['name'],
                       randInt=actionConfig['randomInt'],
                       runFunc=actionConfig['actionFunc'],
                       threadFlg=True)
    _addInfo2Actor(actor, actionConfig)
    gv.iScheduler.registerRandomAction(actor)

#-----------------------------------------------------------------------------
def addWeeklyAction(actionConfig):
    """ Add action which will be executed every week at time point. 
        Args:
            actionConfig (dict): _description_
            action_weekly = {
                'name': 'weekly_print_date',
                'weeklist': [1, 7], # Week index Mon[1] ~ Sun[7] 
                'time': '17:35',
                'actionFunc': lambda: print(datetime.datetime.today()),
                'parallelTH': True,
                'actDetail': 'just a print',#(optional)
                'actDesc': 'Print the date on Mon and Sun.',#(optional)
                'actOwner': 'admin:LYC'#(optional)
            }
    """
    actor = WeeklyAction(actionName=actionConfig['name'],
                       weekIdxList=actionConfig['weeklist'],
                       timeStr=actionConfig['time'],
                       runFunc=actionConfig['actionFunc'],
                       threadFlg=True)

    _addInfo2Actor(actor, actionConfig)
    gv.iScheduler.registerWeeklyAction(actor)

#-----------------------------------------------------------------------------
def main():

    ascii_banner = pyfiglet.figlet_format("CUE Scheduler")
    print(ascii_banner)

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
    # Regiser and report to hub if set the report flag.
    if gv.RPT_MD:
        gv.gDebugPrint("Register to the hub: %s" %str(gv.HUB_IP), logType=gv.LOG_INFO)
        gv.iScheduler.reportTohub()

    gv.iScheduler.startSimulate()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
