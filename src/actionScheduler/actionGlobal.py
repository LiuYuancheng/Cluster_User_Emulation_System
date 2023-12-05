#-----------------------------------------------------------------------------
# Name:        Global.py
#
# Purpose:     This module is used as a local config file to set constants, 
#              global parameters which will be used in the other modules.
#              
# Author:      Yuancheng Liu
#
# Created:     2010/08/26
# Copyright:   
# License:     
#-----------------------------------------------------------------------------
"""
For good coding practice, follow the following naming convention:
    1) Global variables should be defined with initial character 'g'
    2) Global instances should be defined with initial character 'i'
    2) Global CONSTANTS should be defined with UPPER_CASE letters
"""

import os, sys

print("Current working directory is : %s" % os.getcwd())
DIR_PATH = dirpath = os.path.dirname(__file__)
print("Current source code location : %s" % dirpath)
APP_NAME = ('Scheduler', 'actors')

TOPDIR = 'src'
LIBDIR = 'lib'

idx = dirpath.find(TOPDIR)
gTopDir = dirpath[:idx + len(TOPDIR)] if idx != -1 else dirpath   # found it - truncate right after TOPDIR
# Config the lib folder 
gLibDir = os.path.join(gTopDir, LIBDIR)
if os.path.exists(gLibDir):
    sys.path.insert(0, gLibDir)
import Log
Log.initLogger(gTopDir, 'Logs', APP_NAME[0], APP_NAME[1], historyCnt=100, fPutLogsUnderDate=True)

import ConfigLoader
gGonfigPath = os.path.join(dirpath, 'scheduleCfg.txt')
iConfigLoader = ConfigLoader.ConfigLoader(gGonfigPath, mode='r')
if iConfigLoader is None:
    print("Error: The config file %s is not exist.Program exit!" %str(gGonfigPath))
    exit()

CONFIG_DICT = iConfigLoader.getJson()

#------<CONSTANTS>-------------------------------------------------------------
OWN_ID = CONFIG_DICT['Own_ID'] if 'Own_ID' in CONFIG_DICT.keys() else 'Test_Scheduler'
OWN_IP = CONFIG_DICT['OWN_IP'] if 'OWN_IP' in CONFIG_DICT.keys() else '127.0.0.1'
UDP_PORT = int(CONFIG_DICT['HOST_PORT']) # host UDP port

PROFILE_PATH = os.path.join(dirpath, CONFIG_DICT['PROFILE']+'.py')
if not os.path.exists(PROFILE_PATH):
    print("Error: The user proFile %s is not exist.Program exit!" %str(PROFILE_PATH))
    exit()

RPT_MD = CONFIG_DICT['RPT_MD'] if 'RPT_MD' in CONFIG_DICT.keys() else False
HUB_IP = CONFIG_DICT['HUB_IP'] if 'HUB_IP' in CONFIG_DICT.keys() else '127.0.0.1'
HUB_PORT = int(CONFIG_DICT['HUB_PORT'] ) if 'HUB_PORT' in CONFIG_DICT.keys() else 5000

DEBUG_FLG = False
LOG_INFO = 0
LOG_WARN = 1
LOG_ERR = 2
LOG_EXCEPT = 3

# job type
JB_TP_DAILY = 0
JB_TP_RANDOM = 1
JB_TP_WEEKLY = 2

# job state parm
JB_ST_PENDING = 'pending'
JB_ST_ERROR = 'error'
JB_ST_RUNNING = 'running'
JB_ST_FINISH = 'finish'
JB_ST_ACTIVE = 'active'
JB_ST_DEACT = 'deactive'

DB_PATH = os.path.join(dirpath, 'database.db')
SQL_PATH = os.path.join(dirpath, 'schema.sql')


# All the user's config file 
ACTOR_DIR = os.path.join(DIR_PATH, 'UtilsFunc')
ACTOR_CFG = os.path.join(ACTOR_DIR, 'BobConfig')

URL_RCD = os.path.join(ACTOR_CFG, 'urllist.txt')
URL_RCD2 = os.path.join(ACTOR_CFG, 'urllist2.txt')
RST_DIR = os.path.join(ACTOR_CFG, 'datasets')
URL_FN = os.path.join(ACTOR_CFG, 'info.txt')

YOUTUBE_CFG = os.path.join(ACTOR_CFG, 'youTubeList.txt')
WORD_FILE = os.path.join(ACTOR_DIR, 'Report.docx')
WORD_CFG = os.path.join(ACTOR_CFG, 'wordTextInput.txt')

PPT_FILE = os.path.join(ACTOR_DIR, 'Report.pptx')
PPT_CFG1 = os.path.join(ACTOR_CFG, 'pptxInput1.json.')
PPT_CFG2  = os.path.join(ACTOR_CFG, 'pptxInput2.json.')
PPT_CFG3  = os.path.join(ACTOR_CFG, 'pptxInput3.json.')
PPT_CFG4  = os.path.join(ACTOR_CFG, 'pptxInput4.json.')

OFF_FW_EXE = os.path.join(ACTOR_CFG, 'offFW_private.exe')

#-------<GLOBAL VARIABLES (start with "g")>-------------------------------------
def gDebugPrint(msg, prt=True, logType=None):
    if prt: print(msg)
    if logType == LOG_WARN:
        Log.warning(msg)
    elif logType == LOG_ERR:
        Log.error(msg)
    elif logType == LOG_EXCEPT:
        Log.exception(msg)
    elif logType == LOG_INFO or DEBUG_FLG:
        Log.info(msg)

#-------<GLOBAL INSTANCES (start with "i")>-------------------------------------
iDataMgr = None
iScheduler = None
