'''
Created on November 3rd

@author antbush

This goes through all directories in the folder where this script exists and if there are untracked/modified files
creates a new branch, adds the new License, then pushes

'''
import os
from git import Repo

directoryList = os.listdir(".")
gitDirectoryList =[]
for directory in directoryList:
	if(os.path.isdir(directory)):
		repo = Repo(directory)
		untrackedFiles = repo.untracked_files
		if(repo.is_dirty() or len(untrackedFiles) != 0):

			gitDirectoryList.append(directory)
			git = repo.git()
			git.checkout(b="Support_7754_Github_license_and_copyright_clean_up")
			print("created branch Support_7754_Github_license_and_copyright_clean_up")
			index = repo.index.add(["LICENSE"])
			index.commit("Updated license and copyright")
			print("Added untracked files")
			git = repo.git
			git.checkout("master")
			git.merge("--no-ff", "Support_7754_Github_license_and_copyright_clean_up")
			print("merged into master")
			repo.remotes.origin.push()
			print("Directory: "+ directory)
			# print("Git diff: " + git.diff())
print(len(gitDirectoryList))
