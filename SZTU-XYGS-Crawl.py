#coding=utf-8

import os
from FunctionSentEmail import send_GWT_message

from TimeLibs import *
from SentEmailLibs import *
from CrawlLibs import *

from FunctionCrawlPage import *
from FunctionFileControl import *
from FunctionSentEmail import *

from ClassHeaders import *
from ClassSubPageInfo import *


def crawlXYGSMainPage() -> SubPageInfo:
    url = 'http://nbw.sztu.edu.cn/xngs.htm'
    html = etree.HTML(requests.get(url,Headers.headers).content.decode('utf-8'))
    PublicityPage = SubPageInfo(
        academy_list= ['']*len(html.xpath('//body/div[4]/div/ul/li')),
        index_list= [re.findall('[0-9]+/[0-9]+',i)[0] for i in html.xpath('//body/div[4]/div/ul/li/a/@href')],
        title_list= html.xpath('//body/div[4]/div/ul/li/a/text()'),
        has_attachment_list= ['?']*len(html.xpath('//body/div[4]/div/ul/li')),
        date_list= html.xpath('//body/div[4]/div/ul/li/span/text()'),
        cache_file_path= './XYGS.previous.cache.txt',
        mode= 'XYGS'
    )
    return PublicityPage

if __name__ == '__main__':
    try:
        os.mkdir('./html-download')
    except:
        pass
    while True:
        pause_hours = 24
        start_time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        Headers = HeadersMoudle(cookie='')
        PublicityPage = crawlXYGSMainPage()
        PublicityPage.academy_list = len(PublicityPage.academy_list) * ['校内公示 ']
        mark_sent_announcement(PublicityPage)
        save_recent_page_code(PublicityPage.index_list[:],PublicityPage.cache_file_path)
        PublicityPage.remove_duplicate_page()
        PublicityPage.remove_deplicate_mark()
        PublicityPage.creat_email_content(start_time)
        download_web_file(PublicityPage,Headers.headers)
        print(str(len(PublicityPage.academy_list))+' new announcement(s)')
        send_GWT_message(PublicityPage)