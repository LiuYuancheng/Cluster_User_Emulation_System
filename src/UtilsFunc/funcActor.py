#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        funcActor.py
#
# Purpose:     This module will prvoide different individual actor function/class
#              for the action schedular.
#
# Author:      Yuancheng Liu
#
# Version:     v_0.1
# Created:     2022/10/12
# Copyright:   n.a
# License:     n.a
#-----------------------------------------------------------------------------

import os
import time
import json
import subprocess
import keyboard

def runCmd(cmdStr, showConsole=False, winShell=False):
    try:
        if showConsole:
            result = subprocess.call(cmdStr, shell=winShell, creationflags=subprocess.CREATE_NEW_CONSOLE)
            return result
        else:
            result = subprocess.run(cmdStr, shell=winShell, stdout=subprocess.PIPE)
            return result.stdout.decode('utf-8')
    except Exception as err:
        print("Cmd %s \n Execution error: %s" % (cmdStr, str(err)))
        return None

def runWinCmds(cmdConfig, rstRecord=False):
    cmdList = None
    resultDict = {} if rstRecord else None
    if isinstance(cmdConfig, list):
        cmdList = cmdConfig
    elif isinstance(cmdConfig, str):
        if os.path.exists(cmdConfig):
            try:
                with open(cmdConfig, 'r') as fh:
                    cmdList = json.load(fh)
            except Exception as err:
                print("Failed to load the json config file: %s" %str(err))
                return None
    else: 
        print('The input <config> file/parameter is not valid.')
        return None
    # execute the cmds
    for item in cmdList:
        for _ in range(int(item['repeat'])):
            shell = True if 'winShell' in item.keys() else False
            rst = runCmd(item['cmdStr'], showConsole=item['console'], winShell=shell)
            if rstRecord: resultDict[str(item['cmdID'])] = rst
            time.sleep(float(item['interval']))
        print("Finish execute cmd with ID: %s" %str(item['cmdID']))
    
    return resultDict

def startFile(filePath):
    dirPath, fileName = os.path.split(filePath)
    print(dirPath)
    opencmd = [
        {   'cmdID': 'cmd_1',
            'console': False,
            'cmdStr': 'start %s' %str(dirPath),
            'winShell': True,
            'repeat': 1,
            'interval': 1
        },

        {   'cmdID': 'cmd_2',
            'console': False,
            'cmdStr': 'start %s' %str(filePath),
            'winShell': True,
            'repeat': 1,
            'interval': 0.8
        }
    ]
    runWinCmds(opencmd, rstRecord=False)

def testCase(mode):

    if mode == 1:
        runCmd('ping -n 5 www.google.com.sg', showConsole=True)
        print('**')
        rst = runCmd('ping -n 5 www.google.com.sg', showConsole=False)
        print(rst)
        rst = runCmd('ipconfig', showConsole=False)
        print(rst)
    elif mode == 2:
        cmdsList = [
            {   'cmdID': 'cmd_1',
                'console': True,
                'cmdStr': 'ping -n 5 www.google.com.sg',
                'repeat': 1,
                'interval': 0.8
            },
            {   'cmdID': 'cmd_2',
                'console': False,
                'cmdStr': 'ipconfig', #'DIR C:\\Works',
                'repeat': 1,
                'interval': 0.8
            },
            {   'cmdID': 'cmd_3',
                'console': False,
                'cmdStr': 'dir C:\\Works',
                'winShell': True,
                'repeat': 1,
                'interval': 0.8
            }
        ] 
        result = runWinCmds(cmdsList, rstRecord=True)
        print(result)
    elif mode == 3:
        dirPath = os.path.dirname(__file__)
        configPath = os.path.join(dirPath, 'cmdTest.json')
        result = runWinCmds(configPath, rstRecord=True)
        print(result)
    elif mode == 4:
        filePath = "C:\\Works\\NCL\\Project\\Windows_User_Simulator\\src\\UtilsFunc\\Report.docx"
        startFile(filePath)
        time.sleep(3) # wait office start the word doc.
        InputStr = "i am bob, every day i need to write a report, \n feel so boring!"
        for char in InputStr:
            if char == '\n' :
                keyboard.press_and_release('enter')
            elif char == ' ':
                keyboard.press_and_release('space')
            else:
                keyboard.press_and_release(char)
            time.sleep(0.3)
        # close the word doc.
        keyboard.press_and_release('alt+f4')
        time.sleep(1)
        keyboard.press_and_release('enter')
    
    elif mode == 5:
        # Edit a ppt file:
        time.sleep(3)
        cmdsList = [
            {   'cmdID': 'cmd_0',
                'console': False,
                'cmdStr': 'explorer /select, C:\\Works\\NCL\\Project\\Windows_User_Simulator\\src\\UtilsFunc\\pic.png',
                'winShell': True,
                'repeat': 1,
                'interval': 0.8
            },
        ]
        runWinCmds(cmdsList, rstRecord=False)
        time.sleep(2)
        keyboard.press_and_release('ctrl+c')
        time.sleep(1)
        keyboard.press_and_release('alt+f4')
        filePath = "C:\\Works\\NCL\\Project\\Windows_User_Simulator\\src\\UtilsFunc\\Report.pptx"
        startFile(filePath)
        time.sleep(3) # wait office start the word doc.
        keyboard.press_and_release('ctrl+shift+m')
        time.sleep(0.5)
        keyboard.press_and_release('enter')
        InputStr = "i am bob, every day i need to write a report, \n feel so boring!"
        for char in InputStr:
            if char == '\n' :
                keyboard.press_and_release('enter')
            elif char == ' ':
                keyboard.press_and_release('space')
            else:
                keyboard.press_and_release(char)
            time.sleep(0.3)
        keyboard.press_and_release('esc')
        keyboard.press_and_release('tab')
        InputStr = "but I have to do this, now let me pause my current working project ui here."
        for char in InputStr:
            if char == '\n' :
                keyboard.press_and_release('enter')
            elif char == ' ':
                keyboard.press_and_release('space')
            else:
                keyboard.press_and_release(char)
            time.sleep(0.3)

        keyboard.press_and_release('ctrl+v')
        time.sleep(2)
        # close the word doc.
        keyboard.press_and_release('alt+f4')
        time.sleep(1)
        keyboard.press_and_release('enter')

if __name__ == '__main__':
    testCase(5)
