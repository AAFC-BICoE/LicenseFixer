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
import shutil
import datetime

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
    homePath = os.getcwd()
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
            repoPathName = path.join(homePath, homePath+ "/repos/" +name)
            repo = Repo.clone_from(sshBitBucket + name + ".git",repoPathName)
            #check if license is correct
            homeLicensePath = path.join(homePath,homePath+"/LICENSE")
            licensePath = path.join(repoPathName,repoPathName+"/LICENSE")
            if path.exists(licensePath):
                (equality,copyrightDate) = isLicenseEqual(licensePath, DefaultLicense)
               
                if(not equality and overwrite):
                    editLicense(licensePath, copyrightDate)
            else:
                print("License doesn't exist")

                repo.git.checkout(b="update_license_and_copyright")
                print("created branch update_license_and_copyright")
                editLicense(homeLicensePath, licensePath)
            if(not dryrun):
                #add license file and commit to feature branch
                index = repo.index
                index.add(["LICENSE"])
                index.commit("Updated license and copyright")
            
                #checkout master branch and merge in feature branch
                git = repo.git
                git.checkout("master")
                git.merge("--no-ff", "update_license_and_copyright")

                print("merged into master")

                #push changes to origin
                repo.remotes.origin.push()
                print("pushed to origin")
    else:
        print("ERROR: " + str(statCode))
        exit()

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
    
    
def editLicense(homePath,repoPath):
    
    shutil.copy2(homePath, repoPath)
 
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