#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        actionSimulator.py
#
# Purpose:     This module is used to record/repeat(simulate play back) user's 
#              mouse and keyboard action.
#
# Author:      Yuancheng Liu
#
# Version:     v_0.1
# Created:     2022/12/05
# Copyright:   n.a
# License:     n.a
#-----------------------------------------------------------------------------

import os
import json
import datetime
import threading
import time

import mouse
import keyboard

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

class actionSimulator(object):

    def __init__(self, recordFileM=None, recordFileK=None) -> None:
        self.mouseEvts = []
        self.keyboardEvts = []
        self.recordFlg = True
        self.startTime = None
        self.recordfileM = recordFileM  # mouse event record file
        self.recordfileK = recordFileK  # key event record file

#-----------------------------------------------------------------------------
    def enableAutoDump(self, enable):
        self.recordFlg = enable

#-----------------------------------------------------------------------------
    def resetActionRcd(self, mouseFlg=True, keyFlg=True):
        """ Re-init the internal action record list.
            Args:
                mouseFlg (bool, optional): flag to identify whether reset mouse 
                        event list. Defaults to True.
                keyFlg (bool, optional): flag to identify whether reset keyboard 
                        event list. Defaults to True
        """
        self.startTime = None
        if mouseFlg: self.mouseEvts = []
        if keyFlg: self.keyboardEvts = []

#-----------------------------------------------------------------------------
    def setMouseRcdFile(self, filePath=None):
        if filePath and not os.path.exists(filePath):
            pathDir = os.path.dirname(filePath)
            if pathDir: os.makedirs(pathDir, exist_ok=True)
        self.recordfileM = filePath

#-----------------------------------------------------------------------------
    def setKeyboardRcdFile(self, filePath=None):
        if filePath and not os.path.exists(filePath):
            pathDir = os.path.dirname(filePath)
            if pathDir: os.makedirs(pathDir, exist_ok=True)
        self.recordfileK = filePath

#-----------------------------------------------------------------------------
    def dumpsFile(self):
        # dumps mouse record to <recordfileM> file.
        if len(self.mouseEvts) > 0:
            try:
                with open(self.recordfileM, 'w') as json_file:
                    recordList = [item._asdict() for item in self.mouseEvts]
                    json.dump(recordList, json_file)
            except Exception as err:
                print('Error    dumpsFile(): Error to create the mouse record file.')
                print('Exception: %s' %str(err))
        # dumps keyboard record to <recordfileK> file.
        if len(self.keyboardEvts) > 0:
            try:
                with open(self.recordfileK, 'w') as json_file:
                    json.dump([item.to_json() for item in self.keyboardEvts], json_file)
            except:
                print('Error    dumpsFile(): Error to create the keyboard record file.')
                print('Exception: %s' %str(err))

#-----------------------------------------------------------------------------
    def record(self, mouseFlg=True, keyFlg=True, rcdTime=0, stopKey=None):
        """ Start to record the user's action.
            Args:
                mouseFlg (bool, optional): flag to identify record mouse event. Defaults to True.
                keyFlg (bool, optional): flag to identify record keyboard event. Defaults to True.
                rcdTime (int, optional): time period(sec) to record, 0 for forever. Defaults to 0.
                stopKey (_type_, optional): stop record when the user press the key. Defaults to None.
        """
        #self.recordFlg = True
        #self.startTime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        if mouseFlg: mouse.hook(self.mouseEvts.append)
        if keyFlg: keyboard.start_recording()
        if rcdTime > 0:
            time.sleep(rcdTime)
        else:
            keyboard.wait(stopKey)
        if mouseFlg: mouse.unhook(self.mouseEvts.append)
        if keyFlg: self.keyboardEvts += keyboard.stop_recording()
        if self.recordFlg: self.dumpsFile()

#-----------------------------------------------------------------------------
    def replay(self, mouseFlg=True, keyFlg=True):
        """ Replay the users' action.
            Args:
                mouseFlg (bool, optional): flag to identify replay mouse event. Defaults to True.
                keyFlg (bool, optional): flag to identify replay keyboard event. Defaults to True.
        """
        keyboard.press_and_release('windows+d')
        m_thread = None
        k_thread = None
        if mouseFlg:
            m_thread = threading.Thread(target = lambda :mouse.play(self.mouseEvts))
            m_thread.start()
        if keyFlg:
            k_thread = threading.Thread(target = lambda :keyboard.play(self.keyboardEvts))
            k_thread.start()
        print("Start to play back user event mouse: %s, keyboard: %s" %(str(mouseFlg), str(keyFlg))) 
        if m_thread: m_thread.join()
        if k_thread:k_thread.join()
        print('finish all the play back')

#-----------------------------------------------------------------------------
    def loadMouseAction(self, actionFile):
        """ load Mouse action event from input record file."""
        if not actionFile or not os.path.exists(actionFile): 
            print ('Warning: The mouse event action record file not exist!')
            return False
        self.mouseEvts = []
        with open(actionFile, 'r') as f:
            print('Start to load mouse event data...')
            data = json.load(f)
            for item in data:
                keys = item.keys()
                if 'event_type' in keys:
                    self.mouseEvts.append(mouse.ButtonEvent(**item))
                elif 'delta' in keys:
                    self.mouseEvts.append(mouse.WheelEvent(**item))
                else:
                    self.mouseEvts.append(mouse.MoveEvent(**item))
        print('Finished load.')
        return True

#-----------------------------------------------------------------------------
    def loadKeyboardAction(self, actionFile):
        """ load Keyboard action event from input record file."""
        if not actionFile or not os.path.exists(actionFile): 
            print ('Warning: The keyboard event action record file not exist!')
            return False
        self.keyboardEvts = []
        with open(actionFile, 'r') as f:
            print('Start to load keyboard event data...')
            data = json.load(f)
            for jsonStr in data:
                evtJson = json.loads(jsonStr)
                deviceInfo = evtJson['device'] if 'device' in evtJson.keys() else None
                modifiersInfo = evtJson['modifiers'] if 'modifiers' in evtJson.keys() else None
                is_keypadInfo = evtJson['is_keypad'] if 'is_keypad' in evtJson.keys() else None
                keyEvnt = keyboard.KeyboardEvent(evtJson['event_type'], evtJson['scan_code'], 
                name=evtJson['name'], time=evtJson['time'], device=deviceInfo, modifiers=modifiersInfo, is_keypad= is_keypadInfo)
                self.keyboardEvts.append(keyEvnt)

        print('Finished load.')
        return True

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

def testCase(mode):
    if mode == 1:
        recorder = actionSimulator()
        recorder.resetActionRcd()
        timeStr = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        mousercdName= 'rcd'+ timeStr + '_mouse.json'
        keyrcdName= 'rcd'+ timeStr + '_key.json'
        recorder.setMouseRcdFile(mousercdName)
        recorder.setKeyboardRcdFile(keyrcdName)
        recorder.record(stopKey="`")
        time.sleep(1)
        print('Start to replay')
        recorder.replay()
    elif mode == 2:
        recorder = actionSimulator()
        recorder.resetActionRcd()
        recorder.enableAutoDump(False)
        recorder.record(rcdTime=5)
        time.sleep(1)
        print('Start to replay')
        recorder.replay()
    else:
        recorder = actionSimulator()
        recorder.resetActionRcd()
        timeStr = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        mousercdName= 'rcd'+ timeStr + '_mouse.json'
        keyrcdName= 'rcd'+ timeStr + '_key.json'
        recorder.setMouseRcdFile(mousercdName)
        recorder.setKeyboardRcdFile(keyrcdName)
        recorder.loadMouseAction('rcd2022_12_05_17_43_10_mouse.json')
        recorder.loadKeyboardAction('rcd2022_12_05_17_43_10_key.json')
        recorder.replay()

if __name__ == '__main__':
    testCase(1)
