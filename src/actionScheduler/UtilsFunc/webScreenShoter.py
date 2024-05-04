#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        PyWebScreenShoter.py
#
# Purpose:     This module will use Google-Chrome browser drivers API or the 
#              QT5-QtWebEngineWidgets to capture the webpage's screen shot img 
#              based on the given url. 
#   
# Author:      Yuancheng Liu
#
# Created:     2021/11/23
# Version:     v_0.1.2
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License 
#-----------------------------------------------------------------------------

import os
import sys
from time import sleep
from datetime import datetime
from selenium import webdriver

# Import QT web API to capture the web page screen shot.
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

# Import selenium webdriver API to capture the web page screen shot.
# https://pypi.org/project/webdriver-manager/
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

QT_DRIVER = 1
CH_DRIVER = 2

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

class QTCapture(QWebEngineView):
    """ Capture the web page screen shot with QT5<QtWebEngineWidgets> driver."""
    # Reference link:
    # https://zetcode.com/pyqt/qwebengineview/
    # https://stackoverflow.com/questions/55231170/taking-a-screenshot-of-a-web-page-in-pyqt5
    # https://stackoverflow.com/questions/51154871/python-3-7-0-no-module-named-pyqt5-qtwebenginewidgets
    webSize = (1024, 768) # default web page size

    #-----------------------------------------------------------------------------
    # Init the private function here:
    def _onLoaded(self):
        #self.resize(self.page().contentsSize().toSize()) # Wait for resize
        self.resize(self.webSize[0], self.webSize[1])
        QTimer.singleShot(1000, self._takeScreenshot)

    def _takeScreenshot(self):
        self.grab().save(self.outputFile, b'PNG')
        if self.app: self.app.quit()

    #-----------------------------------------------------------------------------
    def captureQT(self, url, outDirPath, outputName=None):
        """ Capture the web page screen shot with QT5<QtWebEngineWidgets> driver.
            Args:
                url (str): url string
                outDirPath (str): output directory path.
                outputName (str, optional): output image file. Defaults to None, then 
                    the program will create image under format: shot_yymmdd_hhmmss.png
            Returns:
                bool: true if catpure successful else false.
        """
        picName = outputName if outputName else "shot_" + datetime.now().strftime("%Y%m%d_%H%M%S")+'.png'
        self.outputFile = os.path.join(outDirPath, picName)
        try:
            self.load(QUrl(url))
            self.loadFinished.connect(self._onLoaded)
            # Create hidden view without scrollbars
            self.setAttribute(Qt.WA_DontShowOnScreen)
            self.page().settings().setAttribute(QWebEngineSettings.ShowScrollBars, False)
            self.show()
            return True
        except Exception as err:
            print("Error > captureQT() capture error: %s" % str(err))
            return False

    #-----------------------------------------------------------------------------
    def setImgSize(self, sizeTuple):
        self.webSize = sizeTuple

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class webScreenShoter(object):
    """ Webpage screenshot capture module."""
    def __init__(self):
        # Init the Chrome capture dirver.
        self.chDriver = None
        # Init the QT capture App
        self.qtApp = QApplication(sys.argv)
        self.qtDriver = QTCapture()
        self.qtDriver.app = self.qtApp

    #-----------------------------------------------------------------------------
    def setQTimgSz(self, sizeTuple):
        if self.qtDriver: self.qtDriver.setImgSize(sizeTuple)

    #-----------------------------------------------------------------------------
    def getScreenShot(self, urlList, outDirPath, driverMode=QT_DRIVER):
        """ Capture the urls screen shot and save in the output folder.
            Args:
                urlList (list/tuple): url string list.
                outDirPath (str): output directory path.
                driverMode (_type_, optional): driver selection. Defaults to QT_DRIVER.
            Returns:
                _type_: _description_
        """
        if urlList is None or urlList=='': return False
        if not (type(urlList) in [list,tuple]): urlList = [urlList]
        if not os.path.exists(outDirPath): os.mkdir(outDirPath)
        if driverMode == QT_DRIVER:
            for url in urlList:
                self.qtDriver.captureQT(url, outDirPath)
                self.qtApp.exec_()
        elif driverMode == CH_DRIVER:
            for url in urlList:
                self._capturePage(url, outDirPath)
        else:
            print("> Error: the capture driver mode:[%s] is not defined." %str(driverMode))
            return False
        return True

    #-----------------------------------------------------------------------------
    def _capturePage(self, url, outDirPath, outputName=None):
        """ Capture the url screen shot by google browser driver API.
            Args:
                url ([string]): web url string.
                outputDir ([string]): folder path to save the web components.
        """
        try:
            self.chDriver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            self.chDriver.get(url)
            sleep(1) # wait one second to let the browser to show the whole webpage
            picName = outputName if outputName else "shot_"+datetime.now().strftime("%Y%m%d_%H%M%S")+'.png'
            outputFile = os.path.join(outDirPath, picName)
            self.chDriver.get_screenshot_as_file(outputFile)
            self.chDriver.quit()
            return True
        except Exception as err:
            print("Error > _capturePage() capture error: %s" % str(err))
            self.chDriver.quit()
            return False
    
    #-----------------------------------------------------------------------------
    def stop(self):
        if self.chDriver: self.chDriver.quit()
        if self.qtApp: self.qtApp.quit()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main():
    print("Start the Web screenshoter")
    capturer = webScreenShoter()
    print("Current working directory is : %s" % os.getcwd())
    dirpath = os.path.dirname(os.path.abspath(__file__))
    print("Current source code location : %s" % dirpath)
    print("Select the driver mode: \n - 1: QT5 QtWebEngineWidgets driver \n - 2: Selenium Chrome driver")
    driverMode = int(input())
    outputFolder = os.path.join(dirpath, "outputFolder")
    while True:
        print("Input the url:")
        url = str(input())
        if url in ('exist', 'quit', 'q', 'Q'): break
        capturer.getScreenShot(url, outputFolder, driverMode=driverMode)
        print('Finished')
    capturer.stop()

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
