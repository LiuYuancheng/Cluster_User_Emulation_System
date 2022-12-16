### User Action Timeline 



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





