#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        gitDownloader.py
#
# Purpose:     This module is used to batch git clone the large file system 
#              via git-lfs
#
# Version:     v_0.1
# Created:     2023/09/15
# Copyright:   n.a
# License:     n.a
#-----------------------------------------------------------------------------
import git
import os
import json
from git import Repo

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class gitDownloader(object):

    def __init__(self, targetDir) -> None:
        self.targetDir = targetDir

    def cloneRepo(self, reportUrl, folderName):
        targetFld = os.path.join(self.targetDir, folderName)
        try:
            if not os.path.exists(targetFld):
                os.mkdir(targetFld)
            repo = Repo.clone_from(reportUrl, targetFld)
            return(True, '0')
        except Exception as err:
            return (False, str(err))

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def testCase(mode):
    
    dirpath = os.path.dirname(__file__)
    downloader = gitDownloader(dirpath)
    downloadCfg = os.path.join(dirpath, 'repoRecord.json') 
    with open(downloadCfg) as fp:
        repoInfo = json.load(fp)
        for info in repoInfo:
            repoName = info['repoName']
            repoUrl = info['repoUrl']
            print("Start to clone the repo: %s" %str(repoName) )
            result = downloader.cloneRepo(repoUrl, repoName)
            if result[0]:
                print("Finished")
            else:
                print("error: %s" %str(result[1]))

if __name__ == '__main__':
    testCase(0)