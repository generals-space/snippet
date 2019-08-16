#!/bin/bash

## 当前脚本名称(不是lib.sh本身哦, 是调用主调脚本的文件名)
__file__=$0
## 主调脚本所在路径
__dir__=$(cd $(dirname $0) && pwd)
## 当前用户名
__user__=$(whoami)

__get_formatted_date() {
    date +"%Y/%m/%d %H:%M:%S"
}

## 经过格式化的当前时间, 使用$__now__即可得到
## 被注释掉的这一行, $__now__得到的是带有引号的字符串, 感觉不太友好.
## 更换成使用函数生成的字符串
## __now__='date +"%Y/%m/%d-%H:%M:%S"'
## __now__是函数, 是函数, 是函数
__now__=__get_formatted_date
