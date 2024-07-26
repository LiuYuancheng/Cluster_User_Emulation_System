#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        ftpComm.py
#
# Purpose:     This lib module will provide FTP Communication client and server
#              class for integrate in other program for file trafer.
# 
# Author:      Yuancheng Liu
#
# Created:     2024/07/23
# Version:     v_0.1.1
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------
""" Liborary Design:

    This lib module will provide FTP Communication client and server class for 
    integrate in other program for file trafer.
    - The server will use the pyftpdlib: https://pypi.org/project/pyftpdlib/
    - The client will use the ftplib: https://docs.python.org/3/library/ftplib.html
"""

import os
from ftplib import FTP
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler, ThrottledDTPHandler
from pyftpdlib.servers import FTPServer, ThreadedFTPServer  

# Default FTP connection port
DEF_FTP_PORT = 8081

DEF_PERM = 'elradfmwM'  # Default permission for user
# Read permissions:
# "e" = change directory (CWD, CDUP commands)
# "l" = list files (LIST, NLST, STAT, MLSD, MLST, SIZE commands)
# "r" = retrieve file from the server (RETR command)
# Write permissions:
# "a" = append data to an existing file (APPE command)
# "d" = delete file or directory (DELE, RMD commands)
# "f" = rename file or directory (RNFR, RNTO commands)
# "m" = create directory (MKD command)
# "w" = store a file to the server (STOR, STOU commands)
# "M" = change file mode / permission (SITE CHMOD command) New in 0.7.0
# "T" = change file modification time (SITE MFMT command) New in 1.5.3

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
DEF_USER = {
    'admin': {
        'passwd': '123456',
        'perm': DEF_PERM,
        'dirpath': os.path.join(DIR_PATH, 'ftpServer_data')
    }
}
# default max speed for client download
DEF_READ_MAX_SPEED = 300 * 1024  # 300 Kb/sec (30 * 1024)
# default max speed for client upload
DEF_WRITE_MAX_SPEED = 300 * 1024  # 300 Kb/sec (30 * 1024)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class ftpServer(object):
    """ FTP server class."""
    def __init__(self, rootDirPath, port=DEF_FTP_PORT, userDict=DEF_USER,
                 readMaxSp=DEF_READ_MAX_SPEED, writeMaxSp=DEF_WRITE_MAX_SPEED,
                 threadFlg=False):
        """ Init example:
            ftpServer('/', port=8081, userDict={'user':{'passwd':'123456','perm':ftpComm.DEF_FTP_PORT,'dirpath':'/home/user'}},
                readMaxSp=100000, writeMaxSp=100000,)
        Args:
            rootDirPath (str): The FTP host file storage root foler.
            port (int, optional): FTP server port. Defaults to DEF_FTP_PORT.
            userDict (dict, optional): Avaliable user dictionary. Defaults to DEF_USER.
            readMaxSp (int, optional): FTP client max allowed download speed(Kb). Defaults to DEF_READ_MAX_SPEED.
            writeMaxSp (_type_, optional): FTP client max allowed upload speed(Kb). Defaults to DEF_WRITE_MAX_SPEED.
            threadFlg (bool, optional): flag to identify whether can run the server in subthread. Defaults to False.
        """
        # Init the server basic parameters
        self._port = int(port)
        if not os.path.exists(rootDirPath): os.makedirs(rootDirPath)
        self._rootPath = rootDirPath
        self._user = userDict
        self._threadFlg = threadFlg

        # Instantiate a dummy authorizer for managing 'virtual' users
        self.authorizer = DummyAuthorizer()
        self._initAuthorization()
        
        # Initiate the throttled DTP handler class for uplad/download speed control
        self.dtphandler = ThrottledDTPHandler
        self.dtphandler.read_limit = int(readMaxSp)
        self.dtphandler.write_limit = int(writeMaxSp)

        # Instantiate FTP handler class
        self.handler = FTPHandler
        self.handler.authorizer = self.authorizer
        self.handler.dtp_handler = self.dtphandler

        # Define a customized banner (welcome string returned when client connects)
        self.handler.banner = "FTP server ready, license port: %s" % str(self._port)

        # Init the FTP server.
        address = ('0.0.0.0', self._port)
        self.server = None
        if self._threadFlg:
            self.server = ThreadedFTPServer(address, self.handler)
        else:
            self.server = FTPServer(address, self.handler)
        print("FTP server started to host on port: %s" % str(self._port))

    #-----------------------------------------------------------------------------
    def _initAuthorization(self):
        """ Initialize the user authorization and add user to the authorizer."""
        for user, info in self._user.items():
            userDir = info['dirpath'] if 'dirpath' in info.keys() else self._rootPath
            self.authorizer.add_user(user, info['passwd'], userDir, perm=info['perm'])
        self.authorizer.add_anonymous(os.getcwd())

    #-----------------------------------------------------------------------------
    def addUser(self, user, passwd, dirpath=None, perm='elradfmwM'):
        """ Add a new user to the server.
            Args:
                user (str): unique user name.
                passwd (str): user login password.
                dirpath (path, optional): user own home dir under root dir. Defaults to None.
                perm (str, optional): permission. Defaults to 'elradfmwM'.
            Returns:
                bool: True if use is added successful, False if user already exists or add failed.
        """
        if user in self._user.keys():
            print("addUser(): User %s already exists" % user)
            return False
        self._user[user] = {'passwd': passwd, 'dirpath': dirpath, 'perm': perm}
        if dirpath is None: dirpath = self._rootPath
        self.authorizer.add_user(user, passwd, dirpath, perm=perm)
        print("addUser(): User [%s] is added." % user)
        return True

    #-----------------------------------------------------------------------------
    def getCurrentUsersInfo(self):
        return self._user

    #-----------------------------------------------------------------------------
    def removeUser(self, userName):
        """ Remove a user from the server authorizer."""
        if userName not in self._user.keys():
            print("removeUser(): User %s does not exist" % userName)
            return False
        self.authorizer.remove_user(userName)
        del self._user[userName]
        print("removeUser(): User %s removed" % userName)
        return True
    
    #-----------------------------------------------------------------------------
    def startServer(self):
        """ Start the FTP server."""
        print("Starting FTP server...")
        if self.server is not None: self.server.serve_forever()
        print("FTF server stopped")

    #-----------------------------------------------------------------------------
    def stopServer(self):
        """ Stop the FTP server."""
        print("Stopping FTP server...")
        if self.server is not None: self.server.close_all()
        print("FTF server stopped")

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class ftpClient(object):
    """ FTP client class for file transfer."""

    def __init__(self, host, port, user, pwd):
        """ Init example:
            client = ftpComm.ftpClient('127.0.0.1', 8081, 'admin', '123456')
            Args:
                host (str): ftp server ip address.
                port (int): ftp server port.
                user (str): user name to login the ftp server.
                pwd (str): password to login the ftp server.
        """
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.client = FTP()
        self.connected = False
        print("Ftp client inited.")

    #-----------------------------------------------------------------------------
    def getConnectionStatus(self): 
        return self.connected

    #-----------------------------------------------------------------------------
    def connectToServer(self):
        """ Connect to FTP server. """
        try:
            self.client.connect(self.host, self.port)
            self.client.login(self.user, self.pwd)
            print(self.client.getwelcome())
            self.connected = True
            return True
        except Exception as err:
            print("ftpClient() connect to server Error: %s" %str(err))
            self.connected = False
            return False

    #-----------------------------------------------------------------------------
    def createDir(self, dirname):
        """ Create directory on FTP server under current directory."""
        self.client.mkd(dirname)

    #-----------------------------------------------------------------------------
    def swithToDir(self, dir):
        """ Switch to the target directory. """
        self.client.cwd(dir)

    #-----------------------------------------------------------------------------
    def listDirInfo(self, detail=False):
        """ List directory information on FTP server under current directory.
            detail == True: return a list of the file or dir.
            detail == False : return folder detail information such as: 
                -rw-rw-rw-   1 owner    group      336512 Mar 09  2023 Hacking.pdf
                drwxrwxrwx   1 owner    group           0 Jul 24 08:54 Test
                drwxrwxrwx   1 owner    group           0 Jul 23 09:57 client1
        """
        if detail:
            return self.client.dir()
        else:
            return self.client.nlst()

    #-----------------------------------------------------------------------------
    def uploadFile(self, localFile, remoteFile):
        """ Upload local file to FTP server side's current directory.
            Args:
                localFile (str): local file path.
                remoteFile (str): remote file name.
            Returns:
                bool: True if upload successful, else false.
        """
        if not os.path.exists(localFile):
            print("Error: uploadFile()> local file not exist: %s" %str(localFile))
            return False
        try:
            self.client.storbinary('STOR ' + remoteFile, open(localFile, 'rb'))
            return True
        except Exception as err:
            print("ftpClient() upload file Error: %s" %str(err))
            return False

    #-----------------------------------------------------------------------------
    def downloadFile(self, remoteFile, localFile):
        """ Download file from FTP server side's current directory to local. """
        try:
            self.client.retrbinary('RETR ' + remoteFile, open(localFile, 'wb').write)
            return True
        except Exception as err:
            print("ftpClient() download file Error: %s" %str(err))
            return False

    #-----------------------------------------------------------------------------
    def close(self):
        self.client.quit()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main():
    print("Input the program you want to run: [1]FTP Client [2]FTP Server")
    choice = int(input())
    if choice == 1:
        print("Init FTP Client")
        serverIP = input("Input Connected server IP:")
        serverPort = int(input("Input Connected server port:"))
        userName = input("Input Connected server username:")
        password = input("Input Connected server password:")
        client = ftpClient(serverIP, serverPort, userName, password)
        client.connectToServer()
        while True:
            print("Input the program you want to run:[0]Swith to Dir [1]Upload [2]Download [3]List dir [4]exit")
            choice = int(input())
            if choice == 0:
                dir = input("Input dir:")
                client.swithToDir(dir)
            elif choice == 1:
                localFile = input("Input local file path:")
                remoteFile = input("Input remote file name:")
                client.uploadFile(localFile, remoteFile)
            elif choice == 2:
                remoteFile = input("Input remote file name:")
                localFile = input("Input local file path:")
                client.downloadFile(remoteFile, localFile)
            elif choice == 3:
                print(client.listDirInfo(detail=True))
            else:
                print("exit...")
                break
        client.close()
    elif choice == 2:
        print("Init FTP Server")
        serverPort = int(input("Input Connected server port:"))
        dir = os.path.join(DIR_PATH, 'ftpServer_data')
        server = ftpServer(dir, port=serverPort, threadFlg=True)
        server.startServer()
    print("exit...")

#-----------------------------------------------------------------------------
if __name__ == "__main__":
    main()