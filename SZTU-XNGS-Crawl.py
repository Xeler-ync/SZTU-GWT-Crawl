#coding=utf-8

from FileControl import *
from TimeLibs import *
from SentEmailLibs import *
from CrawlLibs import *
from DefaultHeaders import *

from ClassSubPageInfo import *


def crawlXNGSMainPage() -> SubPageInfo:
    url = 'http://nbw.sztu.edu.cn/xngs.htm'
    html = etree.HTML(requests.get(url,headers).content.decode('utf-8'))
    PublicityPage = SubPageInfo(
        source_list=html.xpath('//body/div[4]/div/ul/li/a/@href'),
        index_list=[re.findall('info/1024/([0-9]+)\.htm',i,re.S) for i in html.xpath('//body/div[4]/div/ul/li/a/@href')],
        title_list=html.xpath('//body/div[4]/div/ul/li/a/text()'),
        has_attachment_list=['?']*len(html.xpath('//body/div[4]/div/ul/li')),
        date_list=html.xpath('//body/div[4]/div/ul/li/span/text()')
    )
    return PublicityPage

if __name__ == '__main__':
    # crawlXNGSMainPage()
    pass