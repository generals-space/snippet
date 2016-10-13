#!/usr/bin/python
#coding:utf-8
##  function                    @转换securtCRT的session文件为xshell的session文件
##  命令行中main函数需要三个参数
##  1. securecrt_session        @securtCRT配置目录下的session目录
##  2. xshell_xsh_tpl_file      @一个xshell的模版文件(从XShell配置目录拷贝出一个的session文件)
##                              建议: 如果有特殊要求(如有登录脚本), 需要在此模板文件也要有相应配置
##  3. xshell_output_dir        @输出目录(必须不存在, 程序会自动创建)
##
##  原地址: www.cnblogs.com/moodlxs/p/3403828.html
##  说明: 1. 该程序对配置文件的转换是以文件名, 也就是配置文件中的session名称为准的,
##        所以secureCRT的session名称中需要有完整IP出现, 程序会根据正则表达式提取IP;
##        2. 该程序本质上是对XShell模板文件中的IP替换, 所以如果secureCRT配置中有登录脚本, 
##           则XShell模板文件中也要有类似配置
##        3. 第2行不能删除, 配置了python源文件的编码格式
##        4. python2.7中使用通过
##        5. 登录用户名不会变
import os
import re           ##正则模块
from sys import *

def gen_xshell_session(path, tpl_file, output):
    ## 创建输入目录
    if os.path.exists(output):
        print '抱歉, 指定的目录已存在, 请指定其他路径并重试'
        return 1
    os.mkdir(output)

    ## 用于模板文件中的IP替换
    tpl = os.path.basename(tpl_file)    ## 直接取得不带路径的文件名
    tpl_n = tpl.find('.xsh')
    tpl_ip = tpl[0:tpl_n]

    for f in os.listdir(path):
        ## print(f)
        fn = path + '/' + f
        ## 递归调用以处理子目录
        if  os.path.isdir(fn):
            od = output + '/' + f
            gen_xshell_session(fn, tpl_file, od)
        else:
            ## 处理secureCRT的有效配置文件
            ## 如果以'__'开头, 说明这是一个形容目录的配置, XShell不需要
            ## 如果是Default.ini, 呃.....XShell也不需要
            if f.startswith('__') or f == 'Default.ini':
                continue
            ## ext, 是配置文件扩展名的"索引"(第一次出现的位置)
            ext = f.find('.ini')
            ## ip是不带扩展名的文件名, 作为目标IP
            ## 注意: 这里有一些不足, 因为有时候为了方便识别, 文件名称不般不会是单纯的IP
            filename = f[0:ext]       ##这里用了分片索引(可把f文件名看作字符串/数组)
            ## 根据情况可能需要调整正则模式
            ip_obj = re.search('\d{3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', filename)
            ip = ip_obj.group()

            ifn = open(tpl_file, 'r')
            lns = ifn.readlines()   ##按行读取所有内容
            ifn.close()

            ## 创建同名的XShell配置文件
            xshell_cfg_file = output + '/' + filename + '.xsh'
            ofn = open(xshell_cfg_file, 'w')
            for ln in lns:
                ## 逐行替换目标IP
                ln = ln.replace(tpl_ip, ip)
                ofn.write(ln)
            ofn.close()

##  入口函数
if __name__ == '__main__':
    securecrt_session           = argv[1]
    xshell_xsh_tpl_file         = argv[2]
    xshell_output_dir           = argv[3]

    gen_xshell_session(securecrt_session, xshell_xsh_tpl_file, xshell_output_dir)