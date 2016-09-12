#!/usr/bin/python
#!coding:utf-8

## 需要导入smtplib与email两个包
import smtplib
from email.mime.text import MIMEText

## 第三方SMTP服务, 以QQ邮箱为例
## QQ邮箱的SMTP服务需要进行授权登陆,
## 用户名为QQ邮箱地址而不是QQ号
## 其授权码作为密码
## 就算设置了邮箱的独立密码也一样
mailHost = 'smtp.qq.com'
mailPort = 587
mailUser = '2253238252@qq.com'
mailPasswd = 'hegirytnnbkfdihj'

## 发件人
sender = mailUser
## 收件人
receivers = '2568377304@qq.com'

## 邮件内容.
## 经测试, 邮件主题(Subject)与发件人(From)都不是必须的(不过这三者时标准邮件信息).
## 另外, message的From成员可以伪装成其他邮箱
## 但这样的收件人依然可以看到这是由真实发件人"代发"的.
message = MIMEText('Python 邮件测试, 求通过...')
message['Subject'] = 'python 邮件测试'
message['From'] = sender
message['To'] = receivers

try:
    smtpObj = smtplib.SMTP()
    smtpObj.set_debuglevel(True)
    smtpObj.connect(mailHost, mailPort)
    ## 可能私人邮箱不需要使用TLS验证,
    ## 不过QQ邮箱会提示'Must issue a STARTTLS command first.'
    ## 注意starttls()的位置, 一定要是login()的前一句
    smtpObj.starttls()
    smtpObj.login(mailUser, mailPasswd)
    smtpObj.sendmail(sender, receivers, message.as_string())
    ## smtp连接一段时间后会自动断开, 不过还是手动断可靠一点
    smtpObj.close()
    print 'Success: 邮件发送成功'
except smtplib.SMTPException:
    print 'Error: 发送失败'
