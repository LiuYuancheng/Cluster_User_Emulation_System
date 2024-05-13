#-----------------------------------------------------------------------------
# Name:        frontGlobal.py
#
# Purpose:     This module is used as a local config file to set constants, 
#              global parameters which will be used in the other modules.
#              
# Author:      Yuancheng Liu
#
# Created:     2022/08/26
# Version:     v_0.2.3
# Copyright:   Copyright (c) 2023 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------
"""
    For good coding practice, follow the below  naming convention:
        1) Global variables should be defined with initial character 'g'
        2) Global instances should be defined with initial character 'i'
        2) Global CONSTANTS should be defined with UPPER_CASE letters
"""

import os
import sys

print("Current working directory is : %s" % os.getcwd())
dirpath = os.path.dirname(os.path.abspath(__file__))
print("Current source code location : %s" % dirpath)
APP_NAME = ('CUE_Monitor_Hub', 'frontend')

TOPDIR = 'src'
LIBDIR = 'lib'

idx = dirpath.find(TOPDIR)
gTopDir = dirpath[:idx + len(TOPDIR)] if idx != -1 else dirpath   # found it - truncate right after TOPDIR
# Config the lib folder 
gLibDir = os.path.join(gTopDir, LIBDIR)
if os.path.exists(gLibDir): sys.path.insert(0, gLibDir)

#-----------------------------------------------------------------------------
# load the config file.
import ConfigLoader
CONFIG_FILE_NAME = 'config.txt'
gGonfigPath = os.path.join(dirpath, CONFIG_FILE_NAME)
iConfigLoader = ConfigLoader.ConfigLoader(gGonfigPath, mode='r')
if iConfigLoader is None:
    print("Error: The config file %s is not exist.Program exit!" %str(gGonfigPath))
    exit()
CONFIG_DICT = iConfigLoader.getJson()

#-----------------------------------------------------------------------------
# Init the logger
import Log
Log.initLogger(gTopDir, 'Logs', APP_NAME[0], APP_NAME[1], historyCnt=100,
               fPutLogsUnderDate=True)
# Init the log type parameters.
DEBUG_FLG   = False
LOG_INFO    = 0
LOG_WARN    = 1
LOG_ERR     = 2
LOG_EXCEPT  = 3

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

#------<CONSTANTS>-------------------------------------------------------------
RC_TIME_OUT = 10    # reconnection time out.
APP_SEC_KEY = 'secrete-key-goes-here'
UPDATE_PERIODIC = 15
COOKIE_TIME = 30

#-------<GLOBAL VARIABLES (start with "g")>-------------------------------------
# VARIABLES are the built in data type.
gGonfigPath = os.path.join(dirpath, 'peerConfig.txt')

# Flask App parameters : 
gflaskHost = '0.0.0.0'
gflaskPort = int(CONFIG_DICT['FLASK_SER_PORT']) if 'FLASK_SER_PORT' in CONFIG_DICT.keys() else 5000
gflaskDebug = CONFIG_DICT['FLASK_DEBUG_MD']
gflaskMultiTH =  CONFIG_DICT['FLASK_MULTI_TH']

#-------<GLOBAL INSTANCES (start with "i")>-------------------------------------
# INSTANCES are the object.
iConnector = None
iDataMgr = None
