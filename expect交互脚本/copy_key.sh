#!/bin/bash

## 调用import_pub_key.sh脚本, 批量导入公钥到目标主机

## 变量定义
## IP/密码对应列表文件
filename=serverList
## 待导入公钥
KeyFile=id_rsa.pub

## 有时如果当前目录不同时存在id_rsa与id_rsa.pub,
## ssh-copy-id会执行出错, 此时需要手动创建(空文件也行)
if [ ! -e './id_rsa' ]; then touch id_rsa; fi

## 按行读取文件, -r 表示不转义行中反斜线字符, 这很重要!!!
while read -r line
do
    ## echo $line
    IP=$(echo $line | awk '{print $1}')
    Passwd=$(echo $line | awk '{print $2}')
    if [ -z $Passwd ]; then Passwd='\n'; fi

    ./import_pub_key.sh $IP $Passwd $KeyFile
done < $filename

## 清理上面创建的id_rsa文件
rm -f ./id_rsa
