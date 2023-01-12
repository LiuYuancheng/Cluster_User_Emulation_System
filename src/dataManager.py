#-----------------------------------------------------------------------------
# Name:        dataManage.py
#
# Purpose:     Data manager class to store the specific functions and init the 
#              data class.
#              
# Author:      Yuancheng Liu 
#
# Version:     v_0.1
# Created:     2023/01/11
# Copyright:   
# License:     
#-----------------------------------------------------------------------------

import time
import datetime
import threading
import sqlite3

import actionGlobal as gv

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class DataManager(threading.Thread):

    def __init__(self, parent) -> None:
        threading.Thread.__init__(self)
        self.dbConn = None
        self.parent = parent
        self.terminate = False
        self.lastUpdate = datetime.now()

    #-----------------------------------------------------------------------------
    def run(self):
        """ Thread run() function call by start(). """
        time.sleep(1)  
        while not self.terminate:
            print('Do the daily database backup and update')
            Log.info('Do the daily database backup and update')
            self._checkGpuRequest()
            time.sleep(gv.ONE_HOUR)

    def _getDBconnection(self):
        conn = sqlite3.connect(gv.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn