#coding=utf-8

from TimeLibs import *
from CrawlLibs import *

from FunctionFileControl import *
from FunctionCrawlPage import *
from FunctionSentEmail import *

from ClassHeaders import *
from ClassSubPageInfo import *


# def get_total_page_from_first_page_HTML(html):
#     if html == '':
#         html = get_XYXW_page_HTML(1,0)
#     total_page_finder='上页</span><span class="p_no_d">1</span><span class="p_no"><a href="\?totalpage=([0-9]+)\&PAGENUM=2\&urltype=tree.TreeTempUrl\&wbtreeid=[0-9]+"'
#     total_page = re.findall(total_page_finder,html,re.S)
#     return total_page[0]

def get_XYXW_page_info() -> SubPageInfo:
    url = 'https://www.sztu.edu.cn/jd_jd1/xyxw.htm'
    html = etree.HTML(requests.get(url=url,headers=Headers.headers,verify=False).content.decode('utf-8'))
    news_count = len(html.xpath('//body/section[3]/div/div[2]/ul/li'))
    NewsInfo = SubPageInfo(
        academy_list= ['']*news_count,
        index_list= [i[8:-4] for i in html.xpath('//body/section[3]/div/div[2]/ul/li/p/a/@href')],
        title_list= html.xpath('//body/section[3]/div/div[2]/ul/li/p/a/text()'),
        has_attachment_list= ['']*news_count,
        date_list= [html.xpath('//body/section[3]/div/div[2]/ul/li/p/text()')[i].replace('\r\n','') for i in range(0,len(html.xpath('//body/section[3]/div/div[2]/ul/li/p/text()')),2)],
        # date_list= html.xpath('//body/section[3]/div/div[2]/ul/li/p/text()'),
        cache_file_path= './XYXW.previous.cache.txt',
        mode= 'XYXW'
    )
    return NewsInfo

def get_XYXW_page_HTML() -> str: return requests.get(url='https://www.sztu.edu.cn/jd_jd1/xyxw.htm',headers=Headers.headers,verify=False).content.decode('utf-8')

if __name__ == '__main__':
    try:
        import os
        # os.mkdir('./html-download')
    except:
        pass
    while True:
        pause_hours = 24
        start_time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        Headers = HeadersMoudle(cookie='',host='www.sztu.edu.cn')
        NewsInfo = get_XYXW_page_info()
        NewsInfo.academy_list = len(NewsInfo.academy_list) * ['校园新闻']
        mark_sent_announcement(NewsInfo)
        save_recent_page_code(NewsInfo.index_list[:],NewsInfo.cache_file_path)
        NewsInfo.remove_duplicate_page()
        NewsInfo.remove_deplicate_mark()
        NewsInfo.creat_email_content(start_time)
        print(str(len(NewsInfo.academy_list))+' new announcement(s)')
        download_web_file(NewsInfo,Headers.headers)
        send_GWT_message(NewsInfo)
        print('Sleep from '+datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')+' to '+(datetime.datetime.now()+datetime.timedelta(hours=pause_hours)).strftime('%Y-%m-%d_%H:%M:%S'))
        time.sleep(pause_hours*3600)