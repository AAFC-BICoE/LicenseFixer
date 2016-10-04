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
import csv
from itertools import islice

csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\n',
    quoting = csv.QUOTE_MINIMAL)


html_str_start = """
<table border=1>
     <tr>
       <th>Repo</th>
       <th>Repo License File</th>
       <th>License HEAD - first 10 lines</th>
     </tr>
"""

html_str_end = """
</table>
"""

html_str_data_start = """
       <tr>
         <td>
"""

html_str_data_end = """
</td>
       </tr>
"""

DefaultLicense = "MIT License\n"
correctCopyrightHolder = "Government of Canada"

def cloneRepos(overwrite, dryrun):
    username = sys.argv[1]
    password = getpass.getpass("Input password: ")

    #TODO add in if /else to check for ORG vs user repo's
    #TODO add in if/else when dealing with Github vs bitbucket
    baseBitbucketHttp = "https://bitbucket.org/"+username + "/"
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
    
    Html_file= open("htmlreport.html","w")
    Html_file.write(html_str_start)

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
            cloneURL = sshBitBucket + name + ".git"
            print(sshBitBucket + name + ".git")
            repoPathName = path.join(homePath, homePath+ "/repos/" +name)
            repo = Repo.clone_from(sshBitBucket + name + ".git",repoPathName)
            #check if license is correct
            homeLicensePath = path.join(homePath,homePath+"/LICENSE")
            licensePath = path.join(repoPathName,repoPathName+"/LICENSE")
            licenseUpdated = False
            
            if path.exists(licensePath):
                (equality,copyrightDate,fileToStr, headOfFile) = isLicenseEqual(licensePath, DefaultLicense,homePath, cloneURL)
                if(equality and overwrite):
                    #editLicense(homeLicensePath, licensePath)
                    licenseUpdated = True
                elif(not equality):
                    print("License doesn't match")
                    print("License is not MIT logging to file")
                    oFile = open(homePath+"/report.csv",'a')
                    wr = csv.writer(oFile, quoting=csv.QUOTE_ALL)
                    outputLine = [fileToStr.rstrip(), cloneURL]
                    wr.writerow(outputLine)
                    oFile.close()
                    
                    linkString = '<a target="_blank" href="' + "file://" + licensePath+'">' + licensePath + "</a>"
                    headString = str(headOfFile).strip("[]")
                    headString = headString.replace('\\n', '<br />').replace(",","").replace("'","")
                    repoHttpURL = '<a target="_blank" href="' + baseBitbucketHttp+name+'">' + baseBitbucketHttp+name + "</a>"
                    
                    html_row = html_str_data_start + repoHttpURL + "</td>" + "<td>" + linkString + "</td>" + "<td>" + headString + html_str_data_end 
                    
                    Html_file.write(html_row)
                    
                    continue
            else:
                print("License doesn't exist")
#                 repo.git.checkout(b="update_license_and_copyright")
#                 print("created branch update_license_and_copyright")
#                 editLicense(homeLicensePath, licensePath)
                licenseUpdated = True
                
            if(not dryrun):
                repo.git.checkout(b="update_license_and_copyright")
                print("created branch update_license_and_copyright")
                editLicense(homeLicensePath, licensePath)
                
                
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
        Html_file.write(html_str_end)
        Html_file.close()
    else:
        Html_file.write(html_str_end)
        Html_file.close()
        print("ERROR: " + str(statCode))
        exit()

def isLicenseEqual(file1,myLicense,homePath,cloneURL):
    oFile = open(file1,'r')
    oFile2 = open(file1,'r')
    fileToStr = oFile.readline()
    oFile.readline()
    copyrightDate = oFile.readline()
    copyrightHolder = copyrightDate[18:-1]
    copyrightDate = copyrightDate[:18]
    headOfFile = list(islice(oFile2, 10))
    print(fileToStr == myLicense)
    print(copyrightHolder == correctCopyrightHolder)
    print ("First line of License file is : " + fileToStr.rstrip())
    print ("Copyrightholder: " + copyrightHolder)
    if (fileToStr == myLicense):
        print("License is MIT")
        return (True, copyrightDate, fileToStr, headOfFile)
    else:
        print("License is not MIT")
#         oFile = open(homePath+"/report.csv",'a')
#         wr = csv.writer(oFile, quoting=csv.QUOTE_ALL)
#         outputLine = [fileToStr.rstrip(), cloneURL]
#         wr.writerow(outputLine)
#         oFile.close()
        return (False, "Copyright (c) " + str(datetime.datetime.now().year) + " ", fileToStr, headOfFile)
    
def editLicense(homeLicensePath,repoPath):
    shutil.copy2(homeLicensePath, repoPath)
    
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