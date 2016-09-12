#!/usr/bin/python
#!coding:utf-8
import re

var_key = []    ##nginx变量名列表(不含任何多余字符)
var_val = []    ##nginx变量值列表(从日志文件中提取)
var_reg = []    ##为截取str_splited每个元素中的有效变量值所构造的正则字符串
                ##所以其元素个数与str_splited元素个数相同
var_sum = []    ##var_reg中对应的每个元素包含的nginx变量个数

##功能: 转义str_to_normalzie字符串中所有用于正则表达式的字符
##返回: 转义后的字符串
def normalize_reg(str_to_normalize):
    ##chars_reg是可能出现在正则表达式中的字符, 如果str_to_normalize包含它们,
    ##需要对其进行转义
    chars_reg = ['.', '"', '$', '^', '+', '-', '*', '/', '\\', '[', ']']
    str_normalized = ''
    for char in str_to_normalize:
        if char in chars_reg:
            str_normalized += ('\\' + char)
        else:
            str_normalized += char
    return str_normalized

##function: 处理给定的日志格式, 得到配置文件中的变量名列表,
##          根据这个列表可以在读取日志文件时得到这些变量对应的值
##函数流程: 首先将原始的日志变量字符串str_ori按照空格分隔, 得到一个列表str_splited
##          然后分别对str_splited中的每个元素使用正则截取nginx内置变量名(以$为准)
##          (注意每个元素不一定只包含1个变量, 因为它们之间可能使用'-'连接)
##          截取的同时构造对应的正则字符串, 以应用于真正的日志数据文件
##          将得到的nginx变量名组成一个列表var_key, 生成的正则串组成列表var_reg,
##          var_sum中是var_reg里对应的每个正则串可以截取的nginx变量个数.
##          例如'"$request_time"s-[$time_local]'不会以空格分隔开, 但它包含两个变量.
##          它对应的正则串为'\"(\$[a-zA-Z_]+)\"s\-\[(\$[a-zA-Z_]+)\]', var_num存的是2.
##          从日志文件中读取数据时需要根据var_sum从中取得两个分组的值才不会遗漏
def fmt_format(str_ori):
    ##将原始配置字符串按空格分隔, 得到列表
    str_splited = str_ori.split()
    ##i是elem在str_splited中的索引值
    i = 0
    for elem in str_splited:
        ##print 'current elem: ' + elem
        str_reg_tmp = ''
        var_sum_tmp = 0
        while True:
            ##判断是否存在nginx变量
            if re.search('\$[a-zA-Z_]+', elem):
                var_sum_tmp += 1
                ##为了确保第1个分组中不含有nginx变量, 它的值不能是(.*)
                result = re.search('([^\$]*)(\$[a-zA-Z_]+)(.*)', elem)
                grp1, grp2, grp3 = result.group(1), result.group(2), result.group(3)
                ##找出这个nginx变量, 添加到var_key列表中, 并且构造正则字符串
                ##print 'grp2: ' + grp2
                var_key.append(grp2)
                str_reg_tmp += (normalize_reg(grp1) + '(\$[a-zA-Z_]+)')
                ##如果grp3中还有另外的nginx变量, 循环取出直到完毕
                if re.search('\$[a-zA-Z_]+', grp3):
                    elem = grp3
                    continue
                else:
                    str_reg_tmp += normalize_reg(grp3)
                    break
            ##如果不存在就break, 进行下一个元素的匹配
            else:
                break
        var_reg.append(str_reg_tmp)
        var_sum.append(var_sum_tmp)

str_ori = '$http_x_forwarded_for - "$request_time"s-[$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent" "$remote_addr"'

fmt_format(str_ori)

for elem in var_reg:
    print elem