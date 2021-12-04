#coding=utf-8

import os
from FunctionSentEmail import send_GWT_message

from TimeLibs import *
from SentEmailLibs import *
from CrawlLibs import *

from FunctionCrawlPage import *

from ClassHeaders import *
from ClassSubPageInfo import *


def crawlXNGSMainPage() -> SubPageInfo:
    url = 'http://nbw.sztu.edu.cn/xngs.htm'
    html = etree.HTML(requests.get(url,Headers.headers).content.decode('utf-8'))
    PublicityPage = SubPageInfo(
        academy_list= ['']*len(html.xpath('//body/div[4]/div/ul/li')),
        index_list= [re.findall('[0-9]+/[0-9]+',i)[0] for i in html.xpath('//body/div[4]/div/ul/li/a/@href')],
        title_list= html.xpath('//body/div[4]/div/ul/li/a/text()'),
        has_attachment_list= ['?']*len(html.xpath('//body/div[4]/div/ul/li')),
        date_list= html.xpath('//body/div[4]/div/ul/li/span/text()'),
        cache_file_path= './XNGS.previous.cache.txt',
        mode= 'XNGS'
    )
    return PublicityPage

if __name__ == '__main__':
    try:
        os.mkdir('./html-download')
    except:
        pass
    while True:
        pause_hours = 1
        start_time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        Headers = HeadersMoudle(cookie='')
        PublicityPage = crawlXNGSMainPage()
        PublicityPage.academy_list = len(PublicityPage.academy_list) * ['校内公示 ']
        download_web_file(PublicityPage,Headers.headers)
        send_GWT_message(PublicityPage)
        print(1)