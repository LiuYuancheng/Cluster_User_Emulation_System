# Windows_User_Simulator

**Program Design Purpose**: We want to create a "actor" can simulate a normal MS-Windows user to do the user action to generate user's event based on the time line setting.



Example Timeline: 

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



remove access the windows vm:

```
ssh -L 127.0.0.1:3389:192.168.57.10:3389 -p 6022 -J rp_fyp_ctf@gateway.ncl.sg ls23@172.18.178.10
```

