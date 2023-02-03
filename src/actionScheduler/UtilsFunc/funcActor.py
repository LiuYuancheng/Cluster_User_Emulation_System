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
from selenium import webdriver
import datetime

CHROME_DRI = 'chromedriver.exe'

#-----------------------------------------------------------------------------
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

#-----------------------------------------------------------------------------
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

#-----------------------------------------------------------------------------
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

#-----------------------------------------------------------------------------
def selectFile(filePath):
    """ open the file explore directory and select the file.
    """
    if os.path.exists(filePath):
        opencmd = [
            {   'cmdID': 'selectFile',
                'console': False,
                'cmdStr': 'explorer /select, %s' %str(filePath),
                'winShell': True,
                'repeat': 1,
                'interval': 1
            },
        ]
        runWinCmds(opencmd, rstRecord=False)
        return True
    else:
        print("The file needs to be selected is not exist!")
        return False

#-----------------------------------------------------------------------------
def scpFile(filePath, dest, password, port=22,):
    """ Open a terminal and scp the file to server.
    """
    if selectFile(filePath):
        portSpc = ' -P %s' %str(port) if port == 2 else ''
        scpCmd = "scp%s %s %s" %(portSpc, str(filePath), str(dest))
        #"scp -P 3022 "C:\Works\NCL\Project\Windows_User_Simulator\src\UtilsFunc\pic.png" ncl_intern@gateway.ncl.sg:~/pic.png"
        # print(scpCmd)
        # cmdList = [
        #     {   'cmdID': 'scpFile',
        #         'console': False,
        #         'cmdStr': scpCmd,
        #         'winShell': False,
        #         'repeat': 1,
        #         'interval': 5   # make the time interval longer to wait the ssh connection ready
        #     },
        # ]
        # runWinCmds(cmdList, rstRecord=False)
        time.sleep(5)
        print("here")
        #simuUserType(password)
        keyboard.press_and_release('alt+f4')
    else:
        print("The file needs to be scp is not exist!")
        return False

#-----------------------------------------------------------------------------
def simuUserType(typeinStr):
    """ Simulate user type in a string
    """
    for char in typeinStr:
        if char == '\n' :
            keyboard.press_and_release('enter')
        elif char == ' ':
            keyboard.press_and_release('space')
        elif char == '@':
            keyboard.press_and_release('shift+2')
        else:
            keyboard.press_and_release(char)
        time.sleep(0.2)

#-----------------------------------------------------------------------------
def msPPTedit(filePath, actionDict):
    if os.path.exists(filePath):
        # copy the needed picture in clipboard        
        if 'picName'in  actionDict.keys() and os.path.exists(actionDict['picName']):
            selectFile(actionDict['picName'])
            keyboard.press_and_release('ctrl+c')
            time.sleep(actionDict['interval'])
            keyboard.press_and_release('alt+f4')
            time.sleep(actionDict['interval'])
        startFile(filePath)
        time.sleep(actionDict['interval']*3) # wait office start the word doc.
        keyboard.press_and_release('ctrl+shift+m')
        time.sleep(0.5)
        keyboard.press_and_release('enter')
        time.sleep(0.5)
        # Edit the title:
        simuUserType(actionDict['title'])
        time.sleep(int(actionDict['interval']))
        keyboard.press_and_release('esc')
        keyboard.press_and_release('tab')
        time.sleep(actionDict['interval'])
        simuUserType(actionDict['body'])
        time.sleep(actionDict['interval'])
        # close and save the file
        keyboard.press_and_release('ctrl+v')
        time.sleep(2)
        # close the word doc.
        keyboard.press_and_release('alt+f4')
        time.sleep(1)
        keyboard.press_and_release('enter')
        time.sleep(1)
        # close the ppt folder
        keyboard.press_and_release('alt+f4')
    else:
        print("The file %s need to be editted is not exist." %str(filePath))

#-----------------------------------------------------------------------------
class webActor(object):

    def __init__(self, driverPath=None) -> None:
        dirpath = os.path.dirname(__file__)
        chromeDriverPath = driverPath if driverPath else os.path.join(dirpath, CHROME_DRI)
        self.driver = webdriver.Chrome(executable_path=chromeDriverPath)
        self.startT = 0

    def openUrls(self, urlConfig):
        try:
            self.driver.get(urlConfig['url'])
        except Exception as err:
            print('Ignore some internet not access exception %s' %str(err))
        time.sleep(urlConfig['interval'])
    
    def closeBrowser(self):
        self.driver.quit()
