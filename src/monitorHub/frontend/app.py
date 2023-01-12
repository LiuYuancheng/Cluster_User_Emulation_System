#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        app.py [python3]
#
# Purpose:     This module is the main website host program to host the webpage 
#              by using Flask frame work. 
#  
# Author:      Yuancheng Liu
#
# Created:     2022/08/27
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
from flask_login import LoginManager, login_required, current_user
from werkzeug.exceptions import abort

import frontendGlobal as gv

# Init the flask web app program.
def createApp():
    """ Connect to the monitor hub server and init the flask.app.
        Returns:
            _type_: flask.app()
    """
    print("Check whether can connect to the monitor-hub backend server:")
    
    # Try to connect to the monitor-hub backend server.
    #gv.iDataMgr = dataManager.DataManager(None)
    #if not gv.iDataMgr: exit()
    #gv.iDataMgr.start()

    # init the web host
    app = Flask(__name__)
    app.config['SECRET_KEY'] = gv.APP_SEC_KEY
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=gv.COOKIE_TIME)
    return app


app = createApp()
dataDict = {
    "daily":[],
    "random":[],
    "weekly":[]
}

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
                dataDict[key] = json.load(fh)
        except Exception as err:
            print("Failed to load the json config file: %s" % str(err))
            exit()

#-----------------------------------------------------------------------------
# web home request handling functions.
@app.route('/')
def index():
    #Log.info('/index.html is accessed from IP: %s' %str(request.remote_addr))
    posts = [{
        'id': 1,
        'name': "09:01_ping",
        'detail':"Ping 100+ destinations",
        'owner': "User:LYC",
        'startT': "Every 1 day at 09:01:00",
        'period': '10 mins',
        'type':0,
        'dep':0,
        'state':1,
        'nextT': "2023-01-04 09:01:00"
    }]
    return render_template('index.html', posts=dataDict)

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,  debug=False, threaded=True)
