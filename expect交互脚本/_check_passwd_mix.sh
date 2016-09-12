#!/bin/bash

## 验证是否已经对目标主机拥有key或是密码权限

## 加载verifyIdentity函数库, 类似于C中的include, php中的require
## 注意不能使用bash, 只能用source命令
source ./verifyIdentity.sh

## 变量定义
## IP/密码对应文件
filename=serverInfo
User=root

## 按行读取文件, -r 表示不转义行中反斜线字符, 这很重要!!!
while read -r line
do
    ## echo $line
    IP=$(echo $line | awk '{print $1}')
    Passwd=$(echo $line | awk '{print $2}')
    ## 转义密码中的特殊字符
    Passwd=$(escape_for_expect $Passwd)
    ## 调用verifyIdentity函数, 需要三个参数
    verify_identity $User $IP $Passwd
    ## sleep 3
done < $filename
