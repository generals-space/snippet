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


## verify_identity()日志输出有三种结果:
## 1. 有key, 正常登陆
## 2. 密码正确, 正常登陆
## 3. 无key, 密码错误

## 但大致还有两种种错误类型
## 4. 连接超时
####  无法建立连接, 可能是网络原因或是主机未启动.
####  ssh: connect to host 192.168.165.83 port 22: Connection timed out
## 5. ssh: 主机启动, 但没有开放22端口或是被防火墙屏蔽.
####  spawn ssh root@192.168.1.19
####  ssh: connect to host 192.168.1.19 port 22: No route to host
####  expect: spawn id exp7 not open
####      while executing expect {}

## 获取命令行参数变量
#### COMMAND: ssh成功登录目标主机后需要执行的操作
set USER      [lindex $argv 0]
set IP        [lindex $argv 1]
set PASSWD    [lindex $argv 2]

## 如果命令变量是从主调脚本中传入的话, 就不可以包含空格, 否则会被认为是几个独立的参数
## 只能使用这种方式定义要执行的命令, exec命令类似于shell中的`命令`或是$(命令), 可以设置包含空格的变量
set COMMAND  [exec echo cat ~/.ssh/authorized_keys]

set timeout 30
## 登录行为的初始状态码为0, 用以判断ssh登录的结果
set status_code 0                  
## 日志文件, 可选
## log_file expect_ssh.log

spawn ssh $USER@$IP

##################################################################
#### 通用部分

## 首次连接需要接受对方公钥, 添加到已知主机
expect {
    ## 有这个提示说明一定能够到达目标主机的22端口
    "(yes/no)?" {
    	puts "\n第1次登录需要接受主机验证. 接受...\n"
        send "yes\n"
    }
    ## 这里的超时判断暂时注释掉, 可能与末尾的超时处理有重复的地方, 待检测
    ## "Connection timed out" {
    ##     set status_code 4
    ##     send_log "\ncode4 $IP $PASSWD\n"
    ##     puts "连接超时, 请检查网络 $IP \n"
    ## }

    "No route to host" {
        set status_code 5
    }
    "Connection refused" {
        set status_code 5
    }
}

expect {
    ## 若拥有目标主机的key, 则不会提示输入密码而直接登陆
    "#" {
        set status_code 1
        ## custom_command_start/end是一个标志, 方便主调脚本单纯抓取命令执行结果而屏蔽掉ssh的具体行为
        send "echo custom_command_start\n"    
        send "$COMMAND\n"
        send "echo custom_command_end\n"                
        send "exit\n"
        ## 不太理解为什么需要加上interact指令才能完成登录后的输入操作
        ## 但是如果不加登录后就不会再执行send指令
        ## interact
    }
    ## 没有key, 输入密码.
    "password:" {
        set status_code 1
        puts "\n主机验证通过, 输入密码...\n"
        send -- "$PASSWD\n"
    }
}

expect {
    ## 能够执行到这里, 说明密码输入正确
    ## '#'说明是以root身份登录, '$'说明是以普通用户身份登录
    "#" {
        set status_code 2
        ## custom_command_start/end是一个标志, 方便主调脚本单纯抓取命令执行结果而屏蔽掉ssh的具体行为
        send "echo custom_command_start\n"    
        send "$COMMAND\n"
        send "echo custom_command_end\n"                
        send "exit\n"
        ## 不太理解为什么需要加上interact指令才能完成登录后的输入操作
        ## 但是如果不加登录后就不会再执行send指令
        interact
    }
    ## 如果还出现这个提示, 说明密码不正确.
    "password:" {
        set status_code 3
    }
}

if {$status_code == 0} {
    set status_code 4
}

###############################################################
## 检测结果分析
if {$status_code == 1} {
        ## puts "\n拥有key, 未验证密码 $IP\n"
        ## send_log "\ncode1 $IP $PASSWD\n"
        exit 1
} elseif {$status_code == 2} {
        ## puts "\n密码正确 $IP\n"
        ## send_log "\ncode2 $IP $PASSWD\n"
        exit 2
} elseif {$status_code == 3} {
        ## puts "\n密码错误 $IP\n"
        ## send_log "\ncode3 $IP $PASSWD\n"
        exit 3
} elseif {$status_code == 4} {
        ## puts "超时, 可能是网络原因或是目标宕机 $IP \n"
        ## send_log "\ncode4 $IP $PASSWD\n"
        exit 4
} elseif {$status_code == 5} {
        ## puts "未启动22端口或是被防火墙拦截 $IP \n"
        ## send_log "\ncode5 $IP $PASSWD\n"
        exit 5
}
