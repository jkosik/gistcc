# About gistcc:
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
  
**Prerequisite: existing account on GitHub with generated access token to Git**
## Generate GitHub token
![Personal Access Token](images/token.png)


After All exclamation marks are switched to comment sign (hashtag) to start next round in clean setup.

