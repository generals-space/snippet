#!/bin/bash

## 当前脚本名称(不是lib.sh本身哦, 是调用主调脚本的文件名)
__file__=$0
## 主调脚本所在路径
__dir__=$(cd $(dirname $0) && pwd)
## 当前用户名
__user__=$(whoami)
