#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        kypoActor.py
#
# Purpose:     This module will simulator a student to login the kypo-Crp
#              platfrom, type in the couse access token, then log out.
#
# Author:      Yuancheng Liu
#
# Version:     v_0.1
# Created:     2023/02/09
# Copyright:   n.a
# License:     n.a
#-----------------------------------------------------------------------------

import os 
import time
import yaml
from yaml.loader import SafeLoader

import ConfigLoader
from functionActors import browserActor, keyEventActor

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class kypoActor(object):

    def __init__(self, configFile) -> None:
        dirpath = os.path.dirname(__file__)
        print("Current source code location : %s" % dirpath)
        ld = ConfigLoader.ConfigLoader(os.path.join(dirpath, configFile), mode='r')
        self.configJson = ld.getJson()
        self.usersList = None
        try:
            userCrePath = os.path.join(dirpath, self.configJson['User_Cred'])
            with open(userCrePath, 'r') as f:
                self.usersList = list(yaml.load_all(f, Loader=SafeLoader))[0]
            print(self.usersList)
        except Exception as err:
            print("Load the user crediential file error: %s" %str(err))
            return None
        print(self.configJson)
        self.webActor = browserActor(os.path.join(dirpath, self.configJson['Driver_file']))
        self.keyActor = keyEventActor(winOS=False)

#-----------------------------------------------------------------------------
    def accessPage(self, username, password):
        ipAddr = self.configJson['Kypo_ip']
        accessTK = self.configJson['Acc_token']
        accessPF = self.configJson['Acc_pfix']
        keyTab, keyEnter = 'tab', 'enter'
        print("Start test user: %s " %str(username))
        # open login page
        print(' - login')
        urlitem = {
            'cmdID': 'kypo-login',
            'url': 'https://%s/csirtmu-dummy-issuer-server/login' %str(ipAddr),
            'interval': 2,
        }
        self.webActor.openUrls(urlitem)
        time.sleep(1)
        self.keyActor.repeatPress(keyTab, repeat=4, Interval=0.5)
        self.keyActor.pressAndrelease(keyEnter)
        time.sleep(0.5)
        self.keyActor.pressAndrelease(keyTab)
        time.sleep(0.5)
        self.keyActor.pressAndrelease(keyEnter)
        time.sleep(1) # wait 1 sec for the page refresh
        self.keyActor.typeStr(username)
        self.keyActor.pressAndrelease(keyTab)
        time.sleep(0.5)
        self.keyActor.typeStr(password)
        self.keyActor.pressAndrelease(keyEnter)
        time.sleep(5)
        # access the taining page
        print("-access training")
        urlitem = {
            'cmdID': 'kypo-training',
            'url': 'https://%s/training-run' %str(ipAddr),
            'interval': 2,
        }
        self.webActor.openUrls(urlitem)
        self.keyActor.repeatPress(keyTab, repeat=4, Interval=0.5)
        self.keyActor.pressAndrelease(keyEnter)
        time.sleep(2)

        self.keyActor.repeatPress(keyTab, repeat=7, Interval=0.5)
        self.keyActor.typeStr(accessTK)
        self.keyActor.repeatPress(keyTab, repeat=2, Interval=0.5)
        time.sleep(0.2)
        self.keyActor.typeStr(accessPF)
        self.keyActor.repeatPress(keyTab, repeat=2, Interval=0.5)
        self.keyActor.repeatPress(keyEnter, repeat=2, Interval=0.5)

        # logout
        print('- logout')
        urlitem = {
            'cmdID': 'kypo-logout',
            'url': 'https://%s/csirtmu-dummy-issuer-server/endsession' %str(ipAddr),
            'interval': 2,
        }
        self.webActor.openUrls(urlitem)
        self.keyActor.repeatPress(keyTab, repeat=3, Interval=0.5)
        self.keyActor.pressAndrelease(keyEnter)
        time.sleep(3) # wait logout finish.

#-----------------------------------------------------------------------------
    def startAccess(self):
        for item in self.usersList:
            self.accessPage(item['name'], item['password'])
        print("Finished all")
        self.webActor.closeBrowser()

#-----------------------------------------------------------------------------
def main():
    keypoActor = kypoActor('kypoConfig.txt')
    keypoActor.startAccess()

if __name__ == '__main__':
    main()