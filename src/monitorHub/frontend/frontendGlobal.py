#-----------------------------------------------------------------------------
# Name:        frontGlobal.py
#
# Purpose:     This module is used as a local config file to set constants, 
#              global parameters which will be used in the other modules.
#              
# Author:      Yuancheng Liu
#
# Created:     2022/08/26
# Copyright:   National Cybersecurity R&D Laboratories
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
dirpath = os.path.dirname(__file__)
print("Current source code location : %s" % dirpath)
APP_NAME = ('NCL_BM_HUB', 'frontend')

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

#------<CONSTANTS>-------------------------------------------------------------
APP_NAME = 'Action_monitor_HUB [Ver:0.X]'

RC_TIME_OUT = 10    # reconnection time out.
BE_IP = ('127.0.0.1', 3001)     # backend server IP address.
APP_SEC_KEY = 'secrete-key-goes-here'

# define the keys
# user keys
USER_ID_KEY = 'id'
USER_EM_KEY = 'email'
USER_NA_KEY = 'userName'
USER_TP_KEY = 'authority'
USER_PW_KEY = 'password'

# CPU/GPU keys
ITEM_ID_KEY = 'id'
ITEM_SN_KEY = 'servername'
ITEM_IP_KEY = 'ipaddress'

ITEM_USR_KEY = 'userID'
ITEM_TM_KEY = 'updateT'
ITEM_STM_KEY = 'startT'
ITEM_ETM_KEY = 'endT'
ITEM_RQST_KEY = 'requestStatus'

GPU_TP_KEY = 'gpuType'
GPU_BK_KEY = 'bookID'
GPU_LD_KEY = 'gpuLoad'


ITEM_PWR_KEY = 'poweron' # Power on/off, for CPU
ITEM_PWRLVL_KEY = 'powerlvl' # Power level, for GPU

ITEM_LD_KEY = 'overload'
ITEM_CPULD_KEY = 'cpuload'
ITEM_MMRLD_KEY = 'memoryload'

ITEM_OS_KEY = 'ostype'
ITEM_GPU1_KEY = 'gpu1'
ITEM_GPU2_KEY = 'gpu2'

UPDATE_PERIODIC = 15
COOKIE_TIME = 30
#-------<GLOBAL VARIABLES (start with "g")>-------------------------------------
# VARIABLES are the built in data type.

#-------<GLOBAL INSTANCES (start with "i")>-------------------------------------
# INSTANCES are the object.
iConnector = None
iDataMgr = None