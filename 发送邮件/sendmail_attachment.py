#!/usr/bin/python
#coding: utf-8

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

mailHost = 'smtp.qq.com'
mailPort = 587
mailUser = '2253238252@qq.com'
mailPasswd = 'hegirytnnbkfdihj'

## 发件人
sender = mailUser
## 收件人
receivers = '2568377304@qq.com'

message = MIMEMultipart()
message['From'] = sender
message['To'] = receivers
message['Subject'] = 'python邮件主题'

## 邮件正文内容
content = MIMEText('邮件正文内容')
message.attach(content)

## 构造附件
attachment = MIMEText(open('/tmp/test.txt').read(), 'base64', 'utf-8')
attachment['Content-Type'] = 'application/octet-stream'
#### filename的值可以随意填写, 其名称为出现在邮件中的附件名
attachment['Content-Disposition'] = 'attachment; filename="附件test.txt"'
message.attach(attachment)

try:
    smtpObj = smtplib.SMTP()
    smtpObj.set_debuglevel(True)
    smtpObj.connect(mailHost, mailPort)
    smtpObj.starttls()
    smtpObj.login(mailUser, mailPasswd)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print 'Success: 邮件发送成功'
except smtplib.SMTPException:
    print 'Error: 邮件发送失败'
