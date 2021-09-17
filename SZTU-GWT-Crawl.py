#coding=utf-8

import smtplib
import os
import re
import requests
import json
import time
import datetime
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header
headers={
    'Referer' : 'http://nbw.sztu.edu.cn/',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
}
startTime=''
pauseHours=1


def createEmailContentFromNewAnnouncement(newAnnouncement):
    content='There is(are) '+str(len(newAnnouncement))+' new announcement(s) now!\n'
    content+='The message was generated at '+startTime+'\n'
    content+='\n'
    for i in range(len(newAnnouncement)):
        content+='\n'
        content+='From: '+newAnnouncement[i][0]+'\n'
        content+='Date: '+newAnnouncement[i][4]+'\n'
        content+='Tittle: '+newAnnouncement[i][2]+'\n'
        content+='Link: '+'http://nbw.sztu.edu.cn/info/'+newAnnouncement[i][1]+'.htm\n'
        if newAnnouncement[i][3].find('1')==-1:
            content+='Attachment: Flase\n'
        else:
            content+='Attachment: True\n'
    content+='The message was sent at '+datetime.datetime.now().strftime('%y-%m-%d_%H:%M:%S')+'\n'
    content+='本程序所提供的信息，仅供参考之用。所有数据来自深圳技术大学内部网，版权归深圳技术大学及相关发布人所有。\n'
    content+='完整的免责声明见程序发布页或向邮件发送者索取'
    return content

def separateNewAnnouncement(announcementInfoList):
    newAnnouncement=[]
    for i in range(len(announcementInfoList)):
        if announcementInfoList[i][3].find('r')==-1:
            newAnnouncement.append(announcementInfoList[i])
    return newAnnouncement

def markRepetedAnnouncement(announcementInfoList):
    with open(file=os.getcwd()+'/GWT.previous.cache.txt',mode='r',encoding='utf-8') as gpc:
        previousCodeList=gpc.readlines()
        for i in range(len(announcementInfoList)):
            for j in range(len(previousCodeList)):
                if (announcementInfoList[i][1]+'\n')==previousCodeList[j]:
                    announcementInfoList[i][3]+='r'
    return

def saveRecentGWTCode(announcementInfoList):
    codeList=[]
    for i in range(len(announcementInfoList)):
        codeList.append(announcementInfoList[i][1]+'\n')
    writeGWTPreviousCache(codeList)
    return

def writeGWTPreviousCache(numList):
    with open(file=os.getcwd()+'/GWT.previous.cache.txt',mode='w+',encoding='utf-8') as gpc:
        gpc.writelines(numList)
    return

def sentGWTMessage(content):
    jsonSendingData=openInfosFile()
    #set sever
    emailSever=smtplib.SMTP_SSL(jsonSendingData["smtpserver"],jsonSendingData["smtpport"])
    emailSever.login(jsonSendingData["fromaddress"],jsonSendingData["qqcode"])
    message = MIMEText(content, 'plain', 'utf-8')   #define message
    message['from']=formataddr([jsonSendingData["fromname"],jsonSendingData["fromaddress"]])#sender
    message['Subject'] = Header(jsonSendingData["title"], 'utf-8')  #email title
    for i in range(len(jsonSendingData["toname"])):
        message["To"]=formataddr([jsonSendingData["toname"][i],jsonSendingData["toaddress"][i]])#recever
        try:
            emailSever.sendmail(jsonSendingData["fromaddress"], jsonSendingData["toaddress"][i], message.as_string())
            print ('Email sent successfully to '+jsonSendingData["toname"][i]+' '+jsonSendingData["toaddress"][i])
        except Exception as error:
            print ('Email sent failed --' + str(error))
    emailSever.quit()

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
            sea.writelines('    "toaddress": [\n')
            sea.writelines('        ""\n')
            sea.writelines('    ],\n')
            sea.writelines('    "toname": [\n')
            sea.writelines('        ""\n')
            sea.writelines('    ],\n')
            sea.writelines('    "qqcode": "",\n')
            sea.writelines('    "smtpserver": "smtp.qq.com",\n')
            sea.writelines('    "smtpport": 465\n')
            sea.writelines('    "title": ""\n')
            sea.writelines('}')
            print('Please correctly fill in the sender.email.acc.pss.json first.')
            input('Press Enter to quit')
            exit()

def getGWTPageHTML(page,totalPage):
    if page==1 and totalPage==0:
        html=requests.get(url='http://nbw.sztu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1029',headers=headers).content.decode('utf-8')
    else:
        url='http://nbw.sztu.edu.cn/list.jsp?totalpage='+str(totalPage)+'&PAGENUM='+str(page)+'&urltype=tree.TreeTempUrl&wbtreeid=1029'
        html=requests.get(url=url,headers=headers).content.decode('utf-8')
    #http://nbw.sztu.edu.cn/list.jsp?totalpage=236&PAGENUM=2&urltype=tree.TreeTempUrl&wbtreeid=1029
    return html

def getTotalPageFromFirstPageHTML(html):
    if html=='':
        html=getGWTPageHTML(1,0)
    totalPageFinder='上页</span><span class="p_no_d">1</span><span class="p_no"><a href="\?totalpage=([0-9]+)\&PAGENUM=2\&urltype=tree.TreeTempUrl\&wbtreeid=[0-9]+"'
    totalPage=re.findall(totalPageFinder,html,re.S)
    return totalPage[0]

def getGWTPageInfo(page,html,totalPage):
    if page==0:
        return [['No Page 0']*5]
    if html=='':
        html=getGWTPageHTML(1,totalPage)
    if totalPage==0:
        totalPage=getTotalPageFromFirstPageHTML(html)
    html=html.replace('\n','')
    html=html.replace('\r','')
    html=html.replace('<img src="images/fujian.png">','1')#优化返回的内容
    if page>int(totalPage):
        return [['Page too big, max is '+str(totalPage)]*5]
    listFinder='style="font-size: 14px;">(.*?)</a></div><div class="pull-left width04 txt-elise text-left" style="width:54%;"><a href="info/([0-9]+/[0-9]+).htm" title=".*?" target="_blank" style=".*?">(.*?)</a></div><div class="pull-left width05"  style="width:5%;height:32px;">(.*?)</div><div class="pull-right width06"  style="width:11%;">([0-9-]+)</div></li>'
    announcementInfoTuple=re.findall(listFinder,html,re.S)#source, index, title, hasAttachment, date
    announcementInfoList=list(announcementInfoTuple)
    for i in range(len(announcementInfoList)):
        announcementInfoList[i]=list(announcementInfoList[i])
    return announcementInfoList, totalPage

if __name__=='__main__':
    while True:
        startTime=datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        (announcementInfoList,totalPage)=getGWTPageInfo(1,'',0)
        markRepetedAnnouncement(announcementInfoList)
        saveRecentGWTCode(announcementInfoList)
        newAnnouncementList=separateNewAnnouncement(announcementInfoList)
        emailContent=createEmailContentFromNewAnnouncement(newAnnouncementList)
        print(str(len(newAnnouncementList))+' new announcement(s)')
        sentGWTMessage(emailContent)
        print('Sleep from '+datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')+' to '+(datetime.datetime.now()+datetime.timedelta(hours=pauseHours)).strftime('%Y-%m-%d_%H:%M:%S'))
        time.sleep(pauseHours*3600)