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
APP_NAME = ('Monitor_Hub', 'frontend')

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
APP_SEC_KEY = 'secrete-key-goes-here'
UPDATE_PERIODIC = 15
COOKIE_TIME = 30

#-------<GLOBAL VARIABLES (start with "g")>-------------------------------------
# VARIABLES are the built in data type.
gGonfigPath = os.path.join(dirpath, 'peerConfig.txt')

#-------<GLOBAL INSTANCES (start with "i")>-------------------------------------
# INSTANCES are the object.
iConnector = None
iDataMgr = None