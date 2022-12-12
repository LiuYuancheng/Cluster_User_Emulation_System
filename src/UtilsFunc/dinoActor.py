#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        dinoActor.py
#
# Purpose:     This module is used to start a chrome and play the google dino
# Author:      Yuancheng Liu
#
# Version:     v_0.1
# Created:     2022/12/12
# Copyright:   n.a
# License:     n.a
#-----------------------------------------------------------------------------

import os
import time
import keyboard
from selenium import webdriver

import threading
from PIL import ImageGrab, ImageOps
import pyautogui
import time
import numpy as np


CHROME_DRI = 'chromedriver.exe'

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class dinoActor(object):

    def __init__(self, driverPath=None):
        dirpath = os.path.dirname(__file__)
        chromeDriverPath = driverPath if driverPath else os.path.join(
            dirpath, CHROME_DRI)
        self.driver = webdriver.Chrome(executable_path=chromeDriverPath)
        self.appFlg = False  # The zoom is open in a App

        # coordinates of replay button to start the game
        self.replaybutton = (480, 421)
        # this coordinates represent the top-right coordinates
        # that will be used to define the front box
        self.dinasaur = (190, 440)
        self.count = 0
        self.terminate = False

    def restartGame(self):
        # using pyautogui library, we are clicking on the
        # replay button without any user interaction
        pyautogui.click(self.replaybutton)
        # we will keep our Bot always down that
        # will prevent him to get hit by bird
        pyautogui.keyDown('space')
        pyautogui.keyUp('space')    

    def press_space(self):
        # releasing the Down Key
        #pyautogui.keyUp('down')
        # pressing Space to overcome Bush
        pyautogui.keyDown('space')
        # so that Space Key will be recognized easily
        time.sleep(0.05)
        # printing the "Jump" statement on the
        # terminal to see the current output
        print("jump")
        time.sleep(0.10)
        # releasing the S pace Key
        pyautogui.keyUp('space')
        # again pressing the Down Key to keep my Bot always down
        #pyautogui.keyDown('down')

    def imageGrab(self):
        # defining the coordinates of box in front of dinosaur
        box = (self.dinasaur[0]+30, self.dinasaur[1],
               self.dinasaur[0]+120, self.dinasaur[1]+2)

        # grabbing all the pixels values in form of RGB tuples
        image = ImageGrab.grab(box)
        # converting RGB to Grayscale to
        # make processing easy and result faster
        grayImage = ImageOps.grayscale(image)
        # using numpy to get sum of all grayscale pixels
        a = np.array(grayImage.getcolors())
        # returning the sum
        print(a.sum())
        return a.sum()

    def sctn(self):
        while self.count < 2:
            self.count +=1
            if self.count == 2:
                self.terminate = True
                return
            self.restartGame()
            time.sleep(30)

    def play(self):
        try:
            self.driver.get('chrome://dino/')
        except:
            print('11')
        time.sleep(3)
        keyboard.press_and_release('space')
        time.sleep(2)
        keyboard.press_and_release('space')
        time.sleep(0.1)
        
        S = threading.Timer(10.0, self.sctn)  
        S.start()

        self.restartGame()
        while not self.terminate:
            if(self.imageGrab() != 435):
                self.press_space()
                # time to recognize the operation performed by above function
                time.sleep(0.1)
        S.cancel()
        self.driver.quit()
        print("end!")

def testCase(mode=0):
    if mode == 1:
        actor = dinoActor()
        actor.play()
        time.sleep(10)
        print("Finish")
    else:
        pass


if __name__ == '__main__':
    testCase(mode=1)
