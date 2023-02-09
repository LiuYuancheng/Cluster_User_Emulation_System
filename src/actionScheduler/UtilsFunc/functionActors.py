#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        functionActor.py
#
# Purpose:     This module will prvoide different individual actor function/class
#              for the action schedular.
#
# Author:      Yuancheng Liu
#
# Version:     v_0.1
# Created:     2023/01/02
# Copyright:   n.a
# License:     n.a
#-----------------------------------------------------------------------------

import os
import time
from selenium import webdriver
import keyboard # keyboard event for windows.(Linux need root permission to execute this)
from pynput.keyboard import Key, Controller # keyboard event for Linux (no need sudo permit)

CHROME_DRI = 'chromedriver.exe' # default chrome 

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class browserActor(object):
    """ A actor used to start a browser and access the urls with the browser.
    """
    def __init__(self, driverPath=None) -> None:
        """ Init example actor = browserActor(driverPath="/home/user/download/chromedriver")
        Args:
            driverPath (str, optional): driver path. Defaults to None. to find the 
            currect dirver, please to refer this link: https://chromedriver.chromium.org/downloads

        """
        dirpath = os.path.dirname(__file__)
        chromeDriverPath = driverPath if driverPath else os.path.join(dirpath, CHROME_DRI)
        self.driver = webdriver.Chrome(executable_path=chromeDriverPath)
        self.startT = 0

#-----------------------------------------------------------------------------
    def openUrls(self, urlConfig):
        """ Open a url in the browser.
        Args:
            urlConfig (_type_):  example:
            urlitem = {
                'cmdID': 'YouTube',
                'url': 'https://www.youtube.com/watch?v=VMebB6hhjW4',
                'interval' :  0 # time interval to wait for next operation.
        """
        try:
            urlStr = urlConfig if isinstance(urlConfig, str) else urlConfig['url'] 
            self.driver.get(urlStr)
        except Exception as err:
            print('Ignore some internet not access exception %s' %str(err))
        if isinstance(urlConfig, dict) and 'interval' in urlConfig.keys():
            time.sleep(urlConfig['interval'])
    
    def closeBrowser(self):
        self.driver.quit()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class keyEventActor(object):
    """ Actor used to emulator user's key input.
    Args:
        object (_type_): windows OS Flag.
    """
    def __init__(self, winOS=True) -> None:
        self.linuxKeyHd = None if winOS else Controller()

    def _linuxKeyMatch(self, char):
        """ covert key string to the pynput's key event parameter."""
        charL = str(char)
        if charL.lower() == 'tab':
            return Key.tab
        elif charL.lower() == 'shift':
            return Key.shift
        elif charL.lower() == 'enter':
            return Key.enter
        return char

#-----------------------------------------------------------------------------
    def getLinuxKeyHd(self):
        return self.linuxKeyHd 

#-----------------------------------------------------------------------------
    def pressAndrelease(self, keySet, interval=0.1):
        if self.linuxKeyHd:
            if not (isinstance(keySet, list) or isinstance(keySet, tuple)): keySet = [keySet]
            for keyChar in keySet:
                self.linuxKeyHd.press(self._linuxKeyMatch(keyChar))
            if interval > 0.1 : time.sleep(interval)
            for keyChar in keySet:
                self.linuxKeyHd.release(self._linuxKeyMatch(keyChar))
        else:
            if isinstance(keySet, list) or isinstance(keySet, tuple):
                keySet = '+'.join(keySet)
            keyboard.press_and_release(keySet)

#-----------------------------------------------------------------------------
    def repeatPress(self, keySet, repeat=1, Interval=0.2):
        for _ in range(repeat):
            self.pressAndrelease(keySet)
            time.sleep(Interval)

#-----------------------------------------------------------------------------
    def simuUserType(self, typeinStr, interval=0.2):
        """ Simulate user type in a string. (under development)
        """
        for char in typeinStr:
            if char == '\n' :
                self.pressAndrelease('enter')
            elif char == ' ':
                self.pressAndrelease('space')
            elif char == '@':
                self.pressAndrelease(('shift', '2'))
            else:
                self.pressAndrelease(char)
            time.sleep(interval)

#-----------------------------------------------------------------------------
    def typeStr(self, inputStr):
        if self.linuxKeyHd:
            self.linuxKeyHd.type(inputStr)
        else:
            keyboard.write(inputStr)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def testCase(mode):
    pass

if __name__ == '__main__':
    testCase(0)