# -----------------------------------------------------------------------------
# Name:        actorFunctions.py
#
# Purpose:     Please put your actor function in this module
#
# Author:      Yuancheng Liu
#
# Created:     2020/12/15
# Copyright:
# License:
# -----------------------------------------------------------------------------
import os
import glob
import time
import json
import random
from random import randint
import keyboard
import string
import actionGlobal as gv
from urllib.parse import urljoin, urlparse
from UtilsFunc import (
    pingActor,
    funcActor,
    zoomActor,
    webDownload,
    dinoActor,
    emailActor,
    functionActors,
)

# from UtilsFunc import email_gen

import Log
import SSHconnector
import udpCom


PORT = 443  # port to download the server certificate most server use 443.

# -----------------------------------------------------------------------------


def func_0900():
    account = "bob@gt.org"
    password = "123"
    smtpServer = "email.gt.org"
    smtpPort = 143
    actor = emailActor.emailActor(account, password)
    actor.initEmailReader(smtpServer, smtpPort=smtpPort, sslConn=False)
    print(actor.getMailboxList())
    print("=> read 2 random in last 3 email")
    readConfig2 = {
        "mailBox": "inbox",
        "sender": None,
        "number": 6,
        "randomNum": 0,
        "interval": 2,
        "returnFlg": False,
    }
    result = actor.readLastMail(configDict=readConfig2)
    actor.close()


# -----------------------------------------------------------------------------


def func_0915():
    # Open and edit the word doc.
    funcActor.startFile(gv.WORD_FILE)
    time.sleep(3)  # wait office start the word doc.
    try:
        with open(gv.WORD_CFG) as fp:
            textLine = fp.readlines()
            for line in textLine:
                funcActor.simuUserType(line)
        # we will not close the file.
        # time.sleep(1)
        # keyboard.press_and_release('alt+f4')
        # time.sleep(1)
        # keyboard.press_and_release('enter')

    except:
        print("No input file config!")


# -----------------------------------------------------------------------------


def func_0925():
    # ping dest in the config file
    parallel = False
    showConsole = True
    configPath = os.path.join(gv.ACTOR_CFG, "pingTestDest.json")
    actor = pingActor.pingActor(
        configPath, parallel=parallel, Log=None, showConsole=showConsole
    )
    result = actor.runPing()


# -----------------------------------------------------------------------------


def func_0927():
    # Google search on target client
    soup = webDownload.urlDownloader(
        imgFlg=True, linkFlg=True, scriptFlg=True, caFlg=True
    )
    count = failCount = 0
    if not os.path.exists(gv.RST_DIR):
        os.mkdir(gv.RST_DIR)
    soup.setResutlDir(gv.RST_DIR)
    print("> load url record file %s" % gv.URL_RCD2)
    with open(gv.URL_RCD2) as fp:
        urllines = fp.readlines()
        for line in urllines:
            if line[0] in ["#", "", "\n", "\r", "\t"]:
                continue  # jump comments/empty lines.
            count += 1
            print("> Process URL {}: {}".format(count, line.strip()))
            if "http" in line:
                line = line.strip()
                domain = str(urlparse(line).netloc)
                folderName = "_".join((str(count), domain))
                result = soup.savePage(line, folderName)
                # soup.savePage('https://www.google.com', 'www_google_com')
                if result:
                    print("Finished.")
                else:
                    failCount += 1
    print(
        "\n> Download result: download %s url, %s fail" % (str(count), str(failCount))
    )


# -----------------------------------------------------------------------------


def func_0932():
    # Visit whois.com to enumerate ip address. Append ip to end of link once available.
    search = functionActors.browserActor()
    search.openUrls("whois.com/")


# -----------------------------------------------------------------------------


def func_0940():
    # Visit whois.com to enumerate ip address. Append ip to end of link once available.
    search = functionActors.browserActor()
    search.openUrls("robtex.com/dns-lookup/")


# -----------------------------------------------------------------------------


def func_0945():
    # Open and edit the word doc.
    funcActor.startFile(gv.WORD_FILE)
    time.sleep(3)  # wait office start the word doc.
    try:
        with open(gv.WORD_CFG) as fp:
            textLine = fp.readlines()
            for line in textLine:
                funcActor.simuUserType(line)
        # we will not close the file.
        # time.sleep(1)
        # keyboard.press_and_release('alt+f4')
        # time.sleep(1)
        # keyboard.press_and_release('enter')

    except:
        print("No input file config!")


# -----------------------------------------------------------------------------


def func_1000():
    # nmap installed in Charlie's computer. Ip of target must be included.
    os.subprocess.call("nmap -sC -sV <ip>", shell=True)


# -----------------------------------------------------------------------------


def func_1010():
    # gobuster installed in Charlie's computer. Ip of target must be included.
    os.subprocess.call("gobuster -u <url> -w <wordlist>", shell=True)


# -----------------------------------------------------------------------------


def func_1015():
    # Perform google search on port vulnerabilities
    search = functionActors.browserActor()
    search.openUrls("allinurl:port 443")


# -----------------------------------------------------------------------------


def func_1030():
    # start a zoom meeting
    # appName = 'zoomActor.py'
    # appPath = os.path.join(gv.ACTOR_DIR, appName)
    # cmd = "python %s" %str(appPath)
    # result = funcActor.runCmd(cmd)
    # print(result)
    actor = zoomActor.zoomActor(userName="TestUser_Bob")
    actor.startMeeting(
        "https://us04web.zoom.us/j/4580466160?pwd=d0ZUSCs0bWpMc2o2MHgzTS80a2tJdz09"
    )
    meetingPeriod = 20  # 20 mins meeting
    time.sleep(60 * meetingPeriod)
    actor.endCrtMeeting()
    print("Finish")


# -----------------------------------------------------------------------------


def func_1300():
    # sqlmap installed in Charlie's computer. Ip of target must be included.
    os.subprocess.call(
        "sqlmap.py -u <target address url> --cookie=" " --schema --bath", shell=True
    )
    os.subprocess.call(
        "sqlmap.py -u <target address url> --cookie=" " --columns -T users --bath",
        shell=True,
    )


# -----------------------------------------------------------------------------


def func_1320():
    # Perform google search on port vulnerabilities
    search = functionActors.browserActor()
    search.openUrls("https://gchq.github.io/CyberChef/")


# -----------------------------------------------------------------------------


def func_1325():
    # Perform ssh to open port and input pw
    os.subprocess.call("ssh <>@ip", shell=True)
    # Command to input pw


# -----------------------------------------------------------------------------


def func_1330():
    # Run sudo -l to check for root privileges
    os.subprocess.call("sudo -l", shell=True)


# -----------------------------------------------------------------------------


def func_1335():
    # Visit whois.com to enumerate ip address. Append ip to end of link once available.
    search = functionActors.browserActor()
    search.openUrls("https://book.hacktricks.xyz/")


# -----------------------------------------------------------------------------


def func_1345():
    # Visit whois.com to enumerate ip address. Append ip to end of link once available.
    search = functionActors.browserActor()
    search.openUrls("https://gtfobins.github.io/")


# -----------------------------------------------------------------------------


def func_1400():
    # watch youTube video
    watchActor = funcActor.webActor()
    count = failCount = 0
    watchPeriod = 5
    print("> load youTube url record file %s" % gv.YOUTUBE_CFG)
    with open(gv.YOUTUBE_CFG) as fp:
        urllines = fp.readlines()
        for line in urllines:
            if line[0] in ["#", "", "\n", "\r", "\t"]:
                continue  # jump comments/empty lines.
            count += 1
            print("> Process URL {}: {}".format(count, line.strip()))
            if "http" in line:
                line = line.strip()
                urlitem = {
                    "cmdID": "YouTube",
                    "url": line,
                    "interval": 3,
                }
                watchActor.openUrls(urlitem)
                keyboard.press_and_release("page down")
                time.sleep(2)
                keyboard.press_and_release("page up")
                time.sleep(2)
                keyboard.press_and_release("space")
                time.sleep(60 * watchPeriod)

    watchActor.closeBrowser()


# -----------------------------------------------------------------------------


def func_1415():
    # Download WinPEAS from https://github.com/carlospolop/PEASS-ng/releases/download/20230212/winPEASx64.exe
    soup = webDownload.urlDownloader(
        imgFlg=True, linkFlg=True, scriptFlg=True, caFlg=True
    )
    count = failCount = 0
    if not os.path.exists(gv.RST_DIR):
        os.mkdir(gv.RST_DIR)
    soup.setResutlDir(gv.RST_DIR)
    print("> load url record file %s" % gv.URL_RCD2)
    with open(gv.URL_RCD2) as fp:
        urllines = fp.readlines()
        for line in urllines:
            if line[0] in ["#", "", "\n", "\r", "\t"]:
                continue  # jump comments/empty lines.
            count += 1
            print("> Process URL {}: {}".format(count, line.strip()))
            if "http" in line:
                line = line.strip()
                domain = str(urlparse(line).netloc)
                folderName = "_".join((str(count), domain))
                result = soup.savePage(line, folderName)
                # soup.savePage('https://www.google.com', 'www_google_com')
                if result:
                    print("Finished.")
                else:
                    failCount += 1
    print(
        "\n> Download result: download %s url, %s fail" % (str(count), str(failCount))
    )


# -----------------------------------------------------------------------------


def func_1425():
    # File sharing
    # Target needs to run wget at this timing
    os.subprocess.call("python -m SimpleHTTPServer 80", shell=True)


# -----------------------------------------------------------------------------


def func_1430():
    # Download exploit from exploit-db.com
    soup = webDownload.urlDownloader(
        imgFlg=True, linkFlg=True, scriptFlg=True, caFlg=True
    )
    count = failCount = 0
    if not os.path.exists(gv.RST_DIR):
        os.mkdir(gv.RST_DIR)
    soup.setResutlDir(gv.RST_DIR)
    print("> load url record file %s" % gv.URL_RCD2)
    with open(gv.URL_RCD2) as fp:
        urllines = fp.readlines()
        for line in urllines:
            if line[0] in ["#", "", "\n", "\r", "\t"]:
                continue  # jump comments/empty lines.
            count += 1
            print("> Process URL {}: {}".format(count, line.strip()))
            if "http" in line:
                line = line.strip()
                domain = str(urlparse(line).netloc)
                folderName = "_".join((str(count), domain))
                result = soup.savePage(line, folderName)
                # soup.savePage('https://www.google.com', 'www_google_com')
                if result:
                    print("Finished.")
                else:
                    failCount += 1
    print(
        "\n> Download result: download %s url, %s fail" % (str(count), str(failCount))
    )


# -----------------------------------------------------------------------------


def func_1435():
    os.subprocess.call("searchsploit windows", shell=True)


# -----------------------------------------------------------------------------


def func_1440():
    os.subprocess.call("msfvenom", shell=True)


# -----------------------------------------------------------------------------


def func_1450():
    # Open and edit the word doc.
    funcActor.startFile(gv.WORD_FILE)
    time.sleep(3)  # wait office start the word doc.
    try:
        with open(gv.WORD_CFG) as fp:
            textLine = fp.readlines()
            for line in textLine:
                funcActor.simuUserType(line)
        # we will not close the file.
        # time.sleep(1)
        # keyboard.press_and_release('alt+f4')
        # time.sleep(1)
        # keyboard.press_and_release('enter')

    except:
        print("No input file config!")


# -----------------------------------------------------------------------------


def func_1520():
    # Edit the ppt file
    try:
        pptConfig = gv.PPT_CFG1  # you can build your own config file.
        with open(pptConfig) as fp:
            actions = json.load(fp)
            for action in actions:
                if "picName" in action.keys():
                    action["picName"] = os.path.join(gv.ACTOR_CFG, action["picName"])
                funcActor.msPPTedit(gv.PPT_FILE, action)
    except Exception as err:
        print("The pptx config file is not exist.")
        print("error: %s" % str(err))


# -----------------------------------------------------------------------------


def func_1620():
    # start a zoom meeting
    # appName = 'zoomActor.py'
    # appPath = os.path.join(gv.ACTOR_DIR, appName)
    # cmd = "python %s" %str(appPath)
    # result = funcActor.runCmd(cmd)
    # print(result)
    actor = zoomActor.zoomActor(userName="TestUser_Bob")
    actor.startMeeting(
        "https://us04web.zoom.us/j/4580466160?pwd=d0ZUSCs0bWpMc2o2MHgzTS80a2tJdz09"
    )
    meetingPeriod = 20  # 20 mins meeting
    time.sleep(60 * meetingPeriod)
    actor.endCrtMeeting()
    print("Finish")


# -----------------------------------------------------------------------------

if __name__ == "__main__":
    testCase(1)

