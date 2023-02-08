import os
import time
import datetime
import json
import subprocess
#import keyboard
from funcActor import webActor, runCmd, runWinCmds, startFile, selectFile, scpFile, simuUserType
from pynput.keyboard import Key, Controller

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
        password = ''
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
    elif mode == 10:
        keyboard = Controller()
        urlActor = webActor()
        urlitem = {
            'cmdID': 'kypo',
            'url': 'https://192.168.200.207/csirtmu-dummy-issuer-server/login',
            'interval': 3,
        }
        urlActor.openUrls(urlitem)
        time.sleep(1)
        for i in range(4):
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
            time.sleep(0.5)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(0.5)
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        time.sleep(0.5)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(1)
        account = 'user-1'
        keyboard.type(account)
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        time.sleep(0.5)
        password = 'XtwrK48WTz'
        keyboard.type(password)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(5)
        #urlActor.closeBrowser()
        
        urlitem = {
            'cmdID': 'kypo',
            #'url': 'https://192.168.200.207/home',
            'url': 'https://192.168.200.207/training-run',
            'interval': 3,
        }
        urlActor.openUrls(urlitem)
        for i in range(4):
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
            time.sleep(0.5)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        
        time.sleep(2)
        for i in range(7):
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
            time.sleep(0.5)
        token = 'cs4238'
        keyboard.type(token)
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        time.sleep(0.5)
        posFix = '4714'
        keyboard.type(posFix)
        keyboard.type(token)
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(0.8)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

        urlitem = {
            'cmdID': 'kypo',
            'url': 'https://192.168.200.207/csirtmu-dummy-issuer-server/endsession',
            'interval': 3,
        }
        time.sleep(1)
        urlActor.openUrls(urlitem)
        time.sleep(1)
        for i in range(3):
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
            time.sleep(0.5)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(6)
        urlActor.closeBrowser()
        
        

if __name__ == '__main__':
    testName = 'Ping and ssh login'
    testCase(10)
  
