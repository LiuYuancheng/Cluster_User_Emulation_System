#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        pingClient.py
#
# Purpose:     This module will ping the destination ip/url dict periodically, save 
#              the ping result in local disk and report result to the server side.
#
# Author:      Yuancheng Liu
#
# Version:     v_0.1
# Created:     2022/10/12
# Copyright:   n.a
# License:     n.a
#-----------------------------------------------------------------------------

import time
import json
import requests
from pythonping import ping
from datetime import datetime
from statistics import mean

import clientGlobal as gv
# import the lib modules
import Log
import udpCom

TEST_MD = True  # Test mode flag.
serverIDaddr = ('127.0.0.1', 3001) if TEST_MD else gv.HUB_IP 
peerDict = gv.PEER_DICT
pingRst = {}    # ping result dict in the passed 5 mins
# UDP report connector
iConnector = udpCom.udpClient(serverIDaddr)
countT = gv.RPT_COUNT

#-----------------------------------------------------------------------------
def resetResult():
    global countT
    for k in peerDict.keys():
        pingRst[k] = []
    countT = gv.RPT_COUNT

#-----------------------------------------------------------------------------
def updateTeleBot():
    timeStr = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    msg = '\n'.join((
        'NCL-MPH Connection HUB report:', 
        'Time: %s' %timeStr,
        'During passed 5 min each peers avg ping are:'))
    for item in pingRst.items(): 
        key, val = item
        msg += str(' - '+ key +' : '+ str( round(mean(val),3))+' ms \n')
    try:
        url = f"https://api.telegram.org/bot{gv.BOT_TOKEN}/sendMessage?chat_id={gv.CHAT_ID}&text={msg}"
        requests.get(url).json()
    except Exception as e:
        Log.error('Report to telegram error:')
        Log.exception(str(e))

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main():
    global countT
    resetResult()
    #for _ in range(PING_TM):
    while True:
        # ping the peers one by one.
        crtPingRst = {} # current result
        for item in peerDict.items():
            key, val = item
            try:
                data = ping(val, timeout=gv.TIME_OUT, verbose=False)
                print(" Peer [%s] ping min: %s ms, avg: %s ms, max: %s ms" % (key, str(data.rtt_min_ms),  str(data.rtt_avg_ms), str(data.rtt_max_ms)))
                Log.info('[%s]: min:%s,avg:%s,max:%s', key, str(data.rtt_min_ms), str(data.rtt_avg_ms), str(data.rtt_max_ms))
                
                pingRst[key].append(data.rtt_avg_ms)
                crtPingRst[key] = (data.rtt_min_ms, data.rtt_avg_ms, data.rtt_max_ms)
                time.sleep(1)
            except Exception as e:
                Log.exception(e)
            
        # report the result to server
        msg = ';'.join(('REP', gv.OWN_ID, json.dumps(crtPingRst)))
        resp = iConnector.sendMsg(msg, resp=False)
        countT -= 1
        # call telegram API to message the reuslt to group 
        if countT == 0: updateTeleBot()
        time.sleep(gv.PING_INT)
    Log.info("Finished the ping test.")

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main()

