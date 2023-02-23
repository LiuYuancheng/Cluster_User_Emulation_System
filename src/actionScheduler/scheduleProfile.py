#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        scheduleProfile.py
#
# Purpose:     A profile template to define a user's action story timeline.
#
# Author:      Yuancheng Liu
#
# Version:     v_0.2
# Created:     2023/02/23
# Copyright:   n.a
# License:     n.a
#-----------------------------------------------------------------------------

import datetime
import actionGlobal as gv
import actorFunctions

ACTOR_NAME = 'Bob[192.168.57.10]'

dailyTaskList = []
randomTaskList = []
weeklyTaskList = []

# Example for defining a daily action which will run on 09:01 am very day.
action_0901 = {
    'time': '09:01',
    'name': '09:01_ping',
    'actionFunc': actorFunctions.func_0901,
    'parallelTH': False,
    'actDetail': 'Ping 30 destinations',
    'actDesc': 'Ping an internal servers list to check the server connection.',
    'actOwner': 'admin:LYC'
}

dailyTaskList.append(action_0901)

action_0910 = {
    'time': '09:10',
    'name': '09:10_ping[MT]',
    'actionFunc': actorFunctions.func_0901,
    'parallelTH': True,
    'actDetail': 'Ping 100+ destinations',
    'actDesc': 'Ping an external servers list to check the server connection.'
}
dailyTaskList.append(action_0910)

action_0913 = {
    'time': '09:13',
    'name': '09:13_cmdRun',
    'actionFunc': actorFunctions.func_0913,
    'parallelTH': False,
    'actDetail': 'Run Win_Network cmds',
    'actDesc': 'Run Windows network routing cmds.'
}
dailyTaskList.append(action_0913)

action_0920 = {
    'time': '09:20',
    'name': '09:20_sshTest',
    'actionFunc': actorFunctions.func_0920,
    'parallelTH': False,
    'actDetail': 'SSH login to NCL server run cmds',
    'actDesc': 'SSh to the ncl gateway and run commands.'
}
dailyTaskList.append(action_0920)

action_0932 = {
    'time': '09:32',
    'name': '09:32_FileSearch',
    'actionFunc': actorFunctions.func_0932,
    'parallelTH': False,
    'actDetail': 'Search User dir to file and files.',
    'actDesc': 'Tree the C: drive and file all the files match the file type.'
}
dailyTaskList.append(action_0932)

action_0935 = {
    'time': '09:35',
    'name': '09:35_Zoom',
    'actionFunc': actorFunctions.func_0935,
    'parallelTH': False,
    'actDetail': 'Open the Zoom and join meeting.',
    'actDesc': 'Join and Zoom meeting for 30 mins.'
}
dailyTaskList.append(action_0935)

action_1003 = {
    'time': '10:03',
    'name': '10:03_CheckEmail',
    'actionFunc': actorFunctions.func_1003,
    'parallelTH': False,
    'actDetail': 'Check unread email.',
    'actDesc': 'Open Bob inbox and check 6 unread email.'
}
dailyTaskList.append(action_1003)

action_1015 = {
    'time': '10:15',
    'name': '10:15_DownloadWeb',
    'actionFunc': actorFunctions.func_1015,
    'parallelTH': False,
    'actDetail': 'Follow urls list to download all the contents.',
    'actDesc': 'Download cert, image, css file , js file from a list of webs.'
}
dailyTaskList.append(action_1015)

action_1032 = {
    'time': '10:32',
    'name': '10:32_YouTube',
    'actionFunc': actorFunctions.func_1032,
    'parallelTH': False,
    'actDetail': 'Watch some youTube videos',
    'actDesc': ' Watch 5 YouTube videos'
}
dailyTaskList.append(action_1032)

action_1050 = {
    'time': '10:50',
    'name': '10:50_EditMs-Word',
    'actionFunc': actorFunctions.func_1050,
    'parallelTH': False,
    'actDetail': 'Create and edit MS-Word Doc.',
    'actDesc': 'Create the Report.docx file and write some thing in it.'
}
dailyTaskList.append(action_1050)

action_1125 = {
    'time': '11:25',
    'name': '11:25_EditMs-PowerPoint',
    'actionFunc': actorFunctions.func_1125,
    'parallelTH': False,
    'actDetail': 'Create and edit MS-PPT Doc.',
    'actDesc': 'Create the Report.pptx file and write some thing in it.'
}
dailyTaskList.append(action_1125)

action_1135 = {
    'time': '11:35',
    'name': '11:35_PlayGame',
    'actionFunc': actorFunctions.func_1135,
    'parallelTH': False,
    'actDetail': 'Open Chrome and play Dino Game.',
    'actDesc': 'Play google dinosaur jump game for 30 mins.'
}
dailyTaskList.append(action_1135)

action_1310 = {
    'time': '13:10',
    'name': '13:10_Ping_subnet2',
    'actionFunc': actorFunctions.func_1310,
    'parallelTH': False,
    'actDetail': 'Ping ip addresses in subnet2',
    'actDesc': 'Ping another 100 ip addresses in subnet2.'
}
dailyTaskList.append(action_1310)

action_1345 = {
    'time': '13:35',
    'name': '13:45_SSH_subnet2',
    'actionFunc': actorFunctions.func_1345,
    'parallelTH': False,
    'actDetail': 'SSH to hosts in subnet2',
    'actDesc': 'SSH to pingable host in subnet2.'
}
dailyTaskList.append(action_1345)

action_1410 = {
    'time': '14:10',
    'name': '14:10_TrunOff_FW',
    'actionFunc': actorFunctions.func_1410,
    'parallelTH': False,
    'actDetail': 'Turn off Windows FW.',
    'actDesc': 'Turn off the windows privcate network FW'
}
dailyTaskList.append(action_1410)

action_1430 = {
    'time': '14:30',
    'name': '14:30_Webdownload',
    'actionFunc': actorFunctions.func_1430,
    'parallelTH': False,
    'actDetail': 'Download some thing from webs dict',
    'actDesc': 'Follow urls list to download all the contents'
}
dailyTaskList.append(action_1430)

action_1450 = {
    'time': '14:50',
    'name': '14:50_UDP communication',
    'actionFunc': actorFunctions.func_1450,
    'parallelTH': False,
    'actDetail': 'Send message/file by UDP',
    'actDesc': 'Send randome UDP package, each package is about 400KB'
}
dailyTaskList.append(action_1450)

action_1515 = {
    'time': '15:15',
    'name': '15:15_EditMs-PowerPoint',
    'actionFunc': actorFunctions.func_1515,
    'parallelTH': False,
    'actDetail': 'Find and edit MS-PPT Doc',
    'actDesc': 'Find the Report.pptx file and write some thing in it.'
}
dailyTaskList.append(action_1515)

action_1520 = {
    'time': '15:20',
    'name': '15:20_Play game',
    'actionFunc': actorFunctions.func_1520,
    'parallelTH': False,
    'actDetail': 'Play a game',
    'actDesc': 'Play google dinosaur jump game for 10 mins.'
}
dailyTaskList.append(action_1520)

action_1540 = {
    'time': '15:40',
    'name': '15:40_SendEmail',
    'actionFunc': actorFunctions.func_1540,
    'parallelTH': False,
    'actDetail': 'Send emails',
    'actDesc': 'Send 30 emails to other people.'
}
dailyTaskList.append(action_1540)

action_1600 = {
    'time': '16:00',
    'name': '16:00_WatchVideo',
    'actionFunc': actorFunctions.func_1600,
    'parallelTH': False,
    'actDetail': 'Open a video file.',
    'actDesc': 'Look for video file and open.'
}
dailyTaskList.append(action_1600)

action_1635 = {
    'time': '16:35',
    'name': '16:35_CheckPictures',
    'actionFunc': actorFunctions.func_1635,
    'parallelTH': False,
    'actDetail': 'Check pictures in folder.',
    'actDesc': 'Look for picture file and open.'
}
dailyTaskList.append(action_1635)

action_1700 = {
    'time': '17:00',
    'name': '17:00_UDP communication',
    'actionFunc': actorFunctions.func_1450,
    'parallelTH': False,
    'actDetail': 'Send message/file by UDP.',
    'actDesc': 'Send randome UDP package, each package is about 400KB'
}
dailyTaskList.append(action_1700)

action_1735 = {
    'time': '17:35',
    'name': '17:35_Write Report',
    'actionFunc': actorFunctions.func_1050,
    'parallelTH': False,
    'actDetail': 'Bob finished his report.',
    'actDesc': 'Open the report.docx and edit'
}
dailyTaskList.append(action_1735)


# Example for defining a randome action: print time randomely every half min. 
action_rand = {
    'name': 'random_print_time ',
    'randomInt': (5, 10),
    'actionFunc': lambda: print(datetime.datetime.now()),
    'parallelTH': True,
    'actDetail': 'just a print',
    'actDesc': 'Print the time in a time period to test the randome task.',
    'actOwner': 'admin:LYC'
}
randomTaskList.append(action_rand)

# Example for defining a week action: print date every Monday and Sunday at 17:35
action_weekly = {
    'name': 'weekly_print_date',
    'weeklist': [1, 7],
    'time': '17:35',
    'actionFunc': lambda: print(datetime.datetime.today()),
    'parallelTH': True,
    'actDetail': 'just a print',
    'actDesc': 'Print the date on Mon and Sun.',
    'actOwner': 'admin:LYC'
}
weeklyTaskList.append(action_weekly)
