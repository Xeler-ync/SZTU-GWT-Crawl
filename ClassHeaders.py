#coding=utf-8

class HeadersMoudle:
    def __init__(self,cookie) -> None:
        self.headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': cookie,
            'Host': 'nbw.sztu.edu.cn',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'http://nbw.sztu.edu.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        }

    def get_cookie(self,website) -> str:
        from requests import get
        from requests.utils import dict_from_cookiejar
        cookie_str = ''
        if website == 'GWT':
            for key,value in dict_from_cookiejar(get(url='http://nbw.sztu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1020').cookies).items():
                cookie_str += key + '=' + value
        elif website == 'XNGS':
            for key,value in dict_from_cookiejar(get(url='http://nbw.sztu.edu.cn/system/resource/code/datainput.jsp?owner=1728834619&e=1&w=1920&h=1080&treeid=1024&refer=&pagename=L3B0X2xpc3QuanNw&newsid=-1').cookies):
                cookie_str += key + '=' + value
        return cookie_str