'''
Created on Sep 26, 2016

@author: busharaa
@author: bilkhus

'''
import requests
import argparse
import sys
import getpass
import os
from git import Repo
from os import path
import datetime


correctCopyright = """Government of Canada

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
    """
DefaultLicense = "The MIT License (MIT)\n"
correctCopyrightHolder = "Government of Canada"

def cloneRepos(overwrite, dryrun):
    username = sys.argv[1]
    password = getpass.getpass("Input password: ")

    #TODO add in if /else to check for ORG vs user repo's
    #TODO add in if/else when dealing with Github vs bitbucket

    baseAPI = "https://api.bitbucket.org/2.0/repositories/"+username + "/"
    sshBitBucket = "git@altssh.bitbucket.org:"+username + "/"
    baseGithubAPIAAFC = "https://api.github.com/orgs/AAFC-MBB/repos"
    baseGithubAPIUser = "https://api.github.com/user/" + username + "/repos"
    sshGithub = "git@github.com:" + username +"/"
    req = requests.get(baseAPI, auth=(username,password))
    statCode = req.status_code
    homePath = os.path.expanduser("~")
    i = 0
    copyrightDate = ""
    

    if(statCode == 200):
        jobj = req.json()
        for value in jobj['values']:
            i=i+1
    #         get name, check if it's seqdb in this case and ignore
            name = value['name'].lower()
            if name == "seqdb":
                continue
            print("RepoName: " + name)
            req = requests.get(baseAPI+name, auth=(username,password))
            print(sshBitBucket + name + ".git")
            repoPathName = path.join(homePath, homePath+name)
            repo = Repo.clone_from(sshBitBucket + name + ".git",repoPathName)
            #check if license is correct
            licensePath = path.join(repoPathName,repoPathName+"/LICENSE")
            if path.exists(licensePath):
                (equality,copyrightDate) = isLicenseEqual(licensePath, DefaultLicense)
                
                if(not equality and overwrite):
                    editLicense(licensePath, copyrightDate)
            else:
                print("License doesn't exist")
                editLicense(licensePath, "Copyright (c) " + str(datetime.datetime.now().year) + " ")
            if(not dryrun):
                #commit and push
                index = repo.index
                index.add(["LICENSE"])
                index.commit("Updated license")
                repo.remotes.origin.push()
    else:
        print("ERROR: " + str(statCode))
        exit()

#             commit with message "updated license", push

def isLicenseEqual(file1,myLicense):
    oFile = open(file1,'r')
    fileToStr = oFile.readline()
    oFile.readline()
    copyrightDate = oFile.readline()
    copyrightHolder = copyrightDate[19:-1]
    copyrightDate = copyrightDate[:19]
    print(copyrightHolder == correctCopyrightHolder)
    print ("Copyrightholder: " + copyrightHolder)
    if (fileToStr == myLicense and copyrightHolder == correctCopyrightHolder):
        print("License is in fact equal")
        return (True, copyrightDate)
    else:
        return (False, "Copyright (c) " + str(datetime.datetime.now().year) + " ")
     
     
def editLicense(repoPath,copyrightDate):
    f = open(repoPath,'w')
    print(f)
    
    f.write(DefaultLicense+"\n"+copyrightDate+correctCopyright)
    f.close()
   
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("username")
    parser.add_argument("-o", help="Overwrite option")
    parser.add_argument("-d", help="Dryrun option, doesn't commit or push")
    overwrite=False
    dryrun=False
    if(len(sys.argv) <= 1):
        print("Usage: licenseFixer.py username [-o overwrite] [-d Dryrun]")
        exit()
    args = parser.parse_args()
    if (args.d):
        dryrun = True
    if (args.o):
        overwrite = True
    cloneRepos( overwrite,dryrun)

