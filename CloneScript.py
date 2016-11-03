"""
This script contains hardcoded values for an excel file used to clone repos and should be considered a work in progress

"""

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import openpyxl
import os
import sys
from git import Repo


workb = openpyxl.load_workbook("Git_repo_license_summary.xlsx")
works = workb.get_active_sheet()

for row in works.rows:
	url = row[3].value
	if(url == None or url == "REPO URL"):
		continue
	url = url.strip()
	print("cloning project: " + url[28:])
	if(not os.path.exists(url[28:])):
		repo = Repo.clone_from(url, "./"+url[28:])
	print(url[28:] + " Done")
