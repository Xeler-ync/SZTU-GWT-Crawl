import os
import json


def saveRecentGWTCode(announcementInfoList):
    codeList=[]
    for i in range(len(announcementInfoList)):
        codeList.append(announcementInfoList[i][1]+'\n')
    writeGWTPreviousCache(codeList)
    return

def writeGWTPreviousCache(numList):
    # writeFile('./GWT.previous.cache.txt',numList)
    open(file=os.getcwd()+'/GWT.previous.cache.txt',mode='w+',encoding='utf-8').writelines(numList)
    return None

def openInfosFile():#if no, creat one
    try:
        with open(file=os.getcwd()+'/sender.email.acc.pss.json',mode='r',encoding='utf-8') as sea:
            jsonData=json.load(sea)
            return jsonData
    except OSError:
        with open(file=os.getcwd()+'/sender.email.acc.pss.json',mode='w+',encoding='utf-8') as sea:
            sea.writelines('{')
            sea.writelines('    "fromaddress": "",\n')
            sea.writelines('    "fromname": "",\n')
            sea.writelines('    "to": [\n')
            sea.writelines('        {\n')
            sea.writelines('            "name" : "",\n')
            sea.writelines('            "address" : "",\n')
            sea.writelines('            "isadmin" : ,\n')
            sea.writelines('    "qqcode": "",\n')
            sea.writelines('    "smtpserver": "smtp.qq.com",\n')
            sea.writelines('    "smtpport": 465\n')
            sea.writelines('    "title": ""\n')
            sea.writelines('}')
        print('Please correctly fill in the sender.email.acc.pss.json first.')
        input('Press Enter to quit')
        exit()

def saveHTMLpage(content,name):
    # writeFile('./html-download/%s.htm' % name,content)
    open(os.getcwd()+'/html-download/'+name+'.htm',mode='w+',encoding='utf-8').write(content)
    return None

def writeFile(path,content):
    with open(file=path,mode='w+',encoding='utf-8') as f:
        f.write(content)
    return None