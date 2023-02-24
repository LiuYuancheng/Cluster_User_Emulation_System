# Emulate Actor: Alice

This project is used to simulate Alice, who is a company administrative officer. She logged into her desktop at 9:00am



### Actor TimeLine

#### Daily action timeline

The Action's daily Action will follow below time line:

| Time  | Action                                                       | Action Time (TestCase Setting) | Current Progress |
| ----- | ------------------------------------------------------------ | ------------------------------ | ---------------- |
| 9:05  | Check for new emails in outlook (emailActor.py)              | 15 min                         | Done             |
| 9:20  | Play music in YouTube <br> (funcActor.py -> webActor)        | 3 min                          | Done             |
| 9:23  | Prepare draft for meeting in the afternoon using Word (funcActor.py -> startFile) | 37 min                         | Done             |
| 10:00 | Start zoom meeting for company meeting (zoomActor.py)        | 120 min                        | Done             |
| 12:00 | Lunch                                                        | 60 min                         |                  |
| 1:00  | Design slides for new company policy (funcActor.py -> msPPTedit) | 120 min                        | Done             |
| 3:00  | Play dino game on Google browser (dinoActor.py)              | 15 min                         | Done             |
| 3:15  | Browse the Internet for online shopping (funcActor.py -> webActor) | 30 min                         | Done             |
| 3:45  | Download dog wallpapers and executable files online (webDownload.py) | 15 min                         | Done             |
| 4:00  | Reads and replies more email in Outlook (emailActor.py)      | 60 min                         | Done             |
| 5:00  | Uses Telegram desktop to send messages to her friends        | 15 min                         | Done             |
| 5:15  | Research some information for slides proposal <br>(Run WebScreenShoter.py to perform web access. Random link click action one by one sequential | 20 min                         | Done             |
| 5:35  | Finishing up word document report <br>(funcActor.py -> startFile) | 25 min                         | Done             |



#### Random action timeline

The Action's random action will follow below time line:

| Time | Action | Action Time (TestCase Setting) | Current Progress |
| ---- | ------ | ------------------------------ | ---------------- |
|      |        |                                |                  |



#### Weekly action timeline

The Action's random action will follow below time line:

| Time | Action | Action Time (TestCase Setting) | Current Progress |
| ---- | ------ | ------------------------------ | ---------------- |
|      |        |                                |                  |



------

### Program Setup

Follow the below steps to setup Alice's Profile and run the Scheduler as Alice:

- Copy the profile `scheduleProfile_Alice.py` and Customized function repo file `actorFunctionsAlice.py`  to `Windows_User_Simulator\src\actionScheduler` folder. 
- Copy `scheduleCfg_Alice.txt` to `Windows_User_Simulator\src\actionScheduler` folder. change it file name to `scheduleCfg.txt` to overwrite the original one. 
- Run the `Windows_User_Simulator\src\actionScheduler\SchedulerRun.py` file or `Windows_User_Simulator\src\runScheduler_win.bat`



------

