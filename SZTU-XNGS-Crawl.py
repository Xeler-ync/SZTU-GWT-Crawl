#coding=utf-8

from FileControl import *
from TimeLibs import *
from SentEmailLibs import *
from CrawlLibs import *

from ClassHeaders import *
from ClassSubPageInfo import *


def crawlXNGSMainPage() -> SubPageInfo:
    url = 'http://nbw.sztu.edu.cn/xngs.htm'
    html = etree.HTML(requests.get(url,headers.headers).content.decode('utf-8'))
    PublicityPage = SubPageInfo(
        academy_list = ['']*len(html.xpath('//body/div[4]/div/ul/li')),
        index_list = html.xpath('//body/div[4]/div/ul/li/a/@href'),
        title_list = html.xpath('//body/div[4]/div/ul/li/a/text()'),
        has_attachment_list = ['?']*len(html.xpath('//body/div[4]/div/ul/li')),
        date_list = html.xpath('//body/div[4]/div/ul/li/span/text()')
    )
    return PublicityPage

if __name__ == '__main__':
    headers = HeadersMoudle(cookie='')
    PublicityPage = crawlXNGSMainPage()
    pass