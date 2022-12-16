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
import time
from random import randint
import actionGlobal as gv
from urllib.parse import urljoin, urlparse
from UtilsFunc import pingActor, funcActor, zoomActor, webDownload

import Log
import SSHconnector


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
    ipRange = (1, 224)
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
def testCase(mode):
    func_1015()

if __name__ == '__main__':
    testCase(1)