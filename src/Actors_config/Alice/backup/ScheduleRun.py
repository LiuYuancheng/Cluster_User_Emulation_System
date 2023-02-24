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

import actorFunctions
import actionScheduler
from actionScheduler import userAction

ACTOR_NAME = 'Alice[192.168.57.10]'

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
    
    action_0905 = {
        'time': '09:05',
        'name': '09:05_checkEmail',
        'actionFunc': actorFunctions.func_0905,
        'parallelTH': False,
        'actDetail': 'Check new emails',
        'actDesc': 'Open Alice\' mailbox in outlook and read 3 new emails'        
    }
    addOneAction(action_0905)

    action_0920 = {
        'time': '09:20',
        'name': '09:20_YouTube',
        'actionFunc': actorFunctions.func_0920,
        'parallelTH': False,
        'actDetail': 'Play YouTube music videos',
        'actDesc': 'Play 5 YouTube music videos in the background'        
    }    
    addOneAction(action_0920)

    action_0923 = {
        'time': '09:23',
        'name': '09:23_EditMs-Word',
        'actionFunc': actorFunctions.func_0923,
        'parallelTH': False,
        'actDetail': 'Create and edit MS-Word Doc for meeting',
        'actDesc': 'Create meeting.docx file and input meeting details inside'
    }
    addOneAction(action_0923)

    action_1000 = {
        'time': '10:00',
        'name': '10:00_Zoom',
        'actionFunc': actorFunctions.func_1000,
        'parallelTH': False,
        'actDetail': 'Open Zoom and join meeting',
        'actDesc': 'Join Zoom meeting for 2 hrs'
    }
    addOneAction(action_1000)

    action_1300 = {
        'time': '13:00',
        'name': '13:00_EditMs-PowerPoint',
        'actionFunc': actorFunctions.func_1300,
        'parallelTH': False,
        'actDetail': 'Find and edit MS-PPT file',
        'actDesc': 'Create new slides and write some text'
    }
    addOneAction(action_1300)

    action_1500 = {
        'time': '15:00',
        'name': '15:00_Play game',
        'actionFunc': actorFunctions.func_1500,
        'parallelTH': False,
        'actDetail': 'Play google dinosaur game',
        'actDesc': 'Play game for 15 mins'
    }
    addOneAction(action_1500)

    action_1515 = {
        'time': '15:15',
        'name': '15:15_Webdownload',
        'actionFunc': actorFunctions.func_1515,
        'parallelTH': False,
        'actDetail': 'Click some links in a online shopping website',
        'actDesc': 'Visit online shopping website and randomly click some links'
    }
    addOneAction(action_1515)

    action_1545 = {
        'time': '15:45',
        'name': '15:45_DownloadWeb',
        'actionFunc': actorFunctions.func_1545,
        'parallelTH': False,
        'actDetail': 'Follow urls list to download all the contents.',
        'actDesc': 'Download pictures from website such as Unsplash'
    }
    addOneAction(action_1545)

    action_1600 = {
        'time': '16:00',
        'name': '16:00_checkEmail',
        'actionFunc': actorFunctions.func_1600,
        'parallelTH': False,
        'actDetail': 'Write and reply emails',
        'actDesc': 'Write and reply 2 emails in Alice\' mailbox'
    }
    addOneAction(action_1600)

    action_1700 = {
        'time': '17:00',
        'name': '17:00_Telegram',
        'actionFunc': actorFunctions.func_1700,
        'parallelTH': False,
        'actDetail': 'Open Telegram and send messages to chats',
        'actDesc': 'Open Telegram to send messages to chat contacts'
    }
    addOneAction(action_1700)

    action_1715 = {
        'time': '17:15',
        'name': '17:15_SearchWeb',
        'actionFunc': actorFunctions.func_1015,
        'parallelTH': False,
        'actDetail': 'Research some information for slides proposal',
        'actDesc': 'Run WebScreenShoter.py to perform web access and perform random click action.'
    }
    addOneAction(action_1715)

    action_1735 = {
        'time': '17:35',
        'name': '17:35_EditMs-Word',
        'actionFunc': actorFunctions.func_1735,
        'parallelTH': False,
        'actDetail': 'Find and continue edit MS-Word doc',
        'actDesc': 'Open meeting.docx created this morning and write some text'
    }
    addOneAction(action_1735)

    gv.iScheduler.startSimulate()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
