#!/usr/bin/python
#coding: utf-8

## python程序本地发送邮件

import smtplib
from email.mime.text import MIMEText

## 这个sender好像可以随便写
sender = 'localhost@localhost.com'
## 好像列表类型不行啊, 没有办法实现群发
## 好像qq邮箱屏蔽了, 不过还可以发给gmail
receivers = '2253238252@qq.com'

message = MIMEText('Python 邮件测试, 求通过...')
message['Subject'] = 'python 邮件测试';
message['From'] = sender
message['To'] = receivers

try:
    smtpObj = smtplib.SMTP()
    smtpObj.set_debuglevel(True)
    ## 注意, 通过本地发送邮件时, 要求本地存在邮件服务器(一般时postfix)
    ## postfix的默认端口为25, 大多发行版已经自带
    smtpObj.connect('localhost')
    smtpObj.sendmail(sender, receivers, message.as_string())
    print '邮件发送成功'
except smtplib.SMTPException:
    print 'Error: 邮件发送失败'
