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

## 获取命令行参数变量
set IP        [lindex $argv 0]
set PASSWD    [lindex $argv 1]
set KEYFILE   [lindex $argv 2]

set timeout 10
set result 0
set USER root
## 日志文件
## log_file expect_ssh_copy_id.log

spawn ssh-copy-id -i $KEYFILE $USER@$IP

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
    exit 1
} elseif {$status_code == 2} {
    exit 2
} elseif {$status_code == 3} {
    exit 3
} elseif {$status_code == 4} {
    exit 4
} elseif {$status_code == 5} {
    exit 5
}