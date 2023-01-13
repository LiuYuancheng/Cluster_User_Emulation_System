#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        run.py
#
# Purpose:     Config the scheduler as one user them run the program
#
# Author:      Yuancheng Liu
#
# Version:     v_0.1
# Created:     2023/01/13
# Copyright:   n.a
# License:     n.a
#-----------------------------------------------------------------------------

import actionGlobal as gv

import actorFunctions
import actionScheduler
from actionScheduler import userAction

ACTOR_NAME = 'Bob (192.168.57.10)'

#-----------------------------------------------------------------------------
def addOneAction(actionConfig):
    actor = userAction(actionName=actionConfig['name'],
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
def main():
    gv.iScheduler = actionScheduler.actionScheduler(actorName=ACTOR_NAME)
    
    action_0901 = {
        'time': '09:01',
        'name': '09:01_ping',
        'actionFunc': actorFunctions.func_0901,
        'parallelTH': False,
        'actDetail': 'Ping 30 destinations',
        'actDesc': 'Ping an internal servers list to check the server connection.',
        'actOwner': 'admin:LYC'
    }
    addOneAction(action_0901)

    action_0910 = {
        'time': '09:10',
        'name': '09:10_ping[MT]',
        'actionFunc': actorFunctions.func_0901,
        'parallelTH': True,
        'actDetail': 'Ping 100+ destinations',
        'actDesc': 'Ping an external servers list to check the server connection.'
    }
    addOneAction(action_0910)

    action_0913 = {
        'time': '09:13',
        'name': '09:13_cmdRun',
        'actionFunc': actorFunctions.func_0913,
        'parallelTH': False,
        'actDetail': 'Run Win_Network cmds',
        'actDesc': 'Run Windows network routing cmds.'
    }
    addOneAction(action_0913)

    action_0920 = {
        'time': '09:20',
        'name': '09:20_sshTest',
        'actionFunc': actorFunctions.func_0920,
        'parallelTH': False,
        'actDetail': 'SSH login to NCL server run cmds',
        'actDesc': 'SSh to the ncl gateway and run commands.'
    }
    addOneAction(action_0920)

    action_0932 = {
        'time': '09:32',
        'name': '09:32_FileSearch',
        'actionFunc': actorFunctions.func_0932,
        'parallelTH': False,
        'actDetail': 'Search User dir to file and files.',
        'actDesc': 'Tree the C: drive and file all the files match the file type.'
    }
    addOneAction(action_0932)

    action_0935 = {
        'time': '09:35',
        'name': '09:35_Zoom',
        'actionFunc': actorFunctions.func_0935,
        'parallelTH': False,
        'actDetail': 'Open the Zoom and join meeting.',
        'actDesc': 'Join and Zoom meeting for 30 mins.'
    }
    addOneAction(action_0935)

    action_1003 = {
        'time': '10:03',
        'name': '10:03_CheckEmail',
        'actionFunc': actorFunctions.func_1003,
        'parallelTH': False,
        'actDetail': 'Check unread email.',
        'actDesc': 'Open Bob inbox and check 6 unread email.'
    }
    addOneAction(action_1003)

    action_1015 = {
        'time': '10:15',
        'name': '10:15_DownloadWeb',
        'actionFunc': actorFunctions.func_1015,
        'parallelTH': False,
        'actDetail': 'Follow urls list to download all the contents.',
        'actDesc': 'Download cert, image, css file , js file from a list of webs.'
    }
    addOneAction(action_1015)


    gv.iScheduler.startSimulate()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
