#!/bin/bash

## author: general
## email: generals.space@gmail.com
## date: 2016-08-04


## 检测目标用户对目标主机拥有key, 及拥有的密码是否正确
## 应用expect混合脚本, 可用场景有限

## param: 用户名, 一般是root
## param: 目标主机IP
## param: 待检测密码
## 将输出日志到当前目录, 日志文件名verify.log
## 使用要求: 系统中已安装expect命令, 否则无法调用
## bug: 无法检测超时IP, 日志结果中不能明确表示出这样的情况
function verify_identity ()
{
    ## expect内置命令解释
    #### log_file 指定日志输出文件名, 不过标准输出依然会有结果打印出来, 无法屏蔽
    #### spawn expect本身创建进程, 调用ssh命令
    #### send_user 标准输出打印信息
    #### send_log 输出到日志文件, 不会在标准输出出现
    #### exp_continue 再次使用本块expect代码执行一次匹配
    #### close 关闭ssh连接(未完成登陆也可以)

    ## expect命令的绝对路径
    ##EXPECT=/usr/bin/expect
    USER=$1
    IP=$2
    PASSWD=$3

    expect <<-EOF

        set timeout 10
        log_file verify.log
        spawn ssh $USER@$IP

        expect {
            "(yes/no)?" {

                send_user "\n第1次登录需要接受主机验证. 接受...\n"
                send_log "\n第1次登录需要接受主机验证. 接受...\n"

                send "yes"
                send "\n"

                exp_continue
            }
            "password:" {

                send_user "\n主机验证通过, 输入密码...\n"
                send_log "\n主机验证通过, 输入密码...\n"

                send -- "$PASSWD"
                send "\n"
            }
        }

        expect {
            "#" {

                send "exit"
                send "\n"
                send_user "\n密码正确 $IP\n"
                send_log "\ncode2 $IP $PASSWD\n"
            }
            "password:" {

                send_user "\n密码错误 $IP\n"
                send_log "\ncode3 $IP $PASSWD\n"

                close
            }
        }

## 无论什么时候, EOF结束标志都应该在行首
EOF
}

## 为verify_identity转义特殊字符
## 尤其是密码字符串, 特殊字符可以提高密码强度
function escape_for_expect ()
{
    result=$1
    ## 首先替换 \ 反斜线字符, 包括\r \n \t \v 等
    result=$(echo $result | sed 's/\\/\\\\/g')
    ## 替换 $ 美元符号
    result=$(echo $result | sed 's/\$/\\$/g')
    ## 替换 " 双引号
    result=$(echo $result | sed 's/\"/\\"/g')
    ## 替换 ; 分号
    result=$(echo $result | sed 's/;/\\;/g')
    ## 替换 % 百分号
    result=$(echo $result | sed 's/%/\\%/g')
    ## 替换 # 井号
    result=$(echo $result | sed 's/#/\\#/g')
    ## 替换 ( 左括号
    result=$(echo $result | sed 's/(/\\(/g')
    ## 替换 ) 右括号
    result=$(echo $result | sed 's/)/\\)/g')
    ## 替换 [ 左中括号
    result=$(echo $result | sed 's/\[/\\[/g')
    ## 替换 ] 右中括号
    result=$(echo $result | sed 's/\]/\\]/g')
    ## 替换 { 左大括号
    result=$(echo $result | sed 's/{/\\{/g')
    ## 替换 } 右大括号
    result=$(echo $result | sed 's/}/\\}/g')
    ## 替换 ` 反引号...可能需要替换
    ## result=$(echo $result | sed 's/`/\\`/g')

    ## 返回值只能使用这种方式, 被调函数的所有标准输出都将作为"返回值"
    ## return命令只能返回数值, 作为退出码
    echo $result
}


## verify_identity()日志输出有三种结果:
## 1. 有key, 正常登陆
## 2. 密码正确, 正常登陆
## 3. 无key, 密码错误
## 4. 无法建立连接, 可能是主机未启动. 没有明确指定的code码, 需要自行到日志文件中查找特定字符串
## 5. ssh: 主机启动但被防火墙屏蔽.
####  spawn ssh root@192.168.1.19
####  ssh: connect to host 192.168.1.19 port 22: No route to host
####  expect: spawn id exp7 not open
####      while executing expect {}
function analysis_log_for_expect ()
{
    ## 未完成
    true
}
