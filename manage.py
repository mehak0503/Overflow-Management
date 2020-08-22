import configparser
import os,shutil
import smtplib,ssl
import datetime,time
#import requests

#Function to send email
def send_email():
    try:
        server = smtplib.SMTP(config['EMAIL']['server'], int(config['EMAIL']['port']))
        #server.starttls(context=ssl.create_default_context()) # Secure the connection
        #server.login(config['EMAIL']['sender'], config['EMAIL']['password'])
        server.sendmail(config['EMAIL']['sender'], config['EMAIL']['receiver'], config['EMAIL']['text'])
        print("Successfully sent email")
    except:
       print("Error: unable to send email")

#Function to call RESTFul API
def restAPIcall():
    try:
        response = requests.post(config['RESTAPI']['url'], data=config['RESTAPI']['data'])
        print("RESTAPI call response is ",response)
    except:
        print("Error: RESTAPI call failed")

def getfileCnt(path):
    dirContent = os.listdir(path)
    files = [os.path.join(path,name) for name in dirContent if os.path.isfile(os.path.join(path,name))]
    fileCount = len(files)
    return fileCount


#Read the configuration file
config = configparser.ConfigParser()
config.read('goyal.ini')

#Check the original directory for overflow
path = config['PARAMS']['origdirpath']
dirContent = os.listdir(path)
files = [os.path.join(path,name) for name in dirContent if os.path.isfile(os.path.join(path,name))]
fileCount = len(files)
bound = int(config['PARAMS']['overflowbound'])
if fileCount > bound:
    if config['DEFAULT']['movenewfiles']=='yes':
        files.sort(key = os.path.getctime,reverse=True)
    else:
        files.sort(key = os.path.getctime)
    #if config['DEFAULT']['apicall']=='yes':
    #    restAPIcall()
    cnt = 0
    i = 0
    cntMove = int(config['PARAMS']['movefiles'])
    dirCnt = int(config['PARAMS']['noofdir'])
    while i<dirCnt and len(files)>cnt and getfileCnt(path)>bound:
        margin = getfileCnt(path) - bound
        flag = False
        moveDir = path+str(i)
        if not os.path.isdir(moveDir):
            if margin<cntMove and len(files)>cnt+margin:
                filesToMove = files[cnt:cnt+margin]
                cnt+=margin
            elif len(files)>cnt+cntMove:
                filesToMove = files[cnt:cnt+cntMove]
                cnt+=cntMove
            else:
                filesToMove = files[cnt:]
                flag = True
            os.mkdir(moveDir)
            for file in filesToMove:
                shutil.move(file,moveDir)
        else:
            dirContent = os.listdir(moveDir)
            fileCnt = len([name for name in dirContent if os.path.isfile(os.path.join(moveDir,name))])
            if fileCnt < bound:
                toMove = bound - fileCnt
                if margin<cntMove and margin<toMove and len(files)>cnt+margin:
                    filesToMove = files[cnt:cnt+margin]
                    cnt+=margin
                elif len(files)>cnt+toMove and toMove<cntMove:
                    filesToMove = files[cnt:cnt+toMove]
                    cnt+=toMove
                elif len(files)>cnt+cntMove:
                    filesToMove = files[cnt:cnt+cntMove]
                    cnt+=cntMove
                else:
                    filesToMove = files[cnt:]
                    flag = True
                for file in filesToMove:
                    shutil.move(file,moveDir)
        i+=1
        if flag:
            break
    send_email()
