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
from flask import Flask, render_template, request, flash, url_for, redirect

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
            gv.iDataMgr.addSchedulerPeer(peerInfo['name'], peerInfo['ipAddr'], peerInfo['udpPort'])
        except Exception as err:
            print("The peer's info line format Invalid: %s" %str(line))
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

taskInfoDict = {
    "connected" : gv.iDataMgr.schedulerConnected(),
    "updateT"   : None,
    "daily"     : [],
    "random"    : [],
    "weekly"    : []
} if TEST_MD else {} 

if TEST_MD:
    config_D = os.path.join(gv.dirpath, 'static', 'actionConfigD.json')
    config_R = os.path.join(gv.dirpath, 'static', 'actionConfigR.json')
    config_W = os.path.join(gv.dirpath, 'static', 'actionConfigW.json')

    configDist = {
        "daily": os.path.join(gv.dirpath, 'static', 'actionConfigD.json'),
        "random": os.path.join(gv.dirpath, 'static', 'actionConfigR.json'),
        "weekly": os.path.join(gv.dirpath, 'static', 'actionConfigW.json'),
    }

    for item in configDist.items():
        key, config = item
        if os.path.exists(config):
            try:
                with open(config, 'r') as fh:
                    taskInfoDict[key] = json.load(fh)
            except Exception as err:
                print("Failed to load the json config file: %s" % str(err))
                exit()

#-----------------------------------------------------------------------------
# web home request handling functions. 
@app.route('/')
def index():
    return render_template('index.html')

#-----------------------------------------------------------------------------
@app.route('/schedulermgmt')
def schedulermgmt():
    scheudlerInfoDict = gv.iDataMgr.getPeersInfo()
    print(scheudlerInfoDict)
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
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,  debug=False, threaded=True)
