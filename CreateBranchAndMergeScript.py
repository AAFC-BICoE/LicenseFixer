'''
Created on November 3rd

@author antbush

This goes through all directories in the folder where this script exists and if there are untracked/modified files
creates a new branch, adds the new License, then pushes. The final output is the number of all directories visited

'''
import os
from git import Repo

directoryList = os.listdir(".")
gitDirectoryList =[]

for directory in directoryList:
	if(os.path.isdir(directory)):
		repo = Repo(directory)
		untrackedFiles = repo.untracked_files
		# If the repo has modified files or untracked/new files
		if(repo.is_dirty() or len(untrackedFiles) != 0):
			print("Starting Directory: " + directory)
			gitDirectoryList.append(directory)
			git = repo.git()
			branches = git.branch()
			if ("Github_license_and_copyright_clean_up" not in branches):
				git.checkout(b="Github_license_and_copyright_clean_up")
				print("Created branch Github_license_and_copyright_clean_up")
			else:
				git.checkout("Github_license_and_copyright_clean_up")
				print("Switched to branch Github_license_and_copyright_clean_up")
			index = repo.index
			index.add(["LICENSE"])
			index.commit("Updated license and copyright")
			print("Added untracked files")
			git = repo.git
			git.checkout("master")
			git.merge("--no-ff", "Github_license_and_copyright_clean_up")
			print("merged into master")
			repo.remotes.origin.push()
			print("Directory pushed: "+ directory)
print("Number of directories visited: " + len(gitDirectoryList))