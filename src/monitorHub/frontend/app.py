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
from http import server
from flask import Flask, render_template, request, flash, url_for, redirect

import dataManager
import frontendGlobal as gv

TEST_MD = False

# Init the flask web app program.
def createApp():
    """ Connect to the monitor hub server and init the flask.app.
        Returns:
            _type_: flask.app()
    """
    print("Check whether can connect to the monitor-hub backend server:")
    
    # Try to connect to the monitor-hub backend server.
    gv.iDataMgr = dataManager.DataManager(None)
    bobName = 'Bob'
    bobIp = '127.0.0.1'
    bobPort = 3001
    gv.iDataMgr.addSchedulerPeer(bobName, bobIp, bobPort)

    # init the web host
    app = Flask(__name__)
    app.config['SECRET_KEY'] = gv.APP_SEC_KEY
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=gv.COOKIE_TIME)
    return app

app = createApp()

taskInfoDict = {
    "connected" : gv.iDataMgr.schedulerConnected(),
    "updateT"   : None,
    "daily"     : [],
    "random"    : [],
    "weekly"    : []
} if TEST_MD else None 

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
    taskInfoDict = gv.iDataMgr.getPeerTaskInfo('Bob', 'all')

    return render_template('index.html', posts=taskInfoDict)

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,  debug=False, threaded=True)
