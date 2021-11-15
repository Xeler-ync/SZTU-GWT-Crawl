# SZTU-GWT-Crawl
Crawl GWT from SZTU's nbw

## 使用
1. 启动 SZTU-GWT-Crawl.py ，在自动生成的 sender.email.acc.pss.json 中填写信息
2. 再次启动 SZTU-GWT-Crawl.py

## sender.email.acc.pss.json 文件内容
```json
{
    "fromaddress": "",      //发信地址
    "fromname": "",         //发信人
    "to": [                 //收信信息列表
        {                   //
            "name": "",     //收信人
            "address": "",  //收信地址
            "isadmin": true //是否为管理员
        }                   //
    ],                      //
    "qqcode": "",           //授权码
    "smtpserver": "",       //SMTP服务器
    "smtpport": ,           //SMTP端口
    "title": ""             //邮件标题
}
```

## 兼容性
1. 仅测试过Windows 10 20H2平台
2. 仅测试过QQ STMP服务器

## 免责声明
- 截至2021-11-15_15:5，http://nbw.sztu.edu.cn/robots.txt 不存在，且不存在明显的反爬虫
- 本程序所提供的信息，仅供参考之用。所有数据来自深圳技术大学内部网，版权归深圳技术大学及相关发布人所有。
在法律允许的范围内，本程序在此声明，不承担用户或任何人士就使用或未能使用本程序所提供的信息或任何链接或项目所引致的任何直接、间接、附带、从属、特殊、惩罚性或惩戒性的损害赔偿（包括但不限于收益、预期利润的损失或失去的业务、未实现预期的节省）。
- 由于错误或不当使用本程序造成的一切后果与责任，本程序概不负责。
- 通过任何方式使用本程序则视为同意该免责声明。

# 改变

## v1.1
- (2021-11-15)
- > 可以下载页面文件与附件，并作为邮件的附件发送

## v1.0
- (2021-09-17)
- > 可以从nbw的GWT中按照预设的时间间隔爬下第一页，去掉与上一次重复的之后留下新增的，发给目标邮箱