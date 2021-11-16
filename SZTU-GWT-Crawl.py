#coding=utf-8

from FileControl import *
from TimeLibs import *
from SentEmailLibs import *
from CrawlLibs import *
from DefaultHeaders import *


def create_email_content_from_new_announcement(new_announcement):
    content = 'There is(are) '+str(len(new_announcement))+' new announcement(s) now!\n'
    content += 'The message was generated at '+start_time+'\n'
    content += '\n'
    for i in range(len(new_announcement)):
        content += '\n'
        content += 'From: '+new_announcement[i][0]+'\n'
        content += 'Date: '+new_announcement[i][4]+'\n'
        content += 'Tittle: '+new_announcement[i][2]+'\n'
        content += 'Link: '+'http://nbw.sztu.edu.cn/info/'+new_announcement[i][1]+'.htm\n'
        if new_announcement[i][3].find('1') == -1:
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

def separate_new_announcement(announcement_info_list):
    new_announcement = []
    for i in range(len(announcement_info_list)):
        if announcement_info_list[i][3].find('r') == -1:
            new_announcement.append(announcement_info_list[i])
    return new_announcement

def mark_sent_announcement(announcement_info_list):
    with open(file=os.getcwd()+'/GWT.previous.cache.txt',mode='r',encoding='utf-8') as gpc:
        previous_code_list = gpc.readlines()
        for i in range(len(announcement_info_list)):
            for j in range(len(previous_code_list)):
                if (announcement_info_list[i][1]+'\n') == previous_code_list[j]:
                    announcement_info_list[i][3] += 'r'
    return

def send_GWT_message(content,new_annonucement_num,all_HTML_name,announcement_info_list):
    all_HTML_name.sort()
    announcement_info_list.sort()
    json_sending_data = openInfosFile()
    #set sever
    email_sever = smtplib.SMTP_SSL(json_sending_data["smtpserver"],json_sending_data["smtpport"])
    email_sever.login(json_sending_data["fromaddress"],json_sending_data["qqcode"])
    message = MIMEMultipart()   #define message
    message.attach(MIMEText(content, 'plain', 'utf-8'))
    message['from'] = formataddr([json_sending_data["fromname"],json_sending_data["fromaddress"]])#sender
    if new_annonucement_num == 0:
        message['Subject'] = Header('No new GWT announcement', 'utf-8')  #email title
    else:
        message['Subject'] = Header(json_sending_data["title"], 'utf-8')  #email title
    for i in range(len(all_HTML_name)):
        HTMLFile = MIMEApplication(open(os.getcwd()+'/html-download/{}.htm'.format(all_HTML_name[i]),mode='r',encoding='utf-8').read())
        HTMLFile.add_header('Content-Disposition', 'attachment', filename=all_HTML_name[i]+'.htm')
        message.attach(HTMLFile)
    for i in range(len(announcement_info_list)):
        attachmentFile = MIMEApplication(open(os.getcwd()+'/html-download/'+announcement_info_list[i],'rb').read())
        attachmentFile.add_header('Content-Disposition', 'attachment', filename=announcement_info_list[i])
        message.attach(attachmentFile)
    for i in range(len(json_sending_data["to"])):
        if len(newAnnouncementList) == 0 and not json_sending_data['to'][i]["isadmin"]:
            print('No new announcement, ignore '+json_sending_data["to"][i]["name"]+' '+json_sending_data["to"][i]["address"])
            continue
        message["To"] = formataddr([json_sending_data["to"][i]["name"],json_sending_data["to"][i]["address"]])#recever
        try:
            email_sever.sendmail(from_addr = json_sending_data["fromaddress"], to_addrs=[json_sending_data["to"][i]["address"]], msg=message.as_string())
            print('Email sent successfully to '+json_sending_data["to"][i]['name']+' '+json_sending_data["to"][i]["address"])
        except Exception as error:
            print('Email sent failed --> ' + str(error))
    email_sever.quit()

def get_GWT_page_HTML(page,total_page):
    if page == 1 and total_page == 0:
        return requests.get(url='http://nbw.sztu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1029',headers=headers).content.decode('utf-8')
    else:
        url = 'http://nbw.sztu.edu.cn/list.jsp?totalpage='+str(total_page)+'&PAGENUM='+str(page)+'&urltype=tree.TreeTempUrl&wbtreeid=1029'
        return requests.get(url=url,headers=headers).content.decode('utf-8')

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
    announcement_info_tuple = re.findall(list_finder,html,re.S) # source, index, title, hasAttachment, date
    announcement_info_list = list(announcement_info_tuple)
    for i in range(len(announcement_info_list)):
        announcement_info_list[i] = list(announcement_info_list[i])
    return announcement_info_list, total_page

def get_HTML_page(url): return requests.get(url).content.decode('utf-8')

def downloadWebFile(new_announcement):
    all_file_name = []
    announcement_info_list = []
    for i in range(len(new_announcement)):
        html_index = ''
        for j in range(len(new_announcement[i][1])):
            if new_announcement[i][1][-j-1]!='/':
                html_index = new_announcement[i][1][-j-1]+html_index
            else:
                break
        file_name = html_index+'_'+new_announcement[i][4]+'_'+new_announcement[i][2]
        html = etree.HTML(get_HTML_page('http://nbw.sztu.edu.cn/info/'+new_announcement[i][1]+'.htm'))
        xpath_finder = '//html/body/div/form/div/ul/li'
        attachment_link = []
        attachment_divs_num = len(html.xpath(xpath_finder))
        if attachment_divs_num>0:
            for l in range(0,attachment_divs_num):
                announcement_info_list.append(html.xpath(xpath_finder+'/a')[l].text)
                attachment_link.append(html.xpath(xpath_finder+'/a/@href')[l])
            for j in range(-1,-1-attachment_divs_num,-1):
                announcement_info_list[j] = html_index+'_'+announcement_info_list[j]
            file_name += '_hasAttachment'
            for k in range(-1,-1-attachment_divs_num,-1):
                headers['Referer'] = 'http://nbw.sztu.edu.cn/info/'+new_announcement[i][1]+'.htm'
                download_attachment(attachment_link[k],announcement_info_list[k])
        save_HTML_page(etree.tostring(html).decode('utf-8'),file_name)
        all_file_name.append(file_name)
    headers['Referer'] = 'http://nbw.sztu.edu.cn/'
    return all_file_name,announcement_info_list

def download_attachment(URL,file_name):
    r = requests.get(url='http://nbw.sztu.edu.cn/'+URL,stream=True,headers=headers)
    with open(os.getcwd()+'/html-download/'+file_name,mode='wb+') as att:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                att.write(chunk)

if __name__ == '__main__':
    try:
        os.mkdir(os.getcwd()+'/html-download')
    except:
        pass
    while True:
        pause_hours = 1
        start_time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        (announcement_info_list,total_page) = get_GWT_page_info(1,'',0)
        mark_sent_announcement(announcement_info_list)
        save_recent_GWT_code(announcement_info_list)
        newAnnouncementList = separate_new_announcement(announcement_info_list)
        emailContent = create_email_content_from_new_announcement(newAnnouncementList)
        print(str(len(newAnnouncementList))+' new announcement(s)')
        all_HTML_name,announcement_info_list = downloadWebFile(newAnnouncementList)
        send_GWT_message(emailContent,len(newAnnouncementList),all_HTML_name,announcement_info_list)
        print('Sleep from '+datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')+' to '+(datetime.datetime.now()+datetime.timedelta(hours=pause_hours)).strftime('%Y-%m-%d_%H:%M:%S'))
        time.sleep(pause_hours*3600)