#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        zoomActor.py
#
# Purpose:     This module is used to start a zoom meeting via browser with the 
#              input url.
# Author:      Yuancheng Liu, Ponnu Rose Raju
#
# Version:     v_0.2
# Created:     2022/12/12
# Copyright:   n.a
# License:     n.a
#-----------------------------------------------------------------------------

import os 
import time
import keyboard
# change to use new webdriver-manager module : https://pypi.org/project/webdriver-manager/
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

"""
Test Join Zoom Meeting
https://us04web.zoom.us/j/4580466160?pwd=d0ZUSCs0bWpMc2o2MHgzTS80a2tJdz09

Meeting ID: 458 046 6160
Passcode: 8cVJ6M
    
"""
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class zoomActor(object):

    def __init__(self, userName=None, driverPath=None):
        # dirpath = os.path.dirname(__file__)
        # chromeDriverPath = driverPath if driverPath else os.path.join(dirpath, 'chromedriver.exe')
        # self.driver = webdriver.Chrome(executable_path=chromeDriverPath)
        self.userName = userName
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.appFlg = False # The zoom is open in a App

#-----------------------------------------------------------------------------
    def _keyboarPress(self, keyStr):
        time.sleep(0.3)
        keyboard.press_and_release(keyStr)
        time.sleep(0.3)

#-----------------------------------------------------------------------------
    def startMeeting(self, meetUrl, appFlg=True):
        try:
            self.driver.get(meetUrl)
        except Exception as err:
            print("Start the meeting url failed")
            return False
        self.appFlg = appFlg
        if self.appFlg:
            # Click accept the zoom meeting in the web pop-up window.
            self._keyboarPress('tab')
            self._keyboarPress('tab')
            self._keyboarPress('enter')
            # wait 15 second for the zoom start 
            time.sleep(15)
            # accept the use compute audo eable
            self._keyboarPress('enter')
        else:
            # use the API to accept the "open ZOOM in app"
            #obj = self.driver.switch_to.alert
            #time.sleep(1)
            #print(obj.text)
            pass

#-----------------------------------------------------------------------------
    def endCrtMeeting(self):
        # use hotkey to close the zoom
        # close the zoom.  
        self._keyboarPress('alt+f4')
        self._keyboarPress('enter')
        self._keyboarPress('alt+f4')
        # close the browser 
        time.sleep(3)
        self.driver.quit()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def testCase(mode=0):
    if mode == 1:
        actor = zoomActor(userName='TestUser_Bob')
        actor.startMeeting('https://us04web.zoom.us/j/4580466160?pwd=d0ZUSCs0bWpMc2o2MHgzTS80a2tJdz09')
        time.sleep(10)
        actor.endCrtMeeting()
        print("Finish")
    else:
        pass

if __name__ == '__main__':
    testCase(mode=1)
