### User Action Timeline 

BOB

| Idx  | Time  | State   | Task                    | Detail                                          |      |      |
| ---- | ----- | ------- | ----------------------- | ----------------------------------------------- | ---- | ---- |
| 1    | 9:01  | pending | 09:01_ping              | Ping 30 destinations                            |      |      |
| 2    | 9:10  | pending | 09:10_ping[MT]          | Ping 100+ destinations                          |      |      |
| 3    | 9:13  | pending | 09:13_cmdRun            | Run Win_Network cmds                            |      |      |
| 4    | 9:20  | pending | 09:20_sshTest           | SSH login to NCL server run cmds                |      |      |
| 5    | 9:32  | pending | 09:32_FileSearch        | Search User dir to file and files.              |      |      |
| 6    | 9:35  | pending | 09:35_Zoom              | Open the Zoom and join meeting.                 |      |      |
| 7    | 10:03 | pending | 10:03_CheckEmail        | Check unread email.                             |      |      |
| 8    | 10:15 | pending | 10:15_DownloadWeb       | Follow urls list to download all the  contents. |      |      |
| 9    | 10:32 | running | 10:32_YouTube           | Watch some youTube videos                       |      |      |
| 10   | 10:50 | running | 10:50_EditMs-Word       | Create and edit MS-Word Doc.                    |      |      |
| 11   | 11:25 | pending | 11:25_EditMs-PowerPoint | Create and edit MS-PPT Doc.                     |      |      |
| 12   | 11:35 | pending | 11:35_PlayGame          | Open Chrome and play Dino Game.                 |      |      |
| 13   | 13:10 | pending | 13:10_Ping_subnet2      | Ping ip addresses in subnet2                    |      |      |
| 14   | 13:35 | finish  | 13:45_SSH_subnet2       | SSH to hosts in subnet2                         |      |      |
| 15   | 14:10 | running | 14:10_TrunOff_FW        | Turn off Windows FW.                            |      |      |
| 16   | 14:30 | finish  | 14:30_Webdownload       | Download some thing from webs dict              |      |      |
| 17   | 14:50 | pending | 14:50_UDP communication | Send message/file by UDP                        |      |      |
| 18   | 15:15 | pending | 15:15_EditMs-PowerPoint | Find and edit MS-PPT Doc                        |      |      |
| 19   | 15:20 | error   | 15:20_Play game         | Play a game                                     |      |      |
| 20   | 15:40 | pending | 15:40_SendEmail         | Send emails                                     |      |      |
| 21   | 16:00 | pending | 16:00_WatchVideo        | Open a video file.                              |      |      |
| 22   | 16:35 | pending | 16:35_CheckPictures     | Check pictures in folder.                       |      |      |
| 23   | 17:00 | pending | 17:00_UDP communication | Send message/file by UDP.                       |      |      |
| 24   | 17:35 | pending | 17:35_Write Report      | Bob finished his report.                        |      |      |



Bob is a system technical support officer. He login his Windows server at 8:50 am

| Time  | Action                                                       | action time (testCase setting) | current progress                |
| ----- | ------------------------------------------------------------ | ------------------------------ | ------------------------------- |
| 9:01  | Ping a servers list to check the server's connection. (open console ping the dest one by one, sequential ) | 10 min                         | done                            |
| 9:10  | Bob runs the ping client program ping 100 servers need to check and record down the result.(run pingClient.py, multi-thread parallel ping) | 10 min                         | done                            |
| 9:13  | During watching the ping result refresh, bob run server network checking cmd in terminal one by one (ipconfig, Tracert www.google.com.sg , Pathping www.google.com.sg, Getmac, Nslookup www.google.com.sg) | 5 min                          | done                            |
| 9:20  | Bob ssh to 12 Ubuntu servers and run some cmd  record done the result.(run sshConnector.py do server one by one sequential) | 12min                          | done                            |
| 9:32  | Bob use "Tree" cmd to search some files.                     | 2 min                          | done                            |
| 9:35  | Bob start a zoom meeting with his colleague to discuss for half hour | 30 min                         | done                            |
| 10:05 | Write down and draw some diagram based on the meeting.       | 8 min                          | X: need the screen to be 1080P  |
| 10:15 | Bob search some question in google.(run WebScreenShoter.py do web access and random link click action one by one sequential) | 15 min                         | Done                            |
| 10:30 | Bob find what he want, and download the related web's cert, image, js, css,  file.(run WebDownloader.py do the download) | 5 min                          | Done                            |
| 10:35 | Bob send this friend some message and image(video) by telegram .(run telegramClient.py do the message sending) | 5 min                          | x : use YC's telegram password, |
| 10:40 | Bob watch YouTube video for 30 min                           | 30min                          | Done                            |
| 10:48 | Bob read checked the email for 2 min                         | 2min                           | x : use YC's telegram password, |
| 10:50 | Bob Open a word document and write a report.                 | 25 min                         | Done                            |
| 11:25 | Bob made one presentation slides.                            | 13 min                         | Done                            |
| 11:35 | Bob feel tired and play the google dino game for a short while. | 10 min                         | Done                            |
| 12:00 | Bob went for lunch                                           | 60min                          |                                 |
| 13:10 | Bob ping 100 random address  in the subnet 192.168.56.0/24 to check the connection. | 30 min                         | Done                            |
| 13:45 | Bob ssh to 10 random host to run the cmd in the subnet 192.168.57.0/24 | 20 min                         | Done                            |
| 14:10 | Bob turn off his private firewall for 30min                  | 1min                           | Done                            |
| 14:30 | Bob turn search the web and download pic, js, cert file      | 20min                          | Done                            |
| 14:50 | Bob send 2000+ UDP message to 100 different ip 192.168.57.0/24 each IP send 20 UPD message. | 20 min                         | Done                            |
| 15:15 | Bob edit the ppt and pause the test result in.               | 3 min                          | Done                            |
| 15:20 | Bob play game for 10 min                                     | 10 min                         | Done                            |
| 15:40 | Bob run server network checking cmd in terminal one by one (ipconfig, Tracert www.google.com.sg , Pathping www.google.com.sg, Getmac, Nslookup www.google.com.sg) | 5 min                          | Done                            |
| 15:55 | Bob start to pause more result he collected just now in this report | 2 min                          | Done                            |
| 16:00 | Bob watch local video and listen the music for 30 min        | 30 min                         | Done                            |
| 16:35 | Bob check and open all pictures in the picture window        | 15min                          | Done                            |
| 17:00 | Bob send 2000+ UDP message to 100 different ip 192.168.58.0/24 each IP send 20 UPD message. | 20 min                         | Done                            |
| 17:25 | Bob edit the ppt and pause the test result in.               | 5min                           | Done                            |
| 17:35 | Bob edit his daily work report word file                     | 10 min                         | Done                            |
| 17:50 | Bob logout his account.                                      |                                |                                 |



### Testcase tasks schedule:

| Action index                     | Action time   | Action detail                                                |
| -------------------------------- | ------------- | ------------------------------------------------------------ |
| testCase1: Ping and ssh          | Time 12:30:55 | Do ping and ssh login with Win-Cmd and back ground           |
| testCase2: Window basic cmd      | Time 12:31:09 | Run Windows network cmd (ipconfig, ping)                     |
| testCase3: Window basic cmd      | Time 12:31:09 | Load all the commands from config file and run them paralled (dir, ipconfig, ping) |
| testCase4:MS-Office word         | Time 12:31:32 | Create a MS-office word docx and edit. Then save to specific dir. |
| testCase5: MS-Office power point | Time 12:32:03 | Create a MS-office testCase5: MS-Office power point pptx and edit. Then save to specific dir. |
| testCase6: SCP                   | Time 12:33:05 | scp file to a linux server                                   |
| testCase7: watch YouTube         | Time 12:33:16 | Watch a web video                                            |
| testCase8: check gmail           | Time 12:33:42 | Login gmail with a account and read an "unread" email.       |
| testVase9: local file/app open   | Time 12:34:24 | Open a local video.                                          |





