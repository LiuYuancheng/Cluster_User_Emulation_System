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
from random import randint
import actionGlobal as gv
from UtilsFunc import pingActor
from UtilsFunc import funcActor
import Log
import SSHconnector


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
    appName = 'zoomActor.py'
    appPath = os.path.join(gv.ACTOR_DIR, appName)
    cmd = "python %s" %str(appPath)
    result = funcActor.runCmd(cmd)
    print(result)



#-----------------------------------------------------------------------------

def testCase(mode):
    func_0935()

if __name__ == '__main__':
    testCase(1)