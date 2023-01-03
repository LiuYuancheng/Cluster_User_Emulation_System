#-----------------------------------------------------------------------------
# Name:        actorFunctions.py
#
# Purpose:     Please put your actor function in this module 
#              
# Author:      Yuancheng Liu
#
# Created:     2020/12/15
# Copyright:   
# License:     
#-----------------------------------------------------------------------------
import os
import glob
import time
import json
import random
from random import randint
import keyboard
import string
import actionGlobal as gv
from urllib.parse import urljoin, urlparse
from UtilsFunc import pingActor, funcActor, zoomActor, webDownload, dinoActor, emailActor
from UtilsFunc import email_gen

import Log
import SSHconnector
import udpCom


PORT = 443 # port to download the server certificate most server use 443.

#-----------------------------------------------------------------------------
def func_0901():
    # ping all the peers in the config file one by one
    parallel = False
    showConsole = True
    configPath = os.path.join(gv.ACTOR_CFG, 'pingTestDest.json')
    actor = pingActor.pingActor(configPath, parallel=parallel, Log=None, showConsole=showConsole)
    result = actor.runPing()

#-----------------------------------------------------------------------------
def func_0910():
    # ping every ip in a range one by one 
    parallel = False
    pingPrefix = '192.168.55.'
    ipRange = (1, 24)
    showConsole = False
    pinDict= {}
    for i in range(ipRange[0], ipRange[1]):
        pinDict[pingPrefix+str(i)] = randint(1,10)
    actor = pingActor.pingActor(pinDict, parallel=parallel, Log=Log, showConsole=showConsole)
    result = actor.runPing()
    print(result)

#-----------------------------------------------------------------------------
def func_0913():
    # run windows cmd one by one 
    configPath = os.path.join(gv.ACTOR_CFG, 'cmd_09_13.json')
    result = funcActor.runWinCmds(configPath, rstRecord=True)
    print(result)

#-----------------------------------------------------------------------------
def func_0920():
    # SSH to a server
    # YC: I added the config here because it contents the password. So after conver to 
    #   a exe file the hardcoded password will not expose to public.
    server = ('gateway.ncl.sg', 'rp_fyp_ctf', 'rpfyp@ncl2022')
    def test1RplyHandleFun(replyStr):
        print("Got reply: %s" %str(replyStr))
        #if 'rp_fyp_ctf' in replyStr['reply']:
        #    print('Test1 (mainhost): Pass')
        #elif 'ncl' in replyStr:
        #    print('Test1 (jumphost): Pass')
        #else: 
        #    print('Test1: Fail')
    # put the cmd you want to run here.
    cmdList = ['pwd', 'who', 'ip a', 'ifconfig', 'ls -l', 'traceroute']
    mainHost = SSHconnector.sshConnector(None, server[0], server[1], server[2])
    for cmd in cmdList:
        mainHost.addCmd(cmd, test1RplyHandleFun)
    mainHost.InitTunnel()
    mainHost.runCmd(interval=1)
    mainHost.close()

#-----------------------------------------------------------------------------
def func_0932():
    # 
    cmdsList = [
        {   'cmdID': 'cmd_1',
            'console': True,
            'cmdStr': 'three C:\\Works',
            'winShell': True,
            'repeat': 1,
            'interval': 5
        },
        {   'cmdID': 'cmd_2',
            'console': False,
            'cmdStr': 'DIR C:\\Works',
            'winShell': True,
            'repeat': 1,
            'interval': 2
        },
        {   'cmdID': 'cmd_3',
            'console': False,
            'cmdStr': 'where /r C:\\Works\\NCL\\NCL_Doc\\wordDoc *.docx',
            'winShell': True,
            'repeat': 1,
            'interval': 2 
        }
    ] 
    result = funcActor.runWinCmds(cmdsList, rstRecord=True)
    print(result)
    
#-----------------------------------------------------------------------------
def func_0935():
    # start a zoom meeting
    #appName = 'zoomActor.py'
    #appPath = os.path.join(gv.ACTOR_DIR, appName)
    #cmd = "python %s" %str(appPath)
    #result = funcActor.runCmd(cmd)
    #print(result)
    actor = zoomActor.zoomActor(userName='TestUser_Bob')
    actor.startMeeting('https://us04web.zoom.us/j/4580466160?pwd=d0ZUSCs0bWpMc2o2MHgzTS80a2tJdz09')
    meetingPeriod = 20 # 20 mins meeting
    time.sleep(60*meetingPeriod)
    actor.endCrtMeeting()
    print("Finish")

#-----------------------------------------------------------------------------
def func_1015():
    # download some web contents based on the url config. 
    soup = webDownload.urlDownloader(imgFlg=True, linkFlg=True, scriptFlg=True, caFlg=True)
    count = failCount= 0
    if not os.path.exists(gv.RST_DIR): os.mkdir(gv.RST_DIR)
    soup.setResutlDir(gv.RST_DIR)
    print("> load url record file %s" %gv.URL_RCD)
    with open(gv.URL_RCD) as fp:
        urllines = fp.readlines()
        for line in urllines:
            if line[0] in ['#', '', '\n', '\r', '\t']: continue # jump comments/empty lines.
            count += 1
            print("> Process URL {}: {}".format(count, line.strip()))
            if ('http' in line):
                line = line.strip()
                domain = str(urlparse(line).netloc)
                folderName = "_".join((str(count), domain))
                result = soup.savePage(line, folderName)
                # soup.savePage('https://www.google.com', 'www_google_com')
                if result: 
                    print('Finished.')
                else:
                    failCount +=1
    print("\n> Download result: download %s url, %s fail" %(str(count), str(failCount)))

#-----------------------------------------------------------------------------
def func_1040():
    # watch youTube video 
    watchActor = funcActor.webActor()
    count = failCount= 0
    watchPeriod = 5
    print("> load youTube url record file %s" %gv.YOUTUBE_CFG)
    with open(gv.YOUTUBE_CFG) as fp:
        urllines = fp.readlines()
        for line in urllines:
            if line[0] in ['#', '', '\n', '\r', '\t']: continue # jump comments/empty lines.
            count += 1
            print("> Process URL {}: {}".format(count, line.strip()))
            if ('http' in line):
                line = line.strip()
                urlitem = {
                    'cmdID': 'YouTube',
                    'url': line,
                    'interval': 3,
                }
                watchActor.openUrls(urlitem)
                keyboard.press_and_release('page down')
                time.sleep(2)
                keyboard.press_and_release('page up')
                time.sleep(2)
                keyboard.press_and_release('space')
                time.sleep(60*watchPeriod)

    watchActor.closeBrowser()

#-----------------------------------------------------------------------------
def func_1050():
    # Open and edit the word doc.
    funcActor.startFile(gv.WORD_FILE)
    time.sleep(3) # wait office start the word doc.
    try:
        with open(gv.WORD_CFG) as fp:
            textLine = fp.readlines()
            for line in textLine:
                funcActor.simuUserType(line)
        # close and save the file.
        time.sleep(1)
        keyboard.press_and_release('alt+f4')
        time.sleep(1)
        keyboard.press_and_release('enter')

    except:
        print("No input file config!")

#-----------------------------------------------------------------------------
def func_1125():
    # Edit the ppt file
    try:
        pptConfig = gv.PPT_CFG1 # you can build your own config file.
        with open(pptConfig) as fp:
            actions = json.load(fp)
            for action in actions:
                if 'picName' in action.keys():
                    action['picName'] = os.path.join(gv.ACTOR_CFG, action['picName'])
                funcActor.msPPTedit(gv.PPT_FILE, action)
    except Exception as err:
        print("The pptx config file is not exist.")
        print("error: %s" %str(err))

#-----------------------------------------------------------------------------
def func_1135():
    # play the game
    timeInterval = 20
    actor = dinoActor.dinoActor(playtime=60*timeInterval)
    actor.play()

#-----------------------------------------------------------------------------
def func_1310():
    # ping every ip in a range one by one 
    parallel = False
    pingPrefix = '192.168.56.'
    ipRange = (10, 224)
    showConsole = True
    pinDict= {}
    for i in range(100):
        ipAddr = randint(ipRange[0], ipRange[1])
        pinDict[pingPrefix+str(ipAddr)] = randint(5,10)
    actor = pingActor.pingActor(pinDict, parallel=parallel, Log=Log, showConsole=showConsole)
    result = actor.runPing()
    print(result)

#-----------------------------------------------------------------------------
def func_1345():
    # ping every ip in a range one by one 
    parallel = False
    pingPrefix = '192.168.57.'
    ipRange = (10, 224)
    for i in range(10):
        def test1RplyHandleFun(replyStr):
            print("Got reply: %s" %str(replyStr))
            #if 'rp_fyp_ctf' in replyStr['reply']:
            #    print('Test1 (mainhost): Pass')
            #elif 'ncl' in replyStr:
            #    print('Test1 (jumphost): Pass')
            #else: 
            #    print('Test1: Fail')
        # put the cmd you want to run here.
        cmdList = ['pwd', 'who', 'ip a', 'ifconfig', 'ls -l', 'traceroute']
        host = pingPrefix+str(randint(ipRange[0], ipRange[1]))
        user = 'rp_fyp_ctf'
        password = 'not exist'
        try:
            mainHost = SSHconnector.sshConnector(None, host, user, password)
            for cmd in cmdList:
                mainHost.addCmd(cmd, test1RplyHandleFun)
            mainHost.InitTunnel()
            mainHost.runCmd(interval=1)
            mainHost.close()
        except Exception as err:
            print('The ssh host [%s] is not access able' %str(host))
            print('Error: %s' %str(err))
            time.sleep(10)

#-----------------------------------------------------------------------------
def func_1410():
    # Run the fw exe file.
    os.startfile(gv.OFF_FW_EXE)
    time.sleep(20)
    keyboard.press_and_release('enter')

#-----------------------------------------------------------------------------
def func_1430():
    soup = webDownload.urlDownloader(imgFlg=True, linkFlg=True, scriptFlg=True, caFlg=True)
    count = failCount= 0
    if not os.path.exists(gv.RST_DIR): os.mkdir(gv.RST_DIR)
    soup.setResutlDir(gv.RST_DIR)
    print("> load url record file %s" %gv.URL_RCD2)
    with open(gv.URL_RCD2) as fp:
        urllines = fp.readlines()
        for line in urllines:
            if line[0] in ['#', '', '\n', '\r', '\t']: continue # jump comments/empty lines.
            count += 1
            print("> Process URL {}: {}".format(count, line.strip()))
            if ('http' in line):
                line = line.strip()
                domain = str(urlparse(line).netloc)
                folderName = "_".join((str(count), domain))
                result = soup.savePage(line, folderName)
                # soup.savePage('https://www.google.com', 'www_google_com')
                if result: 
                    print('Finished.')
                else:
                    failCount +=1
    print("\n> Download result: download %s url, %s fail" %(str(count), str(failCount)))

#-----------------------------------------------------------------------------
def getRandomStr(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return result_str

#-----------------------------------------------------------------------------
def func_1450():
    pingPrefix = '192.168.58.'
    ipRange = (10, 224)
    portRange = (100, 8080) 
    for i in range(100):
        ipAddr = pingPrefix+str(randint(ipRange[0], ipRange[1]))
        udpPort = randint(portRange[0], portRange[1])
        client = udpCom.udpClient((ipAddr, udpPort))
        for i in range(20):
            msg = getRandomStr(400)
            try:
                resp = client.sendMsg(msg, resp=False)
                print('Send message to %s'%str(ipAddr))
                print('msg: %s' %str(msg))
                #print(" - Server resp: %s" % str(resp))
                time.sleep(0.5)
            except Exception as err:
                print('Error: %s' %str(err))

#-----------------------------------------------------------------------------
def func_1515():
    # Edit the ppt file
    try:
        pptConfig = gv.PPT_CFG2 # you can build your own config file.
        with open(pptConfig) as fp:
            actions = json.load(fp)
            for action in actions:
                if 'picName' in action.keys():
                    action['picName'] = os.path.join(gv.ACTOR_CFG, action['picName'])
                funcActor.msPPTedit(gv.PPT_FILE, action)
    except Exception as err:
        print("The pptx config file is not exist.")
        print("error: %s" %str(err))

#-----------------------------------------------------------------------------
def func_1520():
    # play the game
    timeInterval = 10
    actor = dinoActor.dinoActor(playtime=60*timeInterval)
    actor.play()

#-----------------------------------------------------------------------------
def func_1520():
    # play the game
    timeInterval = 10
    actor = dinoActor.dinoActor(playtime=60*timeInterval)
    actor.play()

#-----------------------------------------------------------------------------
def func_1555():
    # Edit the ppt file
    try:
        pptConfig = gv.PPT_CFG3 # you can build your own config file.
        with open(pptConfig) as fp:
            actions = json.load(fp)
            for action in actions:
                if 'picName' in action.keys():
                    action['picName'] = os.path.join(gv.ACTOR_CFG, action['picName'])
                funcActor.msPPTedit(gv.PPT_FILE, action)
    except Exception as err:
        print("The pptx config file is not exist.")
        print("error: %s" %str(err))

#-----------------------------------------------------------------------------
def func_1600():
    videoFile = os.path.join(gv.ACTOR_DIR, 'Video_2022-12-12_164101.wmv')
    funcActor.startFile(videoFile)
    watchTime = 20
    #keyboard.press_and_release('space')
    time.sleep(60*watchTime)
    keyboard.press_and_release('alt+f4')

#-----------------------------------------------------------------------------
def func_1635():

    os.chdir(gv.ACTOR_CFG)
    for file in glob.glob("*.png"):
        filePath = os.path.join(gv.ACTOR_CFG, file)
        funcActor.startFile(filePath)
        time.sleep(1)
        keyboard.press_and_release("alt+f4")

#-----------------------------------------------------------------------------
def func_1725():
    # Edit the ppt file
    try:
        pptConfig = gv.PPT_CFG4 # you can build your own config file.
        with open(pptConfig) as fp:
            actions = json.load(fp)
            for action in actions:
                if 'picName' in action.keys():
                    action['picName'] = os.path.join(gv.ACTOR_CFG, action['picName'])
                funcActor.msPPTedit(gv.PPT_FILE, action)
    except Exception as err:
        print("The pptx config file is not exist.")
        print("error: %s" %str(err))

#-----------------------------------------------------------------------------
def func_1740():
    account = 'bob@gt.org'
    password = '123'
    smtpServer = 'email.gt.org'
    smtpPort = 143
    actor = emailActor.emailActor(account, password, smtpServer, smtpPort=smtpPort)
    actor.readLastMail(emailNum=2, interval= 10)

#-----------------------------------------------------------------------------
def func_1810():
    intensity = 30 # send 3000 times
    sleep_time = 10  # do not sleep
    for counter in range(intensity):
        print("send one email")
        email_server = "mail.gt.org.txt"
        email_gen.send_mail(email_server)

    time.sleep(sleep_time)

#-----------------------------------------------------------------------------
def testCase(mode):
    func_1810()

if __name__ == '__main__':
    testCase(1)
