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
# from UtilsFunc import email_gen

import Log
import SSHconnector
import udpCom


PORT = 443 # port to download the server certificate most server use 443.

#-----------------------------------------------------------------------------

def func_0905():
    account = 'bob@gt.org'
    password = '123'
    smtpServer = 'email.gt.org'
    smtpPort = 143
    actor = emailActor.emailActor(account, password)
    actor.initEmailReader(smtpServer, smtpPort = smtpPort, sslConn=False)
    print(actor.getMailboxList())
    print('=> read 2 random in last 3 email')
    readConfig2 = {
        'mailBox': 'inbox',
        'sender': None,
        'number': 6,
        'randomNum': 0,
        'interval': 2,
        'returnFlg': False
    }
    result = actor.readLastMail(configDict=readConfig2)
    actor.close()

#-----------------------------------------------------------------------------

def func_0920():
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

def func_0923():
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

def func_1000():
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

def func_1300():
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

def func_1500():
    # play the game
    timeInterval = 20
    actor = dinoActor.dinoActor(playtime=60*timeInterval)
    actor.play()

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

def func_1545():
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

def func_1600():
    intensity = 30 # send 3000 times
    sleep_time = 10  # do not sleep
    for counter in range(intensity):
        print("send one email")
        email_server = "mail.gt.org.txt"
        # email_gen.send_mail(email_server)

    time.sleep(sleep_time)

#-----------------------------------------------------------------------------

def func_1700():
    pass

#-----------------------------------------------------------------------------

def func_1735():
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
def testCase(mode):
    func_1520()

if __name__ == '__main__':
    testCase(1)
           