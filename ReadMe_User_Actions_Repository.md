# User Actions Repository

**Program Design Purpose**: 

[TOC]

### Introduction

The User Action Reposition is a library set which provide API can be invoked by the scheduler module in the User Action Emulator or used intendedly by customers’ own program. 

Currently we provide 5 main repositories with 18 kinds of basic user action functions and 28 kinds of pre-built complex user’s actors components. The 5 main feature repositories covers: 

- **Network traffic action generators**: Create different types of network traffic. 
- **Application operation action generators**: Control/interactive with other software/App to create specific program execution level activities.
- **User’s human activities action generators**. Simulate human’s action events such as mouse/keyboard operation. 
- **System control action generators**. Control/interactive with the system to create OS level activities. 
- **Other action generators**: Special action such as link to DB run SQL, read serial port Data or Open camera.



------

### System Design

Actor modules are the basic components to simulate one kind of normal user's  action such as file editing, surf the internet, access multi-media  and so on. 



#### **Network traffic action generators**

The network traffic action generators module will provide below lib functions:

| Index | **Actor module name**     | **Function provided**                                        | **Traffic/protocol type**     |
| ----- | ------------------------- | ------------------------------------------------------------ | ----------------------------- |
| 1     | pingActor                 | ping                                                         | ICMP                          |
| 2     | webActor                  | Fetch  a websites, send http(s) request.  •Surf  internet. Watch YouTube video. | http(s)                       |
| 3     | webDownloader             | Download  website components: https web cert, css, html, js, images, downloadable link. Page  screen shot | http(s), Page screen shot     |
| 4     | transferActor             | Upload  and download a file or Transfer  files via sftp. Copy  a file or directory to or from a nfs or smb share. | ftp(s), sftp, nfs/smb         |
| 5     | sshConnector/sshForwarder | ssh  connection or scp file transfer. Forward  traffic thought specified port. | ssh/scp                       |
| 6     | udpCom                    | Any  kinds of UDP message communication or file transfer.    | udp                           |
| 7     | tcpCom                    | Any  kinds of TCP message communication or file transfer.    | tcp                           |
| 8     | emailActor                | Email  receive and send (Gmail, Hotmail, Mailu)              | SMTP/IMAP4,POP,IMAP_SSL       |
| 7     | camEchoClient             | Real-Time  Streaming(IP camera) or HTTP Live Streaming such as video web  site. | RTSP / HLS                    |
| 8     | pcapReplayActor           | Parsing  pcap file and send the packet to the specific destination. | replaying send packet in pcap |
| 9     | telnetActor               | Remote  login/Open a telnet connection and issue commands.   | telnet                        |



#### **Application event actors repository** 

| **Index** | **Actor module name** | **Function provided**                          |
| --------- | --------------------- | ---------------------------------------------- |
| 1         | zoomActor             | Join/Start a zoom meeting                      |
| 2         | musicActor            | Search audio files and play one by one.        |
| 3         | VideoActor            | Search video/movie files and play one  by one. |
| 4         | msFileActor(Word)     | Create/edit MS-word(*.docx) file               |
| 5         | msFileActor(PPT)      | Create/edit MS-powerpoint(*.pptx) file         |
| 6         | msTeamsActor          | Join teams meeting, send a message.            |
| 7         | fileActor             | Check pdf file and parse the info.             |



#### **Human activities repository** 

| Index | **Actor module name**  | **Function provided**                                        |
| ----- | ---------------------- | ------------------------------------------------------------ |
| 1     | mouse_keyboard Actor   | Replay recorded user mouse +  keyboard action, Simulate user's mouse+keyboard action based on pre-config |
| 2     | TelegramActor          | Send message to phone by telegram                            |
| 3     | gameActor(dino/sudoku) | Play google dino game. play sudoku  game.                    |
| 4     | PaintActor             | Draw picture with MS-Paint app.                              |



#### **System Operation Actors** **Repository**

| **Index** | **Actor module name** | **Function provided**                                        |
| --------- | --------------------- | ------------------------------------------------------------ |
| 1         | CmdActor              | Run Window/Linux commend under cmd or PowerShell.            |
| 2         | SettingActor          | Change some OS setting (on/off  firewall, change display bg, sort desktop, reboot) |



#### **Other Action Repository**

| **Index** | **Actor module name** | **Function provided**                                        |
| --------- | --------------------- | ------------------------------------------------------------ |
| 1         | SerialConnector       | Send and read message to/from COM  port.                     |
| 2         | camEchoServer         | Computer built in camera/usb camera  video read record. Start a HLS server. |
| 3         | ScreanRecorder        | snapshot the screen under frequency.                         |
| 4         | DBHandler             | DataBase (SQLite3, influxDB, arangodb)  access action simulator. |



------

> Last edit by LiuYuancheng(liu_yuan_cheng@hotmail.com) at 03/02/2023, if you have any problem or find anu bug, please send me a message .