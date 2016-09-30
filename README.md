# License Fixer 

A Python script which will correct the license and copyright information for Github or Bitbucket repositories in an organization or user space.

Required Software
-----------------
	SSH
	ssh-keygen
	Python 2.7
	Git
	
Required Python Modules
-----------------------
	
	requests - http://docs.python-requests.org/en/master/
	gitpython - https://gitpython.readthedocs.io/en/stable/intro.html#requirements
	
Installing Python Modules with pip
----------------------------------
	
	pip install requests
	pip install gitpython
	
Running the script
----------------------

    $ git clone https://github.com/AAFC-MBB/hpdb.git
    $ cd LicenseFixer
    $ python licenseFixer.py username [-o overwrite] [-d Dryrun]
    
The script will then prompt you for your git password
	



	
Authors and Contact Info
------------------------
	
	Project Group email: mbb@agr.gc.ca
	Project Developer: Anthony Bushara
    Project Developer: Satpal Bilkhu - Satpal.Bilkhu@agr.gc.ca

