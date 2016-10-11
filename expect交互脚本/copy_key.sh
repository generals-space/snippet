#!/bin/bash

## 调用import_pub_key.sh脚本, 批量导入公钥到目标主机

## 变量定义
## IP/密码对应列表文件名
ip_list=ip_list
## 待导入公钥名称
key_file=id_rsa.pub
## 每当ssh成功登录一台主机, 就会执行`cat ~/.ssh/authorized_keys`命令,
## 并将登录过程及命令执行结果记录在此文件中
tmp_record=/tmp/expect_command_record
login_log=expect_ssh.log
import_log=expect_import.log
## 有时如果当前目录不同时存在id_rsa与id_rsa.pub, ssh-copy-id会执行出错, 
## 此时需要手动创建(空文件也行)
if [ ! -e './id_rsa' ]; then touch id_rsa; fi


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

import_record() {
    if [ $1 == 1 ]; then
            echo "行$line_num: $IP 目标主机上已存在此公钥, 不再重复导入"
            echo "status1 $IP $PASSWD" >> $import_log
    elif [ $1 == 2 ]; then
            echo "行$line_num: $IP 导入成功"
            echo "status2 $IP $PASSWD" >> $import_log
    elif [ $1 == 3 ]; then 
            echo "行$line_num: $IP 您无权登录此主机, 请检查主机22端口是否开放, 密码是否正确"
            echo "status3 $IP $PASSWD" >> $
    elif [ $1 == 4 ]; then 
            echo "行$line_num: $IP 未知错误, 请重试, "
            echo "status4 $IP $PASSWD" >> $import_log
    fi
}

## 按行读取文件, 放弃使用while read方式
line_sum=$(cat $ip_list | wc -l)
## echo $line_sum
for ((line_num = 1; line_num <= $line_sum; line_num ++))
do
    line=$(sed -n "${line_num}p" $ip_list)
    IP=$(echo $line | awk '{print $1}')
    PASSWD=$(echo $line | awk '{print $2}')

    ## 首先执行ssh脚本查看目标主机上是否已经拥有待导入的公钥
    ./expect_ssh.sh $USER $IP $PASSWD > $tmp_record
    status_code=$?
    login_record $status_code

    ## 如果$tmp_record文件中有待导入的公钥文件, 说明目标服务器上存在了这个key, 不再重复导入
    if [ $(grep "$(cat $key_file)" $tmp_record | wc -l) -ge 1 ]; then
        import_code=1
    ## 如果没有, 还要保证我们拥有目标的ssh登录权限, $status_code的值为1,2表示能够通过key或密码进行登录
    elif (( $status_code == 1 || $status_code == 2 )); then
        ## 如果没有密码(密码为空), 则设置$Passwd变量为'\n', 因为import_pub_key.sh脚本需要这个参数
        if [ -z $Passwd ]; then Passwd='\n'; fi
        ./expect_ssh_copy_id.sh $IP $Passwd $key_file
        status_code=$?
        if (( $status_code == 1 || $status_code == 2 )); then
            import_code=2      
        else
            import_code=4
        fi
    else
        import_code=3        
    fi
    import_record $import_code
done

## 清理上面创建的id_rsa文件
rm -f ./id_rsa
## 清理登录过程记录文件
rm -f $tmp_record