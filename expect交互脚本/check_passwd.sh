#!/bin/bash

## 验证是否已经对目标主机拥有key或是密码权限

## 变量定义
## IP/密码列表文件
ip_list=ip_list
## 日志文件
login_log=expect_ssh.log
## expect脚本返回状态码
status_code=
USER=root


## ssh登录结果记录
#### 函数中IP与PASSWD, line_num变量为全局变量
login_record() {
    if [ $1 == 1 ]; then
            echo "行$line_num: $IP 拥有key, 未验证密码"
            echo "status1 $IP $PASSWD" >> $login_log
    elif [ $1 == 2 ]; then
            echo "行$line_num: $IP 密码正确"
            echo "status2 $IP $PASSWD" >> $login_log
    elif [ $1 == 3 ]; then 
            echo "行$line_num: $IP 密码错误"
            echo "status3 $IP $PASSWD" >> $login_log
    elif [ $1 == 4 ]; then
            echo "行$line_num: $IP 超时, 可能是网络原因或是目标宕机"
            echo "status4 $IP $PASSWD" >> $login_log
    elif [ $1 == 5 ]; then
            echo "行$line_num: $IP 未启动22端口或是被防火墙拦截"
            echo "status5 $IP $PASSWD" >> $login_log
    fi
}

## 按行读取文件, 放弃使用while read方式
line_sum=$(cat $ip_list | wc -l)
for ((line_num = 1; line_num <= $line_sum; line_num ++))
do
        line=$(sed -n "${line_num}p" $ip_list)
        IP=$(echo $line | awk '{print $1}')
        PASSWD=$(echo $line | awk '{print $2}')
        ## 调用expect脚本, 需要三个参数
        ## 如果没有密码(或密码为空), 则设置$Passwd变量为'\n'
        if [ -z $Passwd ]; then Passwd='\n'; fi
        ./expect_ssh.sh $USER $IP $PASSWD
        status_code=$?
        ## echo $status_code
        ## 日志输出, 重定向操作不影响expect脚本的返回状态码
        login_record $status_code
done