#coding=utf-8

from CrawlLibs import *

from ClassHeaders import *
from ClassSubPageInfo import *


def download_web_file(SubPageInfo:SubPageInfo,headers:dict) -> None:
    from FunctionFileControl import replace_illegal_char
    from FunctionFileControl import save_HTML_page
    for i in range(len(SubPageInfo.academy_list)):
        page_index = re.findall('/([0-9]+)',SubPageInfo.index_list[i],re.S)[0]
        HTML_file_name = replace_illegal_char(page_index+'_'+SubPageInfo.date_list[i]+'_'+SubPageInfo.title_list[i])
        html = etree.HTML(get_HTML_page(f'http://{headers["Host"]}/info/'+SubPageInfo.index_list[i]+'.htm',headers))
        xpath_finder = '//div/form/div/ul/li'
        attachment_link = []
        attachment_divs_num = len(html.xpath(xpath_finder))
        if attachment_divs_num>0:
            for l in range(0,attachment_divs_num):
                SubPageInfo.add_attachment_file(replace_illegal_char(html.xpath(xpath_finder+'/a')[l].text))
                attachment_link.append(html.xpath(xpath_finder+'/a/@href')[l])
            for j in range(-1,-1-attachment_divs_num,-1):
                SubPageInfo.attachment_file_list[j] = page_index+'_'+SubPageInfo.attachment_file_list[j]
            HTML_file_name += '_hasAttachment'
            for k in range(-1,-1-attachment_divs_num,-1):
                headers['Referer'] = f'http://{headers["Host"]}/info/'+SubPageInfo.index_list[i]+'.htm'
                download_attachment(attachment_link[k],SubPageInfo.attachment_file_list[k],headers)
        save_HTML_page(etree.tostring(html).decode('utf-8'),HTML_file_name)
        SubPageInfo.add_HTML_file(HTML_file_name)
    headers['Referer'] = 'http://nbw.sztu.edu.cn/'
    return None

def get_HTML_page(url:str,headers:dict):
    respond = requests.get(url=url,headers=headers,verify=False)
    if not headers['Cookie']:
        cookie_str = ''
        for key,value in requests.utils.dict_from_cookiejar(respond.cookies).items():
            cookie_str += key + '=' + value
        headers['Cookie'] = cookie_str
    headers['Referer'] = url
    return respond.content.decode('utf-8')

def download_attachment(url:str,file_name:str,headers:dict):
    r = requests.get(url='http://nbw.sztu.edu.cn/'+url,stream=True,headers=headers)
    with open('./html-download/'+file_name,mode='wb+') as att:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                att.write(chunk)