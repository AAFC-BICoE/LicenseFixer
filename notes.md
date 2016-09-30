Step 1: Setup SSH key
https://confluence.atlassian.com/bitbucket/set-up-ssh-for-git-728138079.html
ssh-keygen, leave no passphrase for the script

IF USING SSH for bitbucket you MUST connect to the host altssh.bitbucket.org, which should be edited in the config
	- Most likely add this to your script to edit the config file
Change default SSH to 443 by going into /etc/ssh/ssh_config and changing '#port 22' to 'port 443'
 
requires requests library from http://docs.python-requests.org/en/master/

requires gitPython library from https://gitpython.readthedocs.io/en/stable/intro.html#requirements

pip install requests

pip install gitpython

repo’s currently saved in home space under repo# ( where # increments for each repo downloaded )
