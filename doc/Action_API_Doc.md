# CUE Organic Actions API Document

This user API module will introduce the Organic Actions mapping with the related lib and program code API and give a simple example. 

[TOC]

------

### Network Activities Module



#### Action 01 : Ping targets sequence or parallel

Source code module: `pingActor.py`

**API Usage :**

Init the ping actor obj:  

```
actor = pingActor({'127.0.0.1':10},parallel=True, Log=None, showConsole=False)
```

 Pass in parameters:

- `config` (dict): Ping destination config dictionary or the dictionary json file path. json item format `'dest ip/url': int(pingtime)`
- `parallel` (bool, optional): Ping the dest in sequential if val==False or parallel threading  (multi-thread) if val==True. Defaults to False.
- `Log` (_type_, optional): A logger object used to log the result to local if necessary.  Defaults to None.
- `showConsole` (bool, optional): Flag to identify whether pop-up the OS console. Defaults to False.

Start ping action:

```
result = actor.runPing()
print(result)
```

Pass in parameters: `None`



#### Action 02: Capture webpage screen shot

Source code module: `WebScreenShoter.py`

**API Usage :**

Init the pyWebscreenshoter obj:  

```
capturer = webScreenShoter()
```

Pass in parameters: `None`

Start capture:

```
capturer.getScreenShot(url, outputFolder, driverMode=driverMode)
```

Pass in parameters: 

- `urlList` (list/tuple): url string list.
- `outDirPath` (str): output directory path.
- `driverMode` (int, optional): driver selection. Defaults to QT_DRIVER.



#### Action 03: Download all the contents in a web page

Source code module: `webDownloader.py`

Function: provide API to download the webpage components: html file, image file, javascript file, href link file, host SSL certificate and xml file based on the input url.

**API Usage :**

Init the webDownloader obj:  

```
downloader = webDownloader(imgFlg=True, linkFlg=True, scriptFlg=True, caFlg=True)
```

Pass in parameters: 

- `imgFlg` (bool, optional): flag to identify whether download image. Defaults to True.
- `linkFlg` (bool, optional): flag to identify whether download all the hyper link contents. Defaults to True.
- `scriptFlg` (bool, optional): flag to identify whether download script. Defaults to True.
- `caFlg` (bool, optional): flag to identify whether download certificate. Defaults to True.

Download contents:

```
downloader.downloadWebContents(urlStr, downloadFolderPath)
```

Pass in parameters:

- `urlStr` (str): url string.
- `outputDirPath` (str): output folder path.



#### Action 04: Connect to FTP server

Source code module: `networkServiceProber.py`

**API Usage:** 

Connect to FTP server: 

```
checkFtpConn(self, target, loginConfig=None, timeout=3)
```

Pass in parameters:

- `target` (str): IP-address/domain-name
- `loginConfig` (dict, optional): {'user':str, 'password':str}. Defaults to None.
- `timeout` (int, optional): connection timeout.. Defaults to 3.



#### Action 05: SSH connect to target and run command

Source code: `SSHconnector.py`

**API Usage:**

Init the ssh connector obj:

```
mainInfo = ('gateway.ncl.sg', 'xxxxxx', '*******')
mainHost = sshConnector(None, mainInfo[0], mainInfo[1], mainInfo[2])
```

Pass in parameters:

- `parent` (sshConnector or paramiko.SSHClient: parent ssh client.
- `host` (str): host ip address or host domain name.
- `username` (str): username.
- `password` (str): user password.
- `port` (int, optional): ssh port. Defaults to 22.

Run command on target host

```
mainHost.addCmd('pwd', test1RplyHandleFun)
mainHost.InitTunnel()
mainHost.runCmd(interval=0.1)
```

Pass in parameters:

- `cmdline` (string): command line string.
- `handleFun`: a function use to handle the command response. default use None. Below reply dict will be passed in the handle function.
- `interval` (float, optional): Sleep time after time interval (unit second). Defaults to None.



#### Action 06: SCP file to target

Source code: `SCPconnector.py`

**API Usage:**

Init the scp connector obj:

```
scpClient = scpConnector(destInfo, showProgress=True)
```

Pass in parameters:

- `destInfo` (tuple): The destation host's ssh login information. example: (sshHost(ip/domain), userName, password) 
- `jumpChain` (list, optional): The jump host chain ssh info:scpConnectorHost ---> jumphost1 ---> jumphost2---> ... ---> destinationHost[jumphost1Infor, jumphost2Info]. example: [(JumpHost1_ip, userName, password),  (JumpHost2_ip, userName, password) ...] Defaults to None.
- `showProgress` (bool, optional): Flag to identify whether show the file transmission progress. Defaults to False, better to set True when transfer big file.

Upload  file:

```
scpClient.uploadFile('scpTest.txt', '~/scpTest2.txt')
```

Pass in parameters:

- `srcPath` (str): source file path.
- `destPath` (str): destination file path.

Download file:

```
scpClient.downFile('~/scpTest2.txt')
```

Pass in parameters:

- `srcPath` (str): destination host file path.
- `localPath` (str, optional): local path. Defaults set same as the program folder.



#### Action 07: SSH port forward to local

Source code: `SSHforwarder.py`

**API Usage:**

Init the ssh forwarder obj:

```
forwarder = localForwarder(localport, remoteHost[0], remoteHost[1])
```

Pass in parameters:

```
def __init__(self, localPort, remoteHost, remotePort, remoteUser=None, remotePwd=None) -> None:
```

- `localPort` (int): local port 
- `remoteHost` (str): target remote host address.
- `remotePort` (str): target remote host's port need to be forwarded to local.
- `remoteUser` (str, optional): remote host username. Defaults to None.
- `remotePwd` (str, optional): remote host password. Defaults to None.

Start forward:

```
gw = {  'address': 'gateway.ncl.sg',
    'user': 'xxxxx',
    'password': '********'
	}
forwarder.addNextJH(gw['address'], gw['user'], gw['password'])
print(forwarder.getJsonInfo())
forwarder.startForward()
```

Pass in parameters: `None`



#### Action 08: UDP connect to the target

Source code: `udpCom.py`

**API Usage:**

Init the UDP client obj:

```
client = udpClient((ipAddr, udpPort))
```

Pass in parameters:

- `ipAddr` (str, int): IP address and UDP port

Send message:

```
resp = client.sendMsg(msg, resp=True)
```

Pass in parameters:

- `msg` (str): UDP message string
- `resp` (bool): server response flag, method will wait server's response and return the bytes format response if it is set to True.  



#### Action 09: TCP connect to the target

Source code: `tcpCom.py`

**API Usage:**

Init the TCP client obj:

```
client = tcpClient(('127.0.0.1', 502))
```

Pass in parameters:

- `ipAddr` (str, int): IP address and UDP port

Send message:

```
resp = client.sendMsg(msg, resp=True)
```

Pass in parameters:

- `msg` (str): TCP message string
- `resp` (bool): server response flag, method will wait server's response and return the bytes format response if it is set to True.  



#### Action 10: Connect to SQLite3 Database

Source code: `databaseHandler.py`

**API Usage:**

Init the SQLite3 connector obj:

```
dbhandler = Sqlite3Cli('database.db', databaseName ='testdb',threadSafe=False, rowFac=sqlite3.Row )
```

Pass in parameters:

- `dbPath` (str): sqlite3 database local path or connection url.
- `databaseName` (str, optional): Name of the DB. Defaults to None.
- `threadSafe` (bool, optional): flag to check_same_thread, if you want the client be used in different thread, set the val to False. Defaults to True.
- `rowFac` (_type_, optional): select row factor. Defaults to None.

Run SQL query string:

```
executeQuery(self, queryStr, paramList=None)
```

Pass in parameters:

- `queryStr` (str): query string
- `paramList` (tuple, optional): parameter tuple. Defaults to None.

Run SQL query script;

```
executeScript(self, scriptPath)
```

Pass in parameters:

- `scriptPath` (str): query script file path.





------

>Last edit by LiuYuancheng (liu_yuan_cheng@hotmail.com) at 12/05/2024, if you have any problem or find anu bug, please send me a message .

