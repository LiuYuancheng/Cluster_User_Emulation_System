#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        cueHubApp.py
#
# Purpose:     This module is the main website frontend host program to provide 
#              the web UI to monitor the scheduler's tasks information and state. 
#              We use python-flask and bootstrap5 to build the web UI.
#
# Author:      Yuancheng Liu
#
# Created:     2022/01/13
# version:     v0.2.3
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------
# CSS lib [bootstrap]: https://www.w3schools.com/bootstrap5/index.php

import json
from datetime import timedelta
from flask import Flask, render_template, request, url_for, redirect, jsonify

import dataManager
import cueHubGlobal as gv

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def InitDataMgr():
    """ Init the data manager and load the peer information."""
    gv.iDataMgr = dataManager.DataManager(None)
    # load the peer info
    for line in gv.iConfigLoader.getLines():
        try:
            if str(line).startswith('PEER:'):
                info = str(line).split('PEER:')[1].strip()
                peerInfo = json.loads(info)
                lkMode = int(peerInfo['lkMode']) if 'lkMode' in peerInfo.keys() else 0
                gv.iDataMgr.addSchedulerPeer(peerInfo['name'], peerInfo['ipAddr'], 
                                             peerInfo['udpPort'], linkMode=lkMode)
        except Exception as err:
            gv.gDebugPrint("The peer's info line format Invalid: %s" %str(line),
                           logType=gv.LOG_ERR)
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
    posts = {'page': 0} # page index is used to highlight the left page slide bar.
    return render_template('index.html', posts=posts)

#-----------------------------------------------------------------------------
@app.route('/schedulermgmt')
def schedulermgmt():
    schedulerInfoList = gv.iDataMgr.getPeersInfo()
    gv.gDebugPrint("Receive the peer Info %s" %
                   str(schedulerInfoList), logType=gv.LOG_INFO)
    posts = {'page': 1, 'schedulersInfo': schedulerInfoList}
    return render_template('schedulermgmt.html', posts=posts)

#-----------------------------------------------------------------------------
@app.route('/<int:postID>')
def peerstate(postID):
    peerInfoDict = dataManager.buildPeerInfoDict(postID)
    return render_template('peerstate.html', posts=peerInfoDict)
 
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
#-----------------------------------------------------------------------------
if __name__ == '__main__':
    #app.run(host="0.0.0.0", port=5000,  debug=False, threaded=True)
    app.run(host=gv.gflaskHost,
        port=gv.gflaskPort,
        debug=gv.gflaskDebug,
        threaded=gv.gflaskMultiTH)
