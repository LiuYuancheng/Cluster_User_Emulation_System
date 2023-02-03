#-----------------------------------------------------------------------------
# Name:        frontGlobal.py
#
# Purpose:     This module is used as a local config file to set constants, 
#              global parameters which will be used in the other modules.
#              
# Author:      Yuancheng Liu
#
# Created:     2022/08/26
# Copyright:   N.A
# License:     
#-----------------------------------------------------------------------------
"""
For good coding practice, follow the following naming convention:
    1) Global variables should be defined with initial character 'g'
    2) Global instances should be defined with initial character 'i'
    2) Global CONSTANTS should be defined with UPPER_CASE letters
"""

import os, sys
import json

print("Current working directory is : %s" % os.getcwd())
dirpath = os.path.dirname(__file__)
print("Current source code location : %s" % dirpath)
APP_NAME = ('pingClient', 'ping')

TOPDIR = 'src'
LIBDIR = 'lib'

idx = dirpath.find(TOPDIR)
gTopDir = dirpath[:idx + len(TOPDIR)] if idx != -1 else dirpath   # found it - truncate right after TOPDIR
# Config the lib folder 
gLibDir = os.path.join(gTopDir, LIBDIR)
if os.path.exists(gLibDir):
    sys.path.insert(0, gLibDir)

# init the logger
import Log
Log.initLogger(gTopDir, 'Logs', APP_NAME[0], APP_NAME[1], historyCnt=100, fPutLogsUnderDate=True)

# init the config file loader
import ConfigLoader
CFG_FILE = os.path.join(gTopDir, 'clientConfig.txt')
iCfgDict = ConfigLoader.ConfigLoader(CFG_FILE, mode='r').getJson()

# Get OWN ID
OWN_ID = iCfgDict['own_id']

# server hub config 
HUB_IP = eval(iCfgDict['hub_ipAddress'])
PING_INT = int(iCfgDict['ping_interval'])   # interval(sec) between 2 ping action.

# Telegram config
BOT_TOKEN = iCfgDict['bot_token']
CHAT_ID = iCfgDict['chat_id']
RPT_COUNT = int(iCfgDict['report_count'])

# ping peer config
TIME_OUT = int(iCfgDict['time_out'])
PEER_JSON = os.path.join(gTopDir, iCfgDict['ping_peers'])
PEER_DICT = None
with open(PEER_JSON, 'r') as fh:
    PEER_DICT = json.load(fh)
