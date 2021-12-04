#coding=utf-8

from TimeLibs import *
from CrawlLibs import *

from FunctionFileControl import *
from FunctionCrawlPage import *
from FunctionSentEmail import *

from ClassHeaders import *
from ClassSubPageInfo import *


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
        academy_list= [announcement_info_tuple[i][0] for i in range(len(announcement_info_tuple))],
        index_list= [announcement_info_tuple[i][1] for i in range(len(announcement_info_tuple))],
        title_list= [announcement_info_tuple[i][2] for i in range(len(announcement_info_tuple))],
        has_attachment_list= [announcement_info_tuple[i][3] for i in range(len(announcement_info_tuple))],
        date_list= [announcement_info_tuple[i][4] for i in range(len(announcement_info_tuple))],
        cache_file_path= './GWT.previous.cache.txt',
        mode= 'GWT'
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
        import os
        os.mkdir(os.getcwd()+'/html-download')
    except:
        pass
    while True:
        pause_hours = 1
        start_time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        Headers = HeadersMoudle(cookie='')
        (AnnouncementInfo,total_page) = get_GWT_page_info(1,'',0)
        mark_sent_announcement(AnnouncementInfo)
        save_recent_page_code(AnnouncementInfo.index_list[:],AnnouncementInfo.cache_file_path)
        AnnouncementInfo.remove_duplicate_page()
        AnnouncementInfo.remove_deplicate_mark()
        # new_announcement_list = separate_new_announcement(AnnouncementInfo.attachment_file_list)
        # emailContent = create_email_content_from_new_GWT_announcement(AnnouncementInfo,start_time)
        AnnouncementInfo.creat_email_content(start_time)
        print(str(len(AnnouncementInfo.academy_list))+' new announcement(s)')
        download_web_file(AnnouncementInfo,Headers.headers)
        send_GWT_message(AnnouncementInfo) # ,AnnouncementInfo.HTML_file_list,AnnouncementInfo.attachment_file_list
        print('Sleep from '+datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')+' to '+(datetime.datetime.now()+datetime.timedelta(hours=pause_hours)).strftime('%Y-%m-%d_%H:%M:%S'))
        time.sleep(pause_hours*3600)