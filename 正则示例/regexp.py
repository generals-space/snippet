#!/usr/bin/python
#!coding:utf-8
## function@python中正则表达式的初始使用方法
## by@general, 2015-12-18
import re

str = 'host_192.168.1.1'
#######################################################################
## re模块主要有两个函数, match()与search()
## 它们两个作用和用法完全一样, 唯一一点区别是,
## match()只能匹配目标字符串的开始位置, 
## 如果指定模式不是出现在目标字符串的开头时就返回none
ip1 = re.match('host', str)
print ip1
ip2 = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', str)
print ip2
ip3 = re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', str)
print ip3

#######################################################################
## 注意:它们两个返回的是查找到的(字符串)"对象", 所以打印出的是"对象信息"
## 有一个span()函数, 可以返回正则对象的元组表示, 
## 代表指定模式的对象在目标字符串出现的"位置"
ip1 = re.match('host', str).span()
print ip1
ip2 = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', str).span()
print ip2
## 小心! 如果没有匹配到, 使用span()会出错退出!
#ip3 = re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', str).span()
#print ip3

#######################################################################
## 分组的使用
## 注意: 只有python对象可以调用分组函数group(), 
## 所以使用分组的话就不能返回元组, 即不能使用span()函数
ip1 = re.match('(host)', str)
#print ip1
print 'ip1.group(): ' + ip1.group()
print 'ip1.group(1): ' + ip1.group(1)
ip2 = re.search('(.*)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', str)
#print ip2
print 'ip2.group(): ' + ip2.group()
print 'ip2.group(2): ' + ip2.group(2)
