#coding=utf-8

from FileControl import *
from TimeLibs import *
from SentEmailLibs import *
from CrawlLibs import *
from DefaultHeaders import *


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
    content+='\n'
    content+='\n'
    content+='The message was sent at '+datetime.datetime.now().strftime('%y-%m-%d_%H:%M:%S')+'\n'
    content+='\n'
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

def sentGWTMessage(content,newAnnonucementNum,allHTMLName,allAttachmentName):
    allHTMLName.sort()
    allAttachmentName.sort()
    jsonSendingData=openInfosFile()
    #set sever
    emailSever=smtplib.SMTP_SSL(jsonSendingData["smtpserver"],jsonSendingData["smtpport"])
    emailSever.login(jsonSendingData["fromaddress"],jsonSendingData["qqcode"])
    message = MIMEMultipart()   #define message
    message.attach(MIMEText(content, 'plain', 'utf-8'))
    message['from']=formataddr([jsonSendingData["fromname"],jsonSendingData["fromaddress"]])#sender
    if newAnnonucementNum==0:
        message['Subject'] = Header('No new GWT announcement', 'utf-8')  #email title
    else:
        message['Subject'] = Header(jsonSendingData["title"], 'utf-8')  #email title
    for i in range(len(allHTMLName)):
        HTMLFile=MIMEApplication(open(os.getcwd()+'/html-download/{}.htm'.format(allHTMLName[i]),mode='r',encoding='utf-8').read())
        HTMLFile.add_header('Content-Disposition', 'attachment', filename=allHTMLName[i]+'.htm')
        message.attach(HTMLFile)
    for i in range(len(allAttachmentName)):
        attachmentFile=MIMEApplication(open(os.getcwd()+'/html-download/'+allAttachmentName[i],'rb').read())
        attachmentFile.add_header('Content-Disposition', 'attachment', filename=allAttachmentName[i])
        message.attach(attachmentFile)
    for i in range(len(jsonSendingData["to"])):
        if len(newAnnouncementList)==0 and jsonSendingData['to'][i]["isadmin"]==False:
            print('No new announcement, ignore '+jsonSendingData["to"][i]["name"]+' '+jsonSendingData["to"][i]["address"])
            continue
        message["To"]=formataddr([jsonSendingData["to"][i]["name"],jsonSendingData["to"][i]["address"]])#recever
        try:
            emailSever.sendmail(from_addr=jsonSendingData["fromaddress"], to_addrs=[jsonSendingData["to"][i]["address"]], msg=message.as_string())
            print ('Email sent successfully to '+jsonSendingData["to"][i]['name']+' '+jsonSendingData["to"][i]["address"])
        except Exception as error:
            print ('Email sent failed --> ' + str(error))
    emailSever.quit()

def getGWTPageHTML(page,totalPage):
    if page==1 and totalPage==0:
        html=requests.get(url='http://nbw.sztu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1029',headers=headers).content.decode('utf-8')
    else:
        url='http://nbw.sztu.edu.cn/list.jsp?totalpage='+str(totalPage)+'&PAGENUM='+str(page)+'&urltype=tree.TreeTempUrl&wbtreeid=1029'
        html=requests.get(url=url,headers=headers).content.decode('utf-8')
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

def getHTMLPage(url):
    html=requests.get(url).content.decode('utf-8')
    return html

def downloadWebFile(newAnnouncement):
    allFileName=[]
    allAttachmentName=[]
    for i in range(len(newAnnouncement)):
        htmlIndex=''
        for j in range(len(newAnnouncement[i][1])):
            if newAnnouncement[i][1][-j-1]!='/':
                htmlIndex=newAnnouncement[i][1][-j-1]+htmlIndex
            else:
                break
        fileName=htmlIndex+'_'+newAnnouncement[i][4]+'_'+newAnnouncement[i][2]
        html=etree.HTML(getHTMLPage('http://nbw.sztu.edu.cn/info/'+newAnnouncement[i][1]+'.htm'))
        xpathFinder='//html/body/div/form/div/ul/li'
        attachmentLink=[]
        attachmentDivsNum=len(html.xpath(xpathFinder))
        if attachmentDivsNum>0:
            for l in range(0,attachmentDivsNum):
                allAttachmentName.append(html.xpath(xpathFinder+'/a')[l].text)
                attachmentLink.append(html.xpath(xpathFinder+'/a/@href')[l])
            for j in range(-1,-1-attachmentDivsNum,-1):
                allAttachmentName[j]=htmlIndex+'_'+allAttachmentName[j]
            fileName+='_hasAttachment'
            for k in range(-1,-1-attachmentDivsNum,-1):
                headers['Referer'] = 'http://nbw.sztu.edu.cn/info/'+newAnnouncement[i][1]+'.htm'
                downloadAttachment(attachmentLink[k],allAttachmentName[k])
        saveHTMLpage(etree.tostring(html).decode('utf-8'),fileName)
        allFileName.append(fileName)
    headers['Referer'] = 'http://nbw.sztu.edu.cn/'
    return allFileName,allAttachmentName

def downloadAttachment(URL,fileName):
    r=requests.get(url='http://nbw.sztu.edu.cn/'+URL,stream=True,headers=headers)
    with open(os.getcwd()+'/html-download/'+fileName,mode='wb+') as att:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                att.write(chunk)

if __name__=='__main__':
    try:
        os.mkdir(os.getcwd()+'/html-download')
    except:
        pass
    while True:
        pauseHours=1
        startTime=datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        (announcementInfoList,totalPage)=getGWTPageInfo(1,'',0)
        markRepetedAnnouncement(announcementInfoList)
        saveRecentGWTCode(announcementInfoList)
        newAnnouncementList=separateNewAnnouncement(announcementInfoList)
        emailContent=createEmailContentFromNewAnnouncement(newAnnouncementList)
        print(str(len(newAnnouncementList))+' new announcement(s)')
        allHTMLName,allAttachmentName=downloadWebFile(newAnnouncementList)
        sentGWTMessage(emailContent,len(newAnnouncementList),allHTMLName,allAttachmentName)
        print('Sleep from '+datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')+' to '+(datetime.datetime.now()+datetime.timedelta(hours=pauseHours)).strftime('%Y-%m-%d_%H:%M:%S'))
        time.sleep(pauseHours*3600)