import os 
import subprocess

DIR_PATH = os.path.dirname(__file__)
print("Current source code location : %s" % DIR_PATH)

#appFolder = 'UtilsFunc'
appName = 'pingActor.py'
appPath = os.path.join(DIR_PATH, appName)
cmd = "python %s" %str(appPath)
print(cmd)
subprocess.call(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)