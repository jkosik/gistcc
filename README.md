## About gistcc:
* Gist/Git-commanded Bot 
* `gistcc` parses selected Gist @github, identifies commands and executes them locally.
* Command output is stored back on Gist to provide console look&feel.


## Command examples:
* Create a new Gist: $gistcc.py --new NEW_GIST_NAME --token YOUR_GITHUB_TOKEN
* Run gistcc: $gistcc.py --name GIST_NAME --id GIST_ID --token YOUR_GITHUB_TOKEN
* Delete existing Gist: $gistcc.py --delete --id GIST_ID --token YOUR_GITHUB_TOKEN
    
## Gist command syntax (put the following to your Gist):
* !commmand (first occurence of !command is executed on local machine)
* !cat /etc/passwd
* !xterm mc 
* ?-t20 (sets timeout for command runtime to 20 seconds. Concerns only console commands, not external processes)
  
## Generate GitHub token (Prerequisite)
![Personal Access Token](images/token.png)


## Generate GitHub token (Prerequisite)
![Personal Access Token](images/token.png)

## Create new Gist
* manually via GitHub GUI
* using `gistcc` directly (provides back Gist ID - needed for the following command execution)
```
juraj@home:/tmp/gistcc$ python3 gistcc.py --new test --token CHANGE_ME
Your new Gist Name is: test
Your new Gist ID is: 123456789123456789123456789
Ready to run: $gistcc.py --name test --id 123456789123456789123456789 --token CHANGE_ME
```

![New Gist created](images/newgist.png)


## Start Bot on remote machine
```
juraj@home:/tmp/gistcc$ python3 gistcc.py --name test --id 123456789123456789123456789 --token CHANGEME
```
...and now manage the remote machine via Gist edits


After All exclamation marks are switched to comment sign (hashtag) to start next round in clean setup.

