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

ACTOR_NAME = 'Bob[192.168.57.10]'

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

    action_1032 = {
        'time': '10:32',
        'name': '10:32_YouTube',
        'actionFunc': actorFunctions.func_1032,
        'parallelTH': False,
        'actDetail': 'Watch some youTube videos',
        'actDesc': ' Watch 5 YouTube videos'
    }
    addOneAction(action_1032)

    action_1050 = {
        'time': '10:50',
        'name': '10:50_EditMs-Word',
        'actionFunc': actorFunctions.func_1050,
        'parallelTH': False,
        'actDetail': 'Create and edit MS-Word Doc.',
        'actDesc': 'Create the Report.docx file and write some thing in it.'
    }
    addOneAction(action_1050)

    action_1125 = {
        'time': '11:25',
        'name': '11:25_EditMs-PowerPoint',
        'actionFunc': actorFunctions.func_1125,
        'parallelTH': False,
        'actDetail': 'Create and edit MS-PPT Doc.',
        'actDesc': 'Create the Report.pptx file and write some thing in it.'
    }
    addOneAction(action_1125)

    action_1135 = {
        'time': '11:35',
        'name': '11:35_PlayGame',
        'actionFunc': actorFunctions.func_1135,
        'parallelTH': False,
        'actDetail': 'Open Chrome and play Dino Game.',
        'actDesc': 'Play google dinosaur jump game for 30 mins.'
    }
    addOneAction(action_1135)

    action_1310 = {
        'time': '13:10',
        'name': '13:10_Ping_subnet2',
        'actionFunc': actorFunctions.func_1310,
        'parallelTH': False,
        'actDetail': 'Ping ip addresses in subnet2',
        'actDesc': 'Ping another 100 ip addresses in subnet2.'
    }
    addOneAction(action_1310)

    action_1345 = {
        'time': '13:35',
        'name': '13:45_SSH_subnet2',
        'actionFunc': actorFunctions.func_1345,
        'parallelTH': False,
        'actDetail': 'SSH to hosts in subnet2',
        'actDesc': 'SSH to pingable host in subnet2.'
    }
    addOneAction(action_1345)

    action_1410 = {
        'time': '14:10',
        'name': '14:10_TrunOff_FW',
        'actionFunc': actorFunctions.func_1410,
        'parallelTH': False,
        'actDetail': 'Turn off Windows FW.',
        'actDesc': 'Turn off the windows privcate network FW'
    }
    addOneAction(action_1410)

    action_1430 = {
        'time': '14:30',
        'name': '14:30_Webdownload',
        'actionFunc': actorFunctions.func_1430,
        'parallelTH': False,
        'actDetail': 'Download some thing from webs dict',
        'actDesc': 'Follow urls list to download all the contents'
    }
    addOneAction(action_1430)

    action_1450 = {
        'time': '14:50',
        'name': '14:50_UDP communication',
        'actionFunc': actorFunctions.func_1450,
        'parallelTH': False,
        'actDetail': 'Send message/file by UDP',
        'actDesc': 'Send randome UDP package, each package is about 400KB'
    }
    addOneAction(action_1450)
    
    action_1515 = {
        'time': '15:15',
        'name': '15:15_EditMs-PowerPoint',
        'actionFunc': actorFunctions.func_1515,
        'parallelTH': False,
        'actDetail': 'Find and edit MS-PPT Doc',
        'actDesc': 'Find the Report.pptx file and write some thing in it.'
    }
    addOneAction(action_1515)

    action_1520 = {
        'time': '15:20',
        'name': '15:20_Play game',
        'actionFunc': actorFunctions.func_1520,
        'parallelTH': False,
        'actDetail': 'Play a game',
        'actDesc': 'Play google dinosaur jump game for 10 mins.'
    }
    addOneAction(action_1520)

    action_1540 = {
        'time': '15:40',
        'name': '15:40_SendEmail',
        'actionFunc': actorFunctions.func_1540,
        'parallelTH': False,
        'actDetail': 'Send emails',
        'actDesc': 'Send 30 emails to other people.'
    }
    addOneAction(action_1540)

    action_1600 = {
        'time': '16:00',
        'name': '16:00_WatchVideo',
        'actionFunc': actorFunctions.func_1600,
        'parallelTH': False,
        'actDetail': 'Open a video file.',
        'actDesc': 'Look for video file and open.'
    }
    addOneAction(action_1600)

    action_1635 = {
        'time': '16:35',
        'name': '16:35_CheckPictures',
        'actionFunc': actorFunctions.func_1635,
        'parallelTH': False,
        'actDetail': 'Check pictures in folder.',
        'actDesc': 'Look for picture file and open.'
    }
    addOneAction(action_1635)

    action_1700 = {
        'time': '17:00',
        'name': '17:00_UDP communication',
        'actionFunc': actorFunctions.func_1450,
        'parallelTH': False,
        'actDetail': 'Send message/file by UDP.',
        'actDesc': 'Send randome UDP package, each package is about 400KB'
    }
    addOneAction(action_1700)

    action_1735 = {
        'time': '17:35',
        'name': '17:35_Write Report',
        'actionFunc': actorFunctions.func_1050,
        'parallelTH': False,
        'actDetail': 'Bob finished his report.',
        'actDesc': 'Open the report.docx and edit'
    }
    addOneAction(action_1735)

    gv.iScheduler.startSimulate()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
