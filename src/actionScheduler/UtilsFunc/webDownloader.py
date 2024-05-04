#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        webDownloader.py
#
# Purpose:     This module will provide API to download the webpage components: 
#              html file, image file, javascript file, href link file, host SSL
#              certificate and xxl  based on the input url. The user can list 
#              all the urls he wants to downlad in the file "urllist.txt" .
#
# Author:      Yuancheng Liu
#
# Created:     2021/11/12
# Version:     v_0.1.2
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License 
#-----------------------------------------------------------------------------

import os
import sys
import re
import requests
import ssl
from datetime import datetime
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

PORT = 443 # port to download the server certificate most server use 443.

# init the not html hyper link type:
SP_LINK_TYPE = ('css', 'png', 'ico', 'jpg', 'jpeg', 'mov', 'ogg', 'gif', 'xml','js')
# init the html maim page pre-fix. the contents will be save in file downloadPage_yyyymmdd_hhmmss.html
PAGE_PRE_FIX = 'downloadPage'
URL_RCD_FILE = 'urlRcd.txt' # file to record the download info.

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class webDownloader(object):
    """ Downloader class."""
    def __init__(self, imgFlg=True, linkFlg=True, scriptFlg=True, caFlg=True, 
                 spLinkType=SP_LINK_TYPE):
        """ Init example: webDownloader(imgFlg=True, linkFlg=True, scriptFlg=True, caFlg=True)
            Args:
                imgFlg (bool, optional): flag to identify whehter download image. Defaults to True.
                linkFlg (bool, optional): flag to identify whehter download all the hyper link contents. Defaults to True.
                scriptFlg (bool, optional): flag to identify whehter download script. Defaults to True.
                caFlg (bool, optional): flag to identify whehter download certificate. Defaults to True.
                spLinkType (list, optional): all the hyper link contents type . Defaults to SP_LINK_TYPE.
        """
        self.soup = None
        self.imgFlg = imgFlg
        self.linkFlg = linkFlg
        self.scriptFlg = scriptFlg
        self.caFlg = caFlg
        self.linkType = spLinkType
        self.session = requests.Session()

    #-----------------------------------------------------------------------------
    def _soupfindnSave(self, url, outputFolder, tag2find='img', inner='src'):
        """ Use the beautiful soup lib to find all the tag in the html contents and 
            download the contents.
        """
        pagefolder = os.path.join(outputFolder, tag2find)
        if not os.path.exists(pagefolder): os.mkdir(pagefolder)
        for res in self.soup.findAll(tag2find):   # images, css, etc..
            try:
                if not res.has_attr(inner): continue # check if inner tag (file object) exists
                # clean special chars such as '@, # ? <>'
                filename = re.sub('\W+', '.', os.path.basename(res[inner]))
                # print("> filename:", filename)
                # Added the '.html' for the html file in the href
                if tag2find == 'link' and (not any(ext in filename for ext in self.linkType)):
                    filename += '.html'
                fileurl = urljoin(url, res.get(inner))
                filepath = os.path.join(pagefolder, filename)
                # rename html ref so can move html and folder of files anywhere
                res[inner] = os.path.join(os.path.basename(pagefolder), filename)
                # create the file.
                if not os.path.isfile(filepath):
                    with open(filepath, 'wb') as file:
                        filebin = self.session.get(fileurl)
                        if len(filebin.content) > 0: # filter the empty file(imge not found)
                            file.write(filebin.content)
            except Exception as err:
                print(err, file=sys.stderr)

    #-----------------------------------------------------------------------------
    def _saveServCA(self, url, pagefolder):
        """ Parse the host name from the URL then try to download the host's SSL 
            certificate. 
            Args:
                url (str): web url string.
                pagefileDir (str, optional): path to save the web components.
            Returns:
                [bool]: whether the components saved the successfully.
        """
        if 'https' in url:
            certfolder = os.path.join(pagefolder, 'cert')
            if not os.path.exists(certfolder): os.mkdir(certfolder)
            caFilepath = os.path.join(certfolder, 'cert.der')
            hostname = urlparse(url).hostname
            with open(caFilepath, 'wb') as f:
                cert = None
                try:
                    cert = ssl.get_server_certificate((hostname, PORT))
                except:
                    print('>> Error: host: %s is invalid.' % str(hostname))
                    # revert split the host to remove the country section such as 'sg'
                    hostname = hostname.rsplit('.', 1)[0]
                    cert = ssl.get_server_certificate((hostname, PORT))
                if cert: f.write(ssl.PEM_cert_to_DER_cert(cert)) # write the cert info.
            return True
        else:
            print("saveServCA() > The url is not a https url, no ssl CA available")
            return False

    #-----------------------------------------------------------------------------
    def downloadWebContents(self, urlStr, outputDirPath):
        """ Download the web contents.
            Args:
                urlStr (str): url string
                outputDirPath (str): output folder path.
            Returns:
                bool: true if download successful, else fails.
        """
        if not ('http' in urlStr):
            print("> savePage(): The input url is not valid: %s" %str(urlStr))
            return False
        try:
            response = self.session.get(urlStr)
            self.soup = BeautifulSoup(response.text, features="lxml")
            # Create the output folder is the folder not exist.
            if not os.path.exists(outputDirPath): os.mkdir(outputDirPath)
            # save the html page to outputDirPath
            htmlfilePath = os.path.join(outputDirPath, 
                                        PAGE_PRE_FIX+'_'+datetime.now().strftime("%Y%m%d_%H%M%S")+'.html')
            with open(htmlfilePath, 'wb') as file:
                file.write(self.soup.prettify('utf-8'))
            # download all the image files to outputDirPath/img folder:
            if self.imgFlg:
                self._soupfindnSave(urlStr, outputDirPath, tag2find='img', inner='src')
            # download all the hyper link files to outputDirPath/link folder:
            if self.linkFlg:
                self._soupfindnSave(urlStr, outputDirPath, tag2find='link', inner='href')
            # download all the javascript files to outputDirPath/script folder:
            if self.scriptFlg:
                self._soupfindnSave(urlStr, outputDirPath, tag2find='script', inner='src')
            # download the CA certificate to outputDirPath/cert folder:
            if self.caFlg: self._saveServCA(urlStr, outputDirPath)
            # save the orignal url in the url record file
            urlRcdPath = os.path.join(outputDirPath, URL_RCD_FILE)
            with open(urlRcdPath, "a+", encoding='ISO-8859-1') as f:
                f.write(urlStr)
            return True
        except Exception as err:
            print("Error > downloadWebContents() create files failed: %s." % str(err))
            return False

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main():
    print("Start the Web downloader")
    downloader = webDownloader(imgFlg=True, linkFlg=True, scriptFlg=True, caFlg=True)
    print("Current working directory is : %s" % os.getcwd())
    dirpath = os.path.dirname(os.path.abspath(__file__))
    outputDir = os.path.join(dirpath, 'outputFolder')
    urlCount = 0 
    while True:
        print("Input the url:")
        url = str(input())
        if url in ('exist', 'quit', 'q', 'Q'): break
        urlStr = str(url).strip()
        domain = str(urlparse(urlStr).netloc)
        downloadFolderPath = os.path.join(outputDir, '_'.join((str(urlCount), domain)))
        downloader.downloadWebContents(urlStr, downloadFolderPath)

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
