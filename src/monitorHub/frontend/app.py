#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        app.py [python3]
#
# Purpose:     This module is the main website host program to host the scheduled
#              tasks monitor Hub webpage by using python-Flask frame work. 
#  
# Author:      Yuancheng Liu
#
# Created:     2022/01/13
# version:     v0.2
# Copyright:   National Cybersecurity R&D Laboratories
# License:     
#-----------------------------------------------------------------------------

# CSS lib [bootstrap]: https://www.w3schools.com/bootstrap4/default.asp

# https://www.w3schools.com/howto/howto_css_form_on_image.asp

import os
import json

from datetime import timedelta, datetime
from flask import Flask, render_template, request, flash, url_for, redirect, jsonify

import dataManager
import frontendGlobal as gv
import ConfigLoader

TEST_MD = False # Test mode flag.

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def InitDataMgr():
    gv.iDataMgr = dataManager.DataManager(None)
    ld = ConfigLoader.ConfigLoader(gv.gGonfigPath, mode='r')
    for line in ld.getLines():
        try:
            peerInfo = json.loads(line)
            lkMode = int(peerInfo['lkMode']) if 'lkMode' in peerInfo.keys() else 0
            gv.iDataMgr.addSchedulerPeer(peerInfo['name'], peerInfo['ipAddr'], peerInfo['udpPort'], 
                                         linkMode=lkMode)
        except Exception as err:
            gv.gDebugPrint("The peer's info line format Invalid: %s" %str(line), logType=gv.LOG_ERR)
            continue

#-----------------------------------------------------------------------------
# Init the flask web app program.
def createApp():
    """ Create the flask App."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = gv.APP_SEC_KEY
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=gv.COOKIE_TIME)
    return app

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
InitDataMgr()
app = createApp()

#-----------------------------------------------------------------------------
# web home request handling functions. 
@app.route('/')
def index():
    return render_template('index.html')

#-----------------------------------------------------------------------------
@app.route('/schedulermgmt')
def schedulermgmt():
    scheudlerInfoDict = gv.iDataMgr.getPeersInfo()
    gv.gDebugPrint("Receive the peer Info %s" %str(scheudlerInfoDict), logType=gv.LOG_INFO)
    return render_template('schedulermgmt.html', posts=scheudlerInfoDict)

#-----------------------------------------------------------------------------
@app.route('/<int:postID>')
def peerstate(postID):
    peerInfoDict = dataManager.buildPeerInfoDict(postID)
    return render_template('peerstate.html',posts=peerInfoDict)
 
#-----------------------------------------------------------------------------
@app.route('/<string:peerName>/<int:jobID>/<string:action>', methods=('POST',))
def changeTask(peerName, jobID, action):
    peerInfo = gv.iDataMgr.getOnePeerDetail(peerName)
    posts = gv.iDataMgr.changeTaskState(peerName, jobID, action)
    return redirect(url_for('peerstate', postID=peerInfo['id']))


#-----------------------------------------------------------------------------
# Data post request handling 
@app.route('/dataPost/<string:peerName>', methods=('POST',))
def peerRegister(peerName):
    """ handler the schduler register request."""
    content = request.json
    gv.gDebugPrint("Get raw data from %s "%str(peerName), logType=gv.LOG_INFO)
    gv.gDebugPrint("Raw Data: %s" %str(content), prt=True, logType=gv.LOG_INFO)
    if gv.iDataMgr:
        lkMode = 1 if content['report'] else 0
        gv.iDataMgr.addSchedulerPeer(content['name'], content['ipAddr'], content['udpPort'], 
                                linkMode=lkMode)
        gv.gDebugPrint("Added new schudler: %s" %str(peerName), prt=True, logType=gv.LOG_INFO)
    return jsonify({"ok":True})

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,  debug=False, threaded=True)
