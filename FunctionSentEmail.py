#coding=utf-8

from TimeLibs import *
from SentEmailLibs import *

from FunctionFileControl import openInfosFile


def create_email_content_from_new_GWT_announcement(AnnouncementInfo,start_time):
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
    content += 'The message was sent at '+'datetime.datetime.now().strftime("%y-%m-%d_%H:%M:%S")'+'\n'
    content += '\n'
    content += '本程序所提供的信息，仅供参考之用。所有数据来自深圳技术大学内部网，版权归深圳技术大学及相关发布人所有。\n'
    content += '完整的免责声明见程序发布页或向邮件发送者索取'
    return content

def mark_sent_announcement(AnnouncementInfo) -> None:
    with open(file=AnnouncementInfo.cache_file_path,mode='r',encoding='utf-8') as gpc:
        previous_code_list = gpc.readlines()
        for i in range(len(AnnouncementInfo.index_list)):
            for j in range(len(previous_code_list)):
                if (AnnouncementInfo.index_list[i]+'\n') == previous_code_list[j]:
                    AnnouncementInfo.index_list[i] += 'r'
    return None

def send_GWT_message(AnnouncementInfo):
    json_sending_data = openInfosFile()
    #set sever
    email_sever = smtplib.SMTP_SSL(json_sending_data["smtpserver"],json_sending_data["smtpport"])
    email_sever.login(json_sending_data["fromaddress"],json_sending_data["qqcode"])
    message = MIMEMultipart()   #define message
    message['from'] = formataddr([json_sending_data["fromname"],json_sending_data["fromaddress"]])#sender
    if len(AnnouncementInfo.academy_list) == 0:
        message['Subject'] = Header('No new '+AnnouncementInfo.mode+' announcement', 'utf-8')  #email title
    else:
        message['Subject'] = Header('New '+AnnouncementInfo.mode+' announcement', 'utf-8')  #email title
    for i in range(len(AnnouncementInfo.HTML_file_list)):
        HTMLFile = MIMEApplication(open('./html-download/{}.htm'.format(AnnouncementInfo.HTML_file_list[i]),mode='r',encoding='utf-8').read())
        HTMLFile.add_header('Content-Disposition', 'attachment', filename=AnnouncementInfo.HTML_file_list[i]+'.htm')
        message.attach(HTMLFile)
    for i in range(len(AnnouncementInfo.attachment_file_list)):
        attachmentFile = MIMEApplication(open('./html-download/'+AnnouncementInfo.attachment_file_list[i],'rb').read())
        attachmentFile.add_header('Content-Disposition', 'attachment', filename=AnnouncementInfo.attachment_file_list[i])
        message.attach(attachmentFile)
    AnnouncementInfo.content = AnnouncementInfo.content.replace('datetime.datetime.now().strftime("%y-%m-%d_%H:%M:%S")',datetime.datetime.now().strftime("%y-%m-%d_%H:%M:%S"))
    message.attach(MIMEText(AnnouncementInfo.content, 'plain', 'utf-8'))
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