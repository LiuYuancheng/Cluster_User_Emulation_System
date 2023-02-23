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
