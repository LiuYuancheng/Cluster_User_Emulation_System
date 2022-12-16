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

# All the user's config file 
ACTOR_DIR = os.path.join(DIR_PATH, 'UtilsFunc')
ACTOR_CFG = os.path.join(ACTOR_DIR, 'BobConfig')

URL_RCD = os.path.join(ACTOR_CFG, 'urllist.txt')
RST_DIR = os.path.join(ACTOR_CFG, 'datasets')
URL_FN = os.path.join(ACTOR_CFG, 'info.txt')

YOUTUBE_CFG = os.path.join(ACTOR_CFG, 'youTubeList.txt')
WORD_FILE = os.path.join(ACTOR_DIR, 'Report.docx')
WORD_CFG = os.path.join(ACTOR_CFG, 'wordTextInput.txt')

PPT_FILE = os.path.join(ACTOR_DIR, 'Report.pptx')
PPT_CFG1 = os.path.join(ACTOR_CFG, 'pptxInput1.json.')

iScheduler = None
