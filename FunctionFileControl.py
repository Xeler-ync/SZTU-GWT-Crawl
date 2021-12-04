import json


def save_recent_page_code(index_list,path) -> None:
    for i in range(len(index_list)):
        index_list[i] = index_list[i].replace('r','')
    write_GWT_previous_cache(index_list,path)
    return None

def write_GWT_previous_cache(num_list,path) -> None: open(file=path,mode='w+',encoding='utf-8').writelines(f'{i}\n' for i in num_list)

def openInfosFile() -> None:#if no, creat one
    try:
        with open(file='./sender.email.acc.pss.json',mode='r',encoding='utf-8') as sea:
            jsonData=json.load(sea)
            return jsonData
    except OSError:
        with open(file='./sender.email.acc.pss.json',mode='w+',encoding='utf-8') as sea:
            sea.writelines('{')
            sea.writelines('    "fromaddress": "",\n')
            sea.writelines('    "fromname": "",\n')
            sea.writelines('    "to": [\n')
            sea.writelines('        {\n')
            sea.writelines('            "name" : "",\n')
            sea.writelines('            "address" : "",\n')
            sea.writelines('            "isadmin" : ,\n')
            sea.writelines('    "qqcode": "",\n')
            sea.writelines('    "smtpserver": "smtp.qq.com",\n')
            sea.writelines('    "smtpport": 465\n')
            sea.writelines('    "title": ""\n')
            sea.writelines('}')
        print('Please correctly fill in the sender.email.acc.pss.json first.')
        input('Press Enter to quit')
        exit()
    return None

# def save_HTML_page(content,name) -> None: open(os.getcwd()+'\\html-download\\'+name+'.htm',mode='w+',encoding='utf-8').write(content)
def save_HTML_page(content,name) -> None:
    with open('./html-download/'+name+'.htm',mode='w+',encoding='utf-8') as f:
        f.write(content)

def replace_illegal_char(ipt) -> str:
    ipt = ipt.replace('<','[半角前尖括号]')
    ipt = ipt.replace('>','[半角后尖括号]')
    ipt = ipt.replace('\\','[半角反斜杠]')
    ipt = ipt.replace('/','[半角正斜杠]')
    ipt = ipt.replace('"','[半角双引号]')
    ipt = ipt.replace('|','[半角竖线]')
    ipt = ipt.replace('?','[半角问号]')
    ipt = ipt.replace('*','[半角星号]')
    ipt = ipt.replace(':','[半角冒号]')
    return ipt

# def write_file(path,content):
#     with open(file=path,mode='w+',encoding='utf-8') as f:
#         f.write(content)
#     return None