#coding=utf-8

from requests.models import Response
from FileControl import *
from TimeLibs import *
from SentEmailLibs import *
from CrawlLibs import *
from DefaultHeaders import *


def crawlXNGSMainPage():
    url = 'http://nbw.sztu.edu.cn/xngs.htm'
    html = etree.HTML(requests.get(url,headers).content.decode('utf-8'))
    