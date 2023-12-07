#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        emailActorTest.py
#
# Purpose:     The testCase and usage exmaple module for the lib <emailActor.py>
# Author:      Yuancheng Liu
#
# Version:     v_0.1.2
# Created:     2022/12/29
# Copyright:   Copyright (c) LiuYuancheng
# License:     MIT License 
#-----------------------------------------------------------------------------
"""
    Put this program with the same foler as the <emailActor.py>, se the test 
    mode config value <modeVal> to try different cases.
    modeVal == 1 : Read x random in last n emails.
"""

import os
import time
import emailActor

# the test mode value.
modeVal = 5

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def testCase(mode):
    # Init the email acotor's account.
    account = 'yuancheng@ncl.sg'
    password = '****' # YC: Please don't commit your password to the repo!!!
    smtpServerR = 'imap.gmail.com' # IMAP server (SMTP email read)
    smtpPortR = 993 # smtp email read port. 
    actor = emailActor.emailActor(account, password)
    print("Test Mode : %s" %str(mode))
    # Test read email. 
    if mode == 1:
        actor.initEmailReader(smtpServerR, smtpPort=smtpPortR)
        print(actor.getMailboxList())
        print('Case 1 => read 2 random in last 3 emails.')
        readConfig = {
            'mailBox': 'inbox',
            'sender': None,
            'number': 3,
            'randomNum': 2,
            'interval': 0.5,
            'returnFlg': False
        }
        result = actor.readLastMail(configDict=readConfig)
        actor.close()
    # Test send a message as email ( The mail may go to spam ): 
    elif mode ==2:
        destEmail = "liu_yuan_cheng@hotmail.com"
        smtpServerS = 'smtp.gmail.com' # IMAP server (SMTP email read)
        smtpPortS = 587 # smtp email read port. 
        actor.initEmailSender(smtpServerS, smtpPort = smtpPortS, sslConn=False)
        message = "Test message."
        actor.sendEmailMsg(destEmail, message)
        time.sleep(1)
        actor.close()
        print('finish')
    # Test send html contents as email : 
    elif mode == 3:
        destEmail = "liu_yuan_cheng@hotmail.com"
        smtpServerS = 'smtp.gmail.com' # IMAP server (SMTP email read)
        smtpPortS = 587 # smtp email read port. 
        actor.initEmailSender(smtpServerS, smtpPort = smtpPortS, sslConn=False)
        subjectStr = "EmailActor test email subject"
        htmlContent = """\
                 <html>
                 <body>
                     <p>Hi,<br>
                     How are you?<br>
                     <a href="http://www.realpython.com">Real Python</a> 
                     has many great tutorials.
                     </p>
                     <p> Thank you very much, </p>
                     <p> Best Regards </p>
                     <p> YC </p>
                 
                 </body>
             </html>
             """
        dirpath = os.path.dirname(__file__)
        filePath = os.path.join(dirpath, "cmdTest.json")
        actor.sendEmailHtml(destEmail,subjectStr,htmlContent, attachmentPath=filePath)
        time.sleep(1)
        actor.close()
        print('finish')
    # Test send forward an exported email : 
    elif mode == 4:
        destEmail = "liu_yuan_cheng@hotmail.com"
        smtpServerS = 'smtp.gmail.com' # IMAP server (SMTP email read)
        smtpPortS = 587 # smtp email read port. 
        actor.initEmailSender(smtpServerS, smtpPort = smtpPortS, sslConn=False)
        dirpath = os.path.dirname(__file__)
        filePath = os.path.join(dirpath, "email_bank" ,"Logging_Library_Log4j_Vulnerability.eml")
        actor.forwardEml(destEmail, filePath)
        time.sleep(1)
        actor.close()
        print('finish')
    # Test download the attachment from a email.
    if mode == 5:
        actor.initEmailReader(smtpServerR, smtpPort = smtpPortR)
        print(actor.getMailboxList())
        print('=> read last email and downlaod the attachment')
        readConfig2 = {
            'mailBox': 'inbox',
            'sender': 'liu_yuan_cheng@hotmail.com',
            'number': 10,
            'randomNum': 0,
            'interval': 0.5,
            'returnFlg': False
        }
        result = actor.readLastMail(configDict=readConfig2, downloadDir="C:\\Users\\liu_y\\Downloads\\leak\\")
        actor.close()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
if __name__ == '__main__':
    testCase(modeVal)
