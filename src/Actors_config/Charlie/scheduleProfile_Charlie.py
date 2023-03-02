#!/usr/bin/python
# -----------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------

import datetime
import actionGlobal as gv
import actorFunctionsAlice as actorFunctions

ACTOR_NAME = "Charlie[192.168.57.10]"

dailyTaskList = []
randomTaskList = []
weeklyTaskList = []

# Example for defining a daily action which will run on 09:01 am very day.
action_0900 = {
    "time": "09:00",
    "name": "09:00_checkEmail",
    "actionFunc": actorFunctions.func_0900,
    "parallelTH": False,
    "actDetail": "Check new emails to obtain project details and clients' deadlines",
    "actDesc": "Open Charlie's mailbox in outlook and read 5 new emails",
}
dailyTaskList.append(action_0900)

action_0915 = {
    "time": "09:15",
    "name": "09:15_EditMs-Word",
    "actionFunc": actorFunctions.func_0915,
    "parallelTH": False,
    "actDetail": "Create and edit MS-Word Doc to note tasks for the day",
    "actDesc": "Create to-do.docx file and input tasks for the day",
}
dailyTaskList.append(action_0915)

action_0925 = {
    "time": "09:25",
    "name": "09:23_ping",
    "actionFunc": actorFunctions.func_0925,
    "parallelTH": False,
    "actDetail": "",
    "actDesc": "Ping for connectivity of target ip address",
}
dailyTaskList.append(action_0925)

action_0927 = {
    "time": "10:00",
    "name": "10:00_Webdownload",
    "actionFunc": actorFunctions.func_0927,
    "parallelTH": False,
    "actDetail": "Perform web search and download information from target client",
    "actDesc": "Perform web search and download information from target client",
}
dailyTaskList.append(action_0927)

action_0932 = {
    "time": "09:32",
    "name": "09:32_Googlesearch",
    "actionFunc": actorFunctions.func_0932,
    "parallelTH": False,
    "actDetail": "Visit whois.com to enumerate on ip address",
    "actDesc": "",
}
dailyTaskList.append(action_0932)

action_0940 = {
    "time": "09:40",
    "name": "09:40_Googlesearch",
    "actionFunc": actorFunctions.func_0940,
    "parallelTH": False,
    "actDetail": "Visit robtex.com/dns-lookup/ to enumerate on ip address",
    "actDesc": "",
}
dailyTaskList.append(action_0940)

action_0945 = {
    "time": "09:45",
    "name": "09:45_EditMs-Word",
    "actionFunc": actorFunctions.func_0945,
    "parallelTH": False,
    "actDetail": "Record down information gathered into the word docx",
    "actDesc": "",
}
dailyTaskList.append(action_0945)

action_1000 = {
    "time": "10:00",
    "name": "09:45_Nmap",
    "actionFunc": actorFunctions.func_1000,
    "parallelTH": False,
    "actDetail": "Execute Nmap (nmap -sC -sV <ip>)",
    "actDesc": "Execute Nmap to find target address's open ports and vulnerabilities",
}
dailyTaskList.append(action_1000)

action_1010 = {
    "time": "10:10",
    "name": "10:10_Gobuster",
    "actionFunc": actorFunctions.func_1010,
    "parallelTH": False,
    "actDetail": "Execute Gobuster (gobuster -u <target-url> -w \)",
    "actDesc": "Perform subdomain web enumeration using Gobuster",
}
dailyTaskList.append(action_1010)

action_1015 = {
    "time": "10:15",
    "name": "10:15_Googlesearch",
    "actionFunc": actorFunctions.func_1015,
    "parallelTH": False,
    "actDetail": "Perform google search on target client (port 443 exploit)",
    "actDesc": "",
}
dailyTaskList.append(action_1015)

action_1030 = {
    "time": "10:30",
    "name": "10:30_Zoom",
    "actionFunc": actorFunctions.func_1030,
    "parallelTH": False,
    "actDetail": "Open the Zoom and join meeting.",
    "actDesc": "Join and Zoom meeting for 30 mins.",
}
dailyTaskList.append(action_1030)

action_1300 = {
    "time": "13:00",
    "name": "13:00_Sqlmap",
    "actionFunc": actorFunctions.func_1300,
    "parallelTH": False,
    "actDetail": 'sqlmap -u "target address url" --cookie="" --schema --columns --bath',
    "actDesc": "Run sqlmap using os.subprocess()",
}
dailyTaskList.append(action_1300)

action_1320 = {
    "time": "13:20",
    "name": "13:20_Googlesearch",
    "actionFunc": actorFunctions.func_1320,
    "parallelTH": False,
    "actDetail": "Visit https://gchq.github.io/CyberChef/",
    "actDesc": "Create webActor object",
}
dailyTaskList.append(action_1320)

action_1325 = {
    "time": "13:25",
    "name": "13:25_SSH",
    "actionFunc": actorFunctions.func_1325,
    "parallelTH": False,
    "actDetail": "SSH to open port using cracked credentials from DB",
    "actDesc": "SSH username@ip",
}
dailyTaskList.append(action_1325)

action_1330 = {
    "time": "13:30",
    "name": "13:30_Syscommands",
    "actionFunc": actorFunctions.func_1330,
    "parallelTH": False,
    "actDetail": 'Run "sudo -l" to check for sudo privileges',
    "actDesc": "os.subprocess()",
}
dailyTaskList.append(action_1330)

action_1335 = {
    "time": "13:35",
    "name": "13:35_Googlesearch",
    "actionFunc": actorFunctions.func_1335,
    "parallelTH": False,
    "actDetail": "Visit https://book.hacktricks.xyz/",
    "actDesc": "Create webActor object",
}
dailyTaskList.append(action_1335)

action_1345 = {
    "time": "13:45",
    "name": "13:45_Googlesearch",
    "actionFunc": actorFunctions.func_1345,
    "parallelTH": False,
    "actDetail": "Visit https://gtfobins.github.io/",
    "actDesc": "Create webActor object",
}
dailyTaskList.append(action_1345)

action_1400 = {
    "time": "14:00",
    "name": "14:00_YouTube",
    "actionFunc": actorFunctions.func_1400,
    "parallelTH": False,
    "actDetail": "Watch some youTube videos",
    "actDesc": " Watch 3 YouTube videos",
}
dailyTaskList.append(action_1400)

action_1415 = {
    "time": "14:15",
    "name": "14:15_webDownload",
    "actionFunc": actorFunctions.func_1415,
    "parallelTH": False,
    "actDetail": "Web download winPEAS from https://github.com/carlospolop/PEASS-ng/releases/download/20230212/winPEASx64.exe",
    "actDesc": " webDownload.py",
}
dailyTaskList.append(action_1415)

action_1425 = {
    "time": "14:25",
    "name": "14:25_Transferfile",
    "actionFunc": actorFunctions.func_1425,
    "parallelTH": False,
    "actDetail": 'os.subprocess("python -m SimpleHTTPServer 80")',
    "actDesc": "Transfer winPEAS file over to target computer",
}
dailyTaskList.append(action_1425)

action_1430 = {
    "time": "14:30",
    "name": "14:30_Googlesearch",
    "actionFunc": actorFunctions.func_1430,
    "parallelTH": False,
    "actDetail": "Visit exploit-db.com to download exploit",
    "actDesc": "webDownload.py",
}
dailyTaskList.append(action_1430)

action_1435 = {
    "time": "14:35",
    "name": "14:35_Syscommands",
    "actionFunc": actorFunctions.func_1435,
    "parallelTH": False,
    "actDetail": 'Execute os.subprocess("searchsploit windows")',
    "actDesc": "",
}
dailyTaskList.append(action_1435)

action_1440 = {
    "time": "14:40",
    "name": "14:40_Syscommands",
    "actionFunc": actorFunctions.func_1440,
    "parallelTH": False,
    "actDetail": 'Execute os.subprocess("msfvenom")',
    "actDesc": "",
}
dailyTaskList.append(action_1440)

action_1450 = {
    "time": "14:50",
    "name": "14:50_EditMs-Word",
    "actionFunc": actorFunctions.func_1450,
    "parallelTH": False,
    "actDetail": "Create and edit MS-Word Doc to document findings for pentest",
    "actDesc": "Create pentest.docx file and input findings",
}
dailyTaskList.append(action_1450)

action_1520 = {
    "time": "15:20",
    "name": "15:20_EditMs-PowerPoint",
    "actionFunc": actorFunctions.func_1520,
    "parallelTH": False,
    "actDetail": "Create and edit MS-PPT Doc.",
    "actDesc": "Create the Pentest.pptx file and document findings.",
}
dailyTaskList.append(action_1520)

action_1620 = {
    "time": "16:20",
    "name": "16:20_Zoom",
    "actionFunc": actorFunctions.func_1620,
    "parallelTH": False,
    "actDetail": "Open the Zoom and join meeting.",
    "actDesc": "Join and Zoom meeting for 1hr 40mins to end of work",
}
dailyTaskList.append(action_1620)

# Example for defining a randome action: print time randomely every half min.
action_rand = {
    "name": "random_print_time ",
    "randomInt": (5, 10),
    "actionFunc": lambda: print(datetime.datetime.now()),
    "parallelTH": True,
    "actDetail": "just a print",
    "actDesc": "Print the time in a time period to test the randome task.",
    "actOwner": "admin:LYC",
}
# randomTaskList.append(action_rand)

# Example for defining a week action: print date every Monday and Sunday at 17:35
action_weekly = {
    "name": "weekly_print_date",
    "weeklist": [1, 7],
    "time": "17:35",
    "actionFunc": lambda: print(datetime.datetime.today()),
    "parallelTH": True,
    "actDetail": "just a print",
    "actDesc": "Print the date on Mon and Sun.",
    "actOwner": "admin:LYC",
}
# weeklyTaskList.append(action_weekly)
