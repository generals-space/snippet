#!/usr/bin/expect

## author: general
## email: generals.space@gmail.com
## date: 2016-08-04
## function
## 将指定公钥导入目标主机组中
## 适用于拥有主机组中各主机的帐号密码, 希望实现便捷登陆
## 或是由拥有登陆权限的用户为他人拷贝.

## param1: 目标主机IP
## param2: 目标主机密码
## param3: 待导入公钥
## 将输出日志到当前目录, 日志文件名verify.log
## 使用要求: 系统中已安装expect命令, 否则无法调用
## 注意: 如果当前用户用户目标主机的无密码登陆权限, param2也可以为空.

## expect内置命令解释
#### log_file 指定日志输出文件名, 不过标准输出依然会有结果打印出来, 无法屏蔽
#### spawn expect本身创建进程, 调用ssh命令
#### send_user 标准输出打印信息
#### send_log 输出到日志文件, 不会在标准输出出现
#### exp_continue 再次使用本块expect代码执行一次匹配
#### close 关闭ssh连接(未完成登陆也可以)

set IP        [lindex $argv 0]
set PASSWD    [lindex $argv 1]
set KEYFILE   [lindex $argv 2]

set timeout 10
set result 0
## expect脚本中定义字符串变量不用加引号...
## 不过这样貌似会很有很多限制
set USER root
## 日志文件
log_file import.log

spawn ssh-copy-id -i $KEYFILE $USER@$IP

## 首次连接需要接受对方公钥, 添加到已知主机
expect "(yes/no)?" {
    set result 1
    send_user "\n第1次登录需要接受主机验证. 接受...\n"
    send_log "\n第1次登录需要接受主机验证. 接受...\n"

    send "yes"
    send "\n"
}
#### 如果有无密码登陆权限, 则不会再出现以下的情况
## 没有key, 输入密码.
expect "password:" {
    set result 2

    send_user "\n主机验证通过, 输入密码...\n"
    send_log "\n主机验证通过, 输入密码...\n"

    send -- "$PASSWD"
    send "\n"
}

## 如果还出现这个提示, 说明密码不正确.
expect "password:" {
    set result 3
    send_user "\n密码错误 $IP\n"
    send_log "\ncode3 $IP $PASSWD\n"

    close
}

## 导入结果分析
if {$result == 0} {
    send_user "导入失败, 可能是因为超时, 未启动22端口或是目标宕机 $IP \n"
    send_log "\ncode4 $IP $PASSWD\n"
} elseif {$result == 1} {
    send_user "导入成功, 使用key登陆方式 $IP \n"
    send_log "\ncode1 $IP $PASSWD\n"
} elseif {$result == 2} {
    send_user "导入成功, 使用密码登陆 $IP \n"
    send_log "\ncode2 $IP $PASSWD\n"
} elseif {$result == 3} {
    send_user "导入失败, 使用密码登陆, 但密码错误 $IP \n"
    send_log "\ncode3 $IP $PASSWD\n"
}
