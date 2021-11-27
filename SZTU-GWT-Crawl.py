#coding=utf-8

from TimeLibs import *
from SentEmailLibs import *
from CrawlLibs import *

from FunctionFileControl import *
from FunctionCrawlPage import *

from ClassHeaders import *
from ClassSubPageInfo import *


def create_email_content_from_new_announcement():
    content = 'There is(are) '+str(len(AnnouncementInfo.academy_list))+' new announcement(s) now!\n'
    content += 'The message was generated at '+start_time+'\n'
    content += '\n'
    for i in range(len(AnnouncementInfo.academy_list)):
        content += '\n'
        content += 'From: '+AnnouncementInfo.academy_list[i]+'\n'
        content += 'Date: '+AnnouncementInfo.date_list[i]+'\n'
        content += 'Tittle: '+AnnouncementInfo.title_list[i]+'\n'
        content += 'Link: '+'http://nbw.sztu.edu.cn/info/'+AnnouncementInfo.index_list[i]+'.htm\n'
        if AnnouncementInfo.has_attachment_list[i].find('1') == -1:
            content += 'Attachment: Flase\n'
        else:
            content += 'Attachment: True\n'
    content += '\n'
    content += '\n'
    content += 'The message was sent at '+datetime.datetime.now().strftime('%y-%m-%d_%H:%M:%S')+'\n'
    content += '\n'
    content += '本程序所提供的信息，仅供参考之用。所有数据来自深圳技术大学内部网，版权归深圳技术大学及相关发布人所有。\n'
    content += '完整的免责声明见程序发布页或向邮件发送者索取'
    return content

# def separate_new_announcement(AnnouncementInfo.attachment_file_list):
    # new_announcement = []
    # for i in range(len(AnnouncementInfo.attachment_file_list)):
    #     if AnnouncementInfo.attachment_file_list[i][3].find('r') == -1:
    #         new_announcement.append(AnnouncementInfo.attachment_file_list[i])
    # return new_announcement

def mark_sent_announcement() -> None:
    with open(file=os.getcwd()+'/GWT.previous.cache.txt',mode='r',encoding='utf-8') as gpc:
        previous_code_list = gpc.readlines()
        for i in range(len(AnnouncementInfo.index_list)):
            for j in range(len(previous_code_list)):
                if (AnnouncementInfo.index_list[i]+'\n') == previous_code_list[j]:
                    AnnouncementInfo.index_list[i] += 'r'
    return None

def send_GWT_message(content): # ,all_HTML_name,an1nouncement_info_list):
    json_sending_data = openInfosFile()
    #set sever
    email_sever = smtplib.SMTP_SSL(json_sending_data["smtpserver"],json_sending_data["smtpport"])
    email_sever.login(json_sending_data["fromaddress"],json_sending_data["qqcode"])
    message = MIMEMultipart()   #define message
    message.attach(MIMEText(content, 'plain', 'utf-8'))
    message['from'] = formataddr([json_sending_data["fromname"],json_sending_data["fromaddress"]])#sender
    if len(AnnouncementInfo.academy_list) == 0:
        message['Subject'] = Header('No new GWT announcement', 'utf-8')  #email title
    else:
        message['Subject'] = Header(json_sending_data["title"], 'utf-8')  #email title
    for i in range(len(AnnouncementInfo.HTML_file_list)):
        HTMLFile = MIMEApplication(open(os.getcwd()+'/html-download/{}.htm'.format(AnnouncementInfo.HTML_file_list[i]),mode='r',encoding='utf-8').read())
        HTMLFile.add_header('Content-Disposition', 'attachment', filename=AnnouncementInfo.HTML_file_list[i]+'.htm')
        message.attach(HTMLFile)
    for i in range(len(AnnouncementInfo.attachment_file_list)):
        attachmentFile = MIMEApplication(open(os.getcwd()+'/html-download/'+AnnouncementInfo.attachment_file_list[i],'rb').read())
        attachmentFile.add_header('Content-Disposition', 'attachment', filename=AnnouncementInfo.attachment_file_list[i])
        message.attach(attachmentFile)
    for i in range(len(json_sending_data["to"])):
        if len(AnnouncementInfo.academy_list) == 0 and not json_sending_data['to'][i]["isadmin"]:
            print('No new announcement, ignore '+json_sending_data["to"][i]["name"]+' '+json_sending_data["to"][i]["address"])
            continue
        message["To"] = formataddr([json_sending_data["to"][i]["name"],json_sending_data["to"][i]["address"]])#recever
        try:
            email_sever.sendmail(from_addr = json_sending_data["fromaddress"], to_addrs=[json_sending_data["to"][i]["address"]], msg=message.as_string())
            print('Email sent successfully to '+json_sending_data["to"][i]['name']+' '+json_sending_data["to"][i]["address"])
        except Exception as error:
            print('Email sent failed --> ' + str(error))
    email_sever.quit()

def get_total_page_from_first_page_HTML(html):
    if html == '':
        html = get_GWT_page_HTML(1,0)
    total_page_finder='上页</span><span class="p_no_d">1</span><span class="p_no"><a href="\?totalpage=([0-9]+)\&PAGENUM=2\&urltype=tree.TreeTempUrl\&wbtreeid=[0-9]+"'
    total_page = re.findall(total_page_finder,html,re.S)
    return total_page[0]

def get_GWT_page_info(page,html,total_page):
    if page == 0: # 提高鲁棒性
        return [['No Page 0']*5]
    if html == '': # 爬主页
        html = get_GWT_page_HTML(1,total_page)
    if total_page == 0:
        total_page = get_total_page_from_first_page_HTML(html)
    html = html.replace('\n','')
    html = html.replace('\r','')
    html = html.replace('<img src="images/fujian.png">','1') # 优化返回的内容
    if page>int(total_page):
        return [['Page too big, max is '+str(total_page)]*5]
    list_finder = 'style="font-size: 14px;">(.*?)</a></div><div class="pull-left width04 txt-elise text-left" style="width:54%;"><a href="info/([0-9]+/[0-9]+).htm" title=".*?" target="_blank" style=".*?">(.*?)</a></div><div class="pull-left width05"  style="width:5%;height:32px;">(.*?)</div><div class="pull-right width06"  style="width:11%;">([0-9-]+)</div></li>'
    announcement_info_tuple = re.findall(list_finder,html,re.S) # ((academy, index, title, hasAttachment, date),*)
    AnnouncementInfo = SubPageInfo(
        academy_list=[announcement_info_tuple[i][0] for i in range(len(announcement_info_tuple))],
        index_list=[announcement_info_tuple[i][1] for i in range(len(announcement_info_tuple))],
        title_list=[announcement_info_tuple[i][2] for i in range(len(announcement_info_tuple))],
        has_attachment_list=[announcement_info_tuple[i][3] for i in range(len(announcement_info_tuple))],
        date_list=[announcement_info_tuple[i][4] for i in range(len(announcement_info_tuple))]
    )
    return AnnouncementInfo, total_page

def get_GWT_page_HTML(page:int,total_page:int):
    url = ''
    if page == 1 and total_page == 0:
        url = 'http://nbw.sztu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1029'
    else:
        url = 'http://nbw.sztu.edu.cn/list.jsp?totalpage='+str(total_page)+'&PAGENUM='+str(page)+'&urltype=tree.TreeTempUrl&wbtreeid=1029'
    return get_HTML_page(url,Headers.headers)

if __name__ == '__main__':
    try:
        os.mkdir(os.getcwd()+'/html-download')
    except:
        pass
    while True:
        pause_hours = 1
        start_time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        Headers = HeadersMoudle(cookie='')
        (AnnouncementInfo,total_page) = get_GWT_page_info(1,'',0)
        mark_sent_announcement()
        save_recent_GWT_code(AnnouncementInfo.index_list)
        AnnouncementInfo.remove_duplicate_page()
        # new_announcement_list = separate_new_announcement(AnnouncementInfo.attachment_file_list)
        emailContent = create_email_content_from_new_announcement()
        print(str(len(AnnouncementInfo.academy_list))+' new announcement(s)')
        download_web_file(AnnouncementInfo,Headers.headers)
        send_GWT_message(emailContent) # ,AnnouncementInfo.HTML_file_list,AnnouncementInfo.attachment_file_list
        print('Sleep from '+datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')+' to '+(datetime.datetime.now()+datetime.timedelta(hours=pause_hours)).strftime('%Y-%m-%d_%H:%M:%S'))
        time.sleep(pause_hours*3600)