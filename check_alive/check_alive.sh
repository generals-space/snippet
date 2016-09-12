#!/bin/bash

## 批量检测主机存活状态
## 参数: 待检测目标IP列表文件名

filename=serverList

####...$1要用双引号括起来, 不然bash会将"1"看作变量名
if [ -n "$1" ]; 
then
    filename=$1
fi

## ping命令的尝试次数, 在此次数内无响应则判断目标为offline
attemp_times=2
log_file=alive.log

## 按行读取文件, -r 表示不转义行中反斜线字符, 这很重要!!!
while read -r line
do    
    ping -c $attemp_times $line &> /dev/null
    if [ $? -eq 0 ];
    then
        echo $line is alive
	echo "alive: $line" >> $log_file
    else
        echo $line is offline
	echo "offline: $line" >> $log_file
    fi
done < $filename

