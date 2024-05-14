#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        databaseHandler.py
#
# Purpose:     This module will provide several database clients to connect to 
#              different kinds of database to implement query execution, table 
#              create, data insert, update and delete. 
#              
#
# Author:      Yuancheng Liu
#
# Created:     2023/03/19
# Version:     v_0.1.1
# Copyright:   Copyright (c) 2023 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

import os
import sqlite3

# incluxdb Doc: https://influxdb-python.readthedocs.io/en/latest/examples.html
from influxdb import InfluxDBClient

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class dbHandler(object):
    """ Root class of the database clients. """
    def __init__(self, databaseName=None) -> None:
        self.dbConnected = False
        self._testConnect()
        if self.dbConnected: 
            print("Database [%s] handler inited." %str(databaseName))
        else:
            print("Database [%s] handler init fail: DB connection error." %str(databaseName))

    def _testConnect(self):
        if self.getTableList(): self.dbConnected = True

    def createTable(self, tableName):
        return None 

    def getTableList(self):
        return None 

    def dropTable(self, tableName):
        return None
    
    def executeQuery(self, queryStr):
        return None

    def close(self):
        self.dbConnected = False

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class Sqlite3Cli(dbHandler):
    """ Client to connect to Sqlite3 database."""
    def __init__(self, dbPath, databaseName=None, threadSafe=True, rowFac=None) -> None:
        """ Init the client. Init example:
            dbhandler = Sqlite3Cli('database.db', databaseName ='testdb',threadSafe=False, rowFac=sqlite3.Row )
        Args:
            dbPath (_type_): sqlite3 database path.
            databaseName (_type_, optional): Name of the DB. Defaults to None.
            threadSafe (bool, optional): flag to check_same_thread, if you want the client
                be used in different thread, set the val to False. Defaults to True.
            rowFac (_type_, optional): select row factor. Defaults to None.
        """
        if not os.path.exists(dbPath):
            print("Error: sqlite3DB file %s not exist, exit() called..." %str(dbPath))
            exit()
        self.dbPath = dbPath
        self.rowFactor = rowFac
        self.threadSafe = threadSafe
        self.dbConn = None  # data base connector
        self.dbCursor = None
        super().__init__(databaseName)

    #-----------------------------------------------------------------------------
    def _initConn(self):
        try:
            self.dbConn = sqlite3.connect(self.dbPath, check_same_thread=self.threadSafe)
            if self.rowFactor: self.dbConn.row_factory = self.rowFactor
            self.dbCursor = self.dbConn.cursor()
            return True
        except Exception as err:
            print("Error to connect to dataabse: %s" %str(err))
            return False
    
    def reInitConn(self):
        if self.dbConn: self.close()
        self._initConn()

    #-----------------------------------------------------------------------------
    def _testConnect(self):
        self.dbConnected = self._initConn()

    #-----------------------------------------------------------------------------
    def getTableList(self):
        queryStr = """SELECT name FROM sqlite_master WHERE type='table';"""
        self.executeQuery(queryStr)
        result = self.dbCursor.fetchall()
        return result

    #-----------------------------------------------------------------------------
    def getCursor(self):
        if self.dbConnected and self.dbCursor: return self.dbCursor
        return None

    #-----------------------------------------------------------------------------
    def executeQuery(self, queryStr, paramList=None):
        """ 
        Args:
            queryStr (str): query string
            paramList (tuple, optional): paramter tuple. Defaults to None.
        """
        if paramList and isinstance(paramList, tuple):
            self.dbCursor.execute(queryStr, paramList)
        else:
            self.dbCursor.execute(queryStr)
        self.dbConn.commit()

    #-----------------------------------------------------------------------------
    def executeScript(self, scriptPath):
        with open(scriptPath) as fh:
            self.dbConn.executescript(fh.read())
        self.dbConn.commit()

    #-----------------------------------------------------------------------------
    def close(self):
        self.dbConn.close()
        self.dbConn = None
        return super().close()
        
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class InfluxDB1Cli(dbHandler):
    """ Client to connect to the influxDB1.8X and insert data to single DB."""

    def __init__(self, ipAddr=None, dbInfo=None) -> None:
        """ Init the influxDB1.X client to login to the data base. dbInfo: name, 
            password, databaseName. init example: 
            client = InfluxCli(ipAddr=('127.0.0.1', 8086), dbinfo=('root', 'root', 'gatewayDB'))
        """
        (ip, port) = ipAddr if ipAddr else ('localhost', 8086)
        (user, pwd, dbName) = dbInfo if dbInfo and len(
            dbInfo) == 3 else ('root', 'root', 'gatewayDB')
        #self.dbClient = InfluxDBClient('localhost', 8086, 'root', 'root', 'quantumGWDB')
        # link to data base:
        self.defaultTag = {"Name": "time"}
        try:
            self.dbClient = InfluxDBClient(ip, port, user, pwd, dbName)
        except Exception as e:
            print("Can not connect to the data base, please check whether the influxDB service is running. \n" 
                + "- Windows:   go to D:\\Tools\\InfluxDB\\influxdb-1.8.1-1 and run influxd.exe \n"
                + "- Ubuntu:    sudo systemctl start influxdb")
            exit()
        super().__init__(databaseName='InfluxDB1.8.1')

    #-----------------------------------------------------------------------------
    def insertFields(self, measurement, fieldDict, tags=None, timeStr=None):
        """ Insert the fileds to a measurement immediately."""
        if not self.dbConnected: return False
        dataJoson = {   "measurement": str(measurement),
                        "tags": self.defaultTag if tags is None else tags,
                        "fields": fieldDict
                    }
        if timeStr: dataJoson['time'] = timeStr
        return self.insertPoints([dataJoson])

    #-----------------------------------------------------------------------------
    def insertPoints(self, pointList):
        try:
            return self.dbClient.write_points(pointList)
        except Exception as err:
            print("Error to write points: %s " %str(pointList))
            print("Exception: %s " %str(err))
            return False
        
    #-----------------------------------------------------------------------------
    def dropTable(self, tableName):
        if self.dbConnected: self.dbClient.drop_measurement(tableName)
        return self.dbConnected

    #-----------------------------------------------------------------------------
    def executeQuery(self, queryStr, bind_params=None):
        if self.dbConnected:
            bindParams = self.defaultTag if bind_params is None else bind_params
            return self.dbClient.query(queryStr, bind_params=bindParams)
        return None

    #-----------------------------------------------------------------------------
    def getTableList(self):
        try:
            if self.dbClient.ping(): return self.dbClient.get_list_measurements()
            print("InfluxDB server does not response ping() ")
            return None
        except:
            print("InfluxDB server connection error ")
            return None

    #-----------------------------------------------------------------------------
    def setDefaultTag(self, tagJson):
        self.defaultTag = tagJson

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------