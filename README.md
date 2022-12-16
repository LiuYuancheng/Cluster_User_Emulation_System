# Windows_User_Simulator

**Program Design Purpose**: We want to create a "actor" can simulate a normal MS-Windows user to do the user action to generate user's event based on the time line setting.



Example Timeline: 



Bob is a system technical support officer. He login his Windows server at 8:50 am

| Time     | Action                                                       | action time (testCase setting) | current progress                         |
| -------- | ------------------------------------------------------------ | ------------------------------ | ---------------------------------------- |
| 9:01 am  | Ping a servers list to check the server's connection. (open console ping the dest one by one, sequential ) | 10 min                         | done                                     |
| 9:10 am  | Bob runs the ping client program ping 100 servers need to check and record done the result.(run pingClient.py, multi-thread parallel ping) | 10 min                         | done                                     |
| 9:13 am  | During watching the ping result refresh, bob run server network checking cmd in terminal one by one (ipconfig, Tracert www.google.com.sg , Pathping www.google.com.sg, Getmac, Nslookup www.google.com.sg) | 5 min                          | done                                     |
| 9:20 am  | Bob ssh to 12 Ubuntu servers and run some cmd  record done the result.(run sshConnector.py do server one by one sequential) | 12min                          | done                                     |
| 9:32 am  | Bob use "Tree" cmd to search some files.                     | 2 min                          | done                                     |
| 9:35 am  | Bob start a zoom meeting with his colleague to discuss for half hour | 30 min                         | done                                     |
| 10:05am  | Write down and draw some diagram based on the meeting.       | 8 min                          | X: need the screen to be 1080P           |
| 10:15am  | Bob search some question in google.(run WebScreenShoter.py do web access and random link click action one by one sequential) | 15 min                         | Done                                     |
| 10:30 am | Bob find what he want, and download the related web's cert, image, js, css,  file.(run WebDownloader.py do the download) | 5 min                          | Done                                     |
| 10:35 am | Bob send this friend some message and image(video) by telegram .(run telegramClient.py do the message sending) | 5 min                          | x : use YC's telegram password,          |
| 10:40 am | Bob watch YouTube video for 30 min                           | 30min                          | Done                                     |
| 10:48am  | Bob read checked the email for 2 min                         | 2min                           | x : use YC's telegram password,          |
| 10:50 am | Bob Open a word document and write a report.                 | 25 min                         | Done                                     |
| 11:25am  | Bob made one presentation slides.                            | 13 min                         | Done                                     |
| 11:35 am | Bob feel tired and play the google dino game for a short while. | 10 min                         | Done                                     |
| 12:00 am | Bob open the deliveroo.com.sg to search some lunch promotion (run Webattestation.py with the key word setup"sale", 'promotion') | 10min                          | x : need to use YC's Deliveroo password, |
|          |                                                              |                                |                                          |

