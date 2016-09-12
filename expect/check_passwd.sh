#!/bin/bash

## 验证是否已经对目标主机拥有key或是密码权限

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
    ## 分离式expect脚本不需要转义特殊字符, $也是
    ## 调用verifyIdentity脚本, 需要三个参数
    ./verify_identity.sh $User $IP $Passwd
done < $filename
