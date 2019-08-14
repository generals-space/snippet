#!/bin/bash

## 当前脚本名称(不是lib.sh本身哦, 是调用主调脚本的文件名)
__file__=$0
## 主调脚本所在路径
__dir__=$(cd $(dirname $0) && pwd)
## 当前用户名
__user__=$(whoami)

## __strlen: 计算指定字符串的长度
##__strlen() {}

__get_formatted_date() {
    date +"%Y/%m/%d %H:%M:%S"
}
__strlen() {
    local str=$1
    ## 1. wc 的-L选项, 直接获取当前行的字符数
    echo $1 | wc -L
    ## 2. ${}方法, 把字符串变量当作是数组处理
    ## echo ${#str}
    ## 3. awk内置的length()函数
    ## echo $a | awk '{print length($0)}'
    ## 4. expr内置lenght无法处理变量中存在空格的情形, 放弃使用
}

## 经过格式化的当前时间, 使用$__now__即可得到
## 被注释掉的这一行, $__now__得到的是带有引号的字符串, 感觉不太友好.
## 更换成使用函数生成的字符串
## __now__='date +"%Y/%m/%d-%H:%M:%S"'
## __now__是函数, 是函数, 是函数
__now__=__get_formatted_date
