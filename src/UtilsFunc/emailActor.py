#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        emailActor.py
#
# Purpose:     This module is used to read and write email.
# Author:      Yuancheng Liu
#
# Version:     v_0.1
# Created:     2022/12/28
# Copyright:   n.a
# License:     n.a
#-----------------------------------------------------------------------------

# Gmail configure:
# Turn on the Less secure app access at: Google Account> Security> Less secure app access
# Enable the IMAP Access at: Gmail Settings> Forwarding and POP / IMAP> IMAP Acess

import time
import ssl
import smtplib
import imaplib
import email
import traceback 
import random

SMTP_PORT_READ = 993
SMTP_PORT_SEND = 587
SMTP_PORT_SEND_SSL = 465

DEFAULT_CFG = {
    'mailBox': 'inbox',
    'sender': None,
    'number': 10,
    'randomNum': 0,
    'interval': 0,
    'returnFlg': False
}

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class emailActor(object):
    """ GMail: smtpPort[993], sslConn[True]
        HotMail: smtpPort[587], sslConn[True]
        Mailu: smtpPort[143], sslConn[True]

    Args:
        object (_type_): _description_
    """

    def __init__(self, account, password) -> None:
        self.account = account
        self.password = password
        self.emailReader = None
        self.emailSender = None

#-----------------------------------------------------------------------------
    def initEmailReader(self, smtpServer, smtpPort=SMTP_PORT_READ, sslConn=True):
        """ Connect(login) to the email read IMAP server and init the read object. 
            Args:
                smtpServer (str): email IMAP server url.
                smtpPort (int, optional): email IMAP server port. Defaults to SMTP_PORT_READ.
                sslConn (bool, optional): email account's connection ssl encryption 
                    config. Defaults to True.

            Returns:
                _type_: _description_
        """
        try:
            self.emailReader = imaplib.IMAP4_SSL(
                host=smtpServer, port=smtpPort) if sslConn else imaplib.IMAP4(host=smtpServer, port=smtpPort)
            self.emailReader.login(self.account, self.password)
            return True
        except Exception as err:
            print("Login the email server failed.")
            print("Error: %s" % str(err))
            return False
#-----------------------------------------------------------------------------
    def initEmailSender(self, smtpServer, smtpPort=SMTP_PORT_READ, sslConn=True):
        try:
            if sslConn:
                ssl_context = ssl.create_default_context()
                service = smtplib.SMTP_SSL(smtpServer, smtpPort, context=ssl_context)
                service.login(self.account, self.password)
            else:
                self.emailSender = smtplib.SMTP(smtpServer, smtpPort)
                self.emailSender.starttls()
                self.emailSender.login(self.account, self.password)
        except Exception as err:
            print("Login the email server failed.")
            print("Error: %s" % str(err))
            return False

#-----------------------------------------------------------------------------
    def getMailboxList(self):
        if self.emailReader:
            return self.emailReader.list()
        return None

#-----------------------------------------------------------------------------
    def sendEmail(self):
        if self.emailSender:
            self.emailSender.sendmail("sender_email_id", 'liu_yuan_cheng@hotmail.com', "test message from ncl gmail box")
            self.emailSender.quit()

#-----------------------------------------------------------------------------
    def readLastMail(self, configDict=DEFAULT_CFG):
        if not isinstance(configDict, dict):
            print("The input config is invalid: %s" %str(configDict))
            return None
        configKeys = configDict.keys()
        result = [] if 'returnFlg' in configKeys and configDict['returnFlg'] else None
        if self.emailReader:
            mailIds = self.getEmailIdList(emailBox=configDict['mailBox'], emailNum=configDict['number'], sender=configDict['sender'])
            if mailIds is None :
                print("Can not file email based on the config.")
                return None
            randMailIds = random.sample(mailIds, configDict['randomNum']) if 'randomNum' in configKeys and configDict['randomNum'] > 0 else mailIds
            for mailId in randMailIds:
                msg = self.getEmailDetail(mailId)
                if msg:
                    print("Get email: %s " %str(msg['subject']))
                    if result is None:
                        print("Email idx=%s info:" %str(mailId))
                        print('From : ' + msg['from'] + '\n')
                        print('To : ' + msg['to'] + '\n')
                        print('Subject : ' + msg['subject'] + '\n')
                    else:
                        result.append(msg)
                if 'interval' in configKeys and configDict['interval'] > 0:
                    time.sleep(configDict['interval'])
            print("Read email finish")
            if result: return result
        else:
            print("Email send is not init.")

#-----------------------------------------------------------------------------
    def getEmailIdList(self, emailBox='inbox', emailNum=10, sender=None):
        if self.emailReader:
            try:
                self.emailReader.select(emailBox)
                emailInfo = self.emailReader.search(None, 'ALL') if sender is None else self.emailReader.search(None, 'FROM', f'"{sender}"')
                IdList = emailInfo[1][0].split() 
                mailIds = IdList if len(IdList) < emailNum else IdList[-emailNum:]
                return mailIds
            except Exception as err:
                print("Get the mail ids error: %s" %str(err))
        print("Email reader is not init.")
        return None

#-----------------------------------------------------------------------------
    def getEmailDetail(self, emailId):
        """ Get the email info.
        Args:
            emailIdx (_type_): _description_
        """
        if self.emailReader:
            mailId = int(emailId)
            data = self.emailReader.fetch(str(mailId), '(RFC822)')
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    try:
                        return email.message_from_string(str(arr[1],'utf-8'))
                    except:
                        return None
        else:
            print("Email reader is not init.")
            return None

#-----------------------------------------------------------------------------
    def close(self):
        if self.emailReader:
            self.emailReader.close()
            self.emailReader.logout()
            self.emailReader = None
    
        if self.emailSender:
            self.emailSender.close()
            self.emailSender = None

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def testCase(mode):
    account = 'alice@gt.org'
    account = 'bob@gt.org'
    account = 'charles@gt.org'
    password = '123'
    smtpServer = 'email.gt.org'
    smtpPort = 143
    actor = emailActor(account, password, smtpServer, smtpPort=smtpPort, sslConn=False)
    actor.readLastMail(emailNum=2)

if __name__ == '__main__':
    testCase(1)
