# reference link: https://schedule.readthedocs.io/en/stable/
# https://schedule.readthedocs.io/en/stable/
import os 
import schedule
import subprocess
import threading

import time
import datetime


# def job():
#     print("I'm working...")

# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)


class userAction(object):
    def __init__(self, actionName='', timeStr=None, runFunc=None, threadFlg=False) -> None:
        self.name = actionName
        self.timeStr = timeStr
        self.func = runFunc
        self.threadFlg = threadFlg
    
    def runFunc(self):
        print('Start to run job')
        if self.func:
            if self.threadFlg:
                jobthread = threading.Thread(target=self.func)
                jobthread.start()
            else:
                self.func()
        else:
            print('No function is added')


class userActionPing(userAction):
    def __init__(self, pingDict, actionName='', timeStr=None, runFunc=None, threadFlg=False) -> None:
        super().__init__(actionName, timeStr, runFunc, threadFlg)
        self.pingList = pingDict['peerList']
        self.pingInterval = pingDict['interval']   # ping interval between each ping peer. 
        self.consoleEnable = pingDict['console']

    def run():
        pass


class actionScheduler(object):

    def __init__(self) -> None:
        # The action dictionary
        self.actionDict = {}
        self.terminate = False 

    def addAction(self, actionObj):
        if actionObj:
            self.actionDict[actionObj.name] = actionObj

    def buildPlan(self):
        for item in self.actionDict:
            name, action = item

    def startSimulate(self):
        while not self.terminate:
            schedule.run_pending()
            time.sleep(1)

    def run_threaded(job_func):
        job_thread = threading.Thread(target=job_func)
        job_thread.start()


def testCase(mode):

    
    timeData = datetime.datetime.now() 
    minDelay = datetime.timedelta(seconds = 60)
    
    # Task 1: ping
    def func1():
        subprocess.call('python C:\\Works\\NCL\\Project\\Windows_User_Simulator\\src\\UtilsFunc\\pingActor.py', creationflags=subprocess.CREATE_NEW_CONSOLE)
    timeData+= datetime.timedelta(seconds = 10)
    nextMin = timeData.strftime("%H:%M:%S")
    print(nextMin)
    userAction1 = userAction(actionName='action1', timeStr=nextMin, runFunc=func1, threadFlg=False)
    schedule.every().day.at(userAction1.timeStr).do(userAction1.runFunc)

    # start Zoom meeting
    def func2():
        subprocess.call('python C:\\Works\\NCL\\Project\\Windows_User_Simulator\\src\\UtilsFunc\\zoomActor.py', creationflags=subprocess.CREATE_NEW_CONSOLE)
    timeData += minDelay
    nextMin = timeData.strftime("%H:%M:%S")
    userAction2 = userAction(actionName='action2', timeStr=nextMin, runFunc=func2, threadFlg=False)
    schedule.every().day.at(userAction2.timeStr).do(userAction2.runFunc)

    # Dra picture
    def func3():
        os.startfile("C:\\Works\\NCL\\Project\\Windows_User_Simulator\\src\\dist\\actionSimulator.exe")

    timeData += minDelay
    nextMin = timeData.strftime("%H:%M:%S")
    userAction3 = userAction(actionName='action3', timeStr=nextMin, runFunc=func3, threadFlg=True)
    schedule.every().day.at(userAction3.timeStr).do(userAction3.runFunc)
    

    # playgame
    def func4():
        subprocess.call('python C:\\Works\\NCL\\Project\\Windows_User_Simulator\\src\\UtilsFunc\\dinoActor.py', creationflags=subprocess.CREATE_NEW_CONSOLE)

    timeData += minDelay
    nextMin = timeData.strftime("%H:%M:%S")
    userAction3 = userAction(actionName='action3', timeStr=nextMin, runFunc=func4, threadFlg=True)
    schedule.every().day.at(userAction3.timeStr).do(userAction3.runFunc)

    print(schedule.get_jobs())

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    testCase(1)

