#!/usr/bin/expect

## 验证是否已经对目标主机拥有key或是密码权限

## author: general
## email: generals.space@gmail.com
## date: 2016-08-04

## param: 用户名, 一般是root
## param: 目标主机IP
## param: 待检测密码
## 将输出日志到当前目录, 日志文件名verify.log
## 使用要求: 系统中已安装expect命令, 否则无法调用

## expect内置命令解释
#### log_file 指定日志输出文件名, 不过标准输出依然会有结果打印出来, 无法屏蔽
#### spawn expect本身创建进程, 调用ssh命令
#### puts 标准输出打印信息
#### send_log 输出到日志文件, 不会在标准输出出现
#### exp_continue 再次使用本块expect代码执行一次匹配
#### close 关闭ssh连接(未完成登陆也可以)

## verify_identity()日志输出有三种结果:
## 1. 有key, 正常登陆
## 2. 密码正确, 正常登陆
## 3. 无key, 密码错误

## 但大致还有三种错误类型
## 4. 连接超时
####  无法建立连接, 可能是网络原因或是主机未启动.
####  ssh: connect to host 192.168.165.83 port 22: Connection timed out
## 5. ssh: 主机启动, 但没有开放22端口或是被防火墙屏蔽.
####  spawn ssh root@192.168.1.19
####  ssh: connect to host 192.168.1.19 port 22: No route to host
####  expect: spawn id exp7 not open
####      while executing expect {}

set USER      [lindex $argv 0]
set IP        [lindex $argv 1]
set PASSWD    [lindex $argv 2]

set timeout 10
set status_code 0
## 日志文件
log_file verify.log

spawn ssh $USER@$IP

## 首次连接需要接受对方公钥, 添加到已知主机
expect {
    "(yes/no)?" {
    	puts "\n第1次登录需要接受主机验证. 接受...\n"
        send_log "\n第1次登录需要接受主机验证. 接受...\n"

        send "yes"
        send "\n"
    }
    ## 这里的超时暂时注释掉, 可能与末尾的超时处理有重复的地方, 待检测
    ## "Connection timed out" {
    ##     set status_code 4
    ##     send_log "\ncode4 $IP $PASSWD\n"
    ##     puts "连接超时, 请检查网络 $IP \n"
    ## }
    "No route to host" {
        set status_code 5
        send_log "\ncode5 $IP $PASSWD\n"
        puts "未启动22端口或是被防火墙拦截 $IP \n"
        exit
    }
}

expect {
    ## 若拥有目标主机的key, 则不会提示输入密码而直接登陆
    "#" {
        set status_code 1

        send "exit"
        send "\n"
        puts "\n拥有key, 未验证密码 $IP\n"
        send_log "\ncode1 $IP $PASSWD\n"
    }
    ## 没有key, 输入密码.
    "password:" {
        set status_code 1

        puts "\n主机验证通过, 输入密码...\n"
        send_log "\n主机验证通过, 输入密码...\n"

        send -- "$PASSWD"
        send "\n"
    }
}

expect {
    ## 执行到这里, 说明密码输入正确
    "#" {
        set status_code 2
        send "exit"
        send "\n"
        puts "\n密码正确 $IP\n"
        send_log "\ncode2 $IP $PASSWD\n"
    }
    ## 如果还出现这个提示, 说明密码不正确.
    "password:" {
        set status_code 3
        puts "\n密码错误 $IP\n"
        send_log "\ncode3 $IP $PASSWD\n"

        close
    }
}

if {$status_code == 0} {
    set status_code 4
    puts "超时, 可能是网络原因或是目标宕机 $IP \n"
    send_log "\ncode4 $IP $PASSWD\n"
}

