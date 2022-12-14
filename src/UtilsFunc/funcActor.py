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

#-----------------------------------------------------------------------------
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
        # cmdsList = [
        #     {   'cmdID': 'cmd_0',
        #         'console': False,
        #         'cmdStr': 'explorer /select, C:\\Works\\NCL\\Project\\Windows_User_Simulator\\src\\UtilsFunc\\pic.png',
        #         'winShell': True,
        #         'repeat': 1,
        #         'interval': 0.8
        #     },
        # ]
        # runWinCmds(cmdsList, rstRecord=False)
        # time.sleep(2)
        selectFile("C:\\Works\\NCL\\Project\\Windows_User_Simulator\\src\\UtilsFunc\\pic.png")
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

    elif  mode == 6:
        scpFilePath = "C:\\Works\\NCL\\Project\\Windows_User_Simulator\\src\\UtilsFunc\\pic.png"
        dest = "ncl_intern@gateway.ncl.sg:~/pic.png"
        password =  None
        scpFile(scpFilePath, dest, password)

    elif mode == 7:
        # watch a YouTube video
        urlActor = webActor()
        urlitem = {
            'cmdID': 'YouTube',
            'url': 'https://www.youtube.com/watch?v=VMebB6hhjW4',
            'interval': 3,
        }
        urlActor.openUrls(urlitem)
        keyboard.press_and_release('page down')
        time.sleep(1)
        keyboard.press_and_release('page up')
        time.sleep(1)
        keyboard.press_and_release('space')
        time.sleep(10)
        urlActor.closeBrowser()

    elif mode == 8:
        urlActor = webActor()
        urlitem = {
            'cmdID': 'gmail',
            'url': 'https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox',
            'interval': 3,
        }
        urlActor.openUrls(urlitem)
        emailAddress = 'yuancheng@ncl.sg'
        simuUserType(emailAddress)
        time.sleep(0.5)
        keyboard.press_and_release('enter')
        time.sleep(3)
        password = '618827lyc'
        simuUserType(password)
        time.sleep(0.5)
        keyboard.press_and_release('enter')
        # enable the "allow program activity"
        time.sleep(3)
        keyboard.press_and_release('tab')
        time.sleep(1)
        keyboard.press_and_release('tab')
        time.sleep(1)
        keyboard.press_and_release('enter')
        # pres the down button the check the email
        time.sleep(0.5)
        keyboard.press_and_release('down')
        time.sleep(0.5)
        keyboard.press_and_release('down')

        urlitem = {
            'cmdID': 'gmail',
            'url': 'https://mail.google.com/mail/u/0/#inbox/FMfcgzGrbRXqCZrlVrLrfsXWlpQKSGSK',
            'interval': 3,
        }
        urlActor.openUrls(urlitem)
        time.sleep(2)
        time.sleep(0.5)
        keyboard.press_and_release('page down')
        time.sleep(0.5)
        keyboard.press_and_release('page up')


        time.sleep(5)
        urlActor.closeBrowser()

    elif mode == 9:
        videFile = 'C:\\Works\\NCL\\Project\\Windows_User_Simulator\\src\\UtilsFunc\\Video_2022-12-12_164101.wmv'
        startFile(videFile)
        #keyboard.press_and_release('space')
        time.sleep(15)
        keyboard.press_and_release('alt+f4')

if __name__ == '__main__':
    testName = 'Ping and ssh login'
    print("Time %s testCase1: \n %s" %(datetime.datetime.now().strftime("%H:%M:%S"), testName))
    testCase(1)
    time.sleep(5)

    testName = 'Run windows network cmd (dir, ipconfig, ping)'
    print("Time %s testCase2: \n %s" %(datetime.datetime.now().strftime("%H:%M:%S"), testName))
    testCase(2)
    time.sleep(5)

    testName = 'Run windows network cmd from a config file (dir, ipconfig, ssh)'
    print("Time %s testCase3: \n %s" %(datetime.datetime.now().strftime("%H:%M:%S"), testName))
    testCase(3)
    time.sleep(5)

    testName = 'Create and edit a MS-office word doc'
    print("Time %s testCase4: \n %s" %(datetime.datetime.now().strftime("%H:%M:%S"), testName))
    testCase(4)
    time.sleep(5)

    testName = 'Create and edit a MS-office ppt doc'
    print("Time %s testCase5: \n %s" %(datetime.datetime.now().strftime("%H:%M:%S"), testName))
    testCase(5)
    time.sleep(5)

    testName = 'Scp a file to the server  rp_fyp_ctf@gateway.ncl.sg'
    print("Time %s testCase6: \n %s" %(datetime.datetime.now().strftime("%H:%M:%S"), testName))
    testCase(6)
    time.sleep(5)

    testName = 'watch Youtube video'
    print("Time %s testCase7: \n %s" %(datetime.datetime.now().strftime("%H:%M:%S"), testName))
    testCase(7)
    time.sleep(5)

    testName = 'check gmail email'
    print("Time %s testCase8: \n %s" %(datetime.datetime.now().strftime("%H:%M:%S"), testName))
    testCase(8)
    time.sleep(5)

    testName = 'watch a local video'
    print("Time %s testCase9: \n %s" %(datetime.datetime.now().strftime("%H:%M:%S"), testName))
    testCase(9)
    time.sleep(5)

    print("All test finished!")