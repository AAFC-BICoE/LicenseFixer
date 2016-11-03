# -*- coding: utf-8 -*-
"""
Use this script to manually go through each license of your repos in the same directory as the script

IF NO LICENSE SCRIPT IS FOUND THEN VARIABLE "CorrectLicense" IS AUTOMATICALLY USED

"""

import os
CorrectLicense=\
"""
MIT License

Copyright © 2016 Government of Canada

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
SOFTWARE."""

directoryList = os.listdir(".")
count = 0
countNot=0
for directory in directoryList:
	if(os.path.isdir(directory)):
		licensePath = directory+"/LICENSE";
		if(os.path.exists(licensePath)):
			# count+=1
			licenseFile = open(directory+"/LICENSE", "r")
			print(licenseFile.read())
			keep = raw_input("Correct License?y/n\n")
			if (keep == "n"):
				# licenseFile = open(directory+"/LICENSE", "w")
				# licenseFile.write(CorrectLicense)
				licenseFile.close()
				countNot+=1
			else:
				count+=1
				licenseFile.close()
				continue
		else:
			newLicenseFile = open(directory+"/LICENSE", 'w')
			newLicenseFile.write(CorrectLicense)
			newLicenseFile.close()
			


print(count)
print(countNot)
