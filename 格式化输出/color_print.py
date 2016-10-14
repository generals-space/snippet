#!/usr/bin/python
# coding: utf-8

## 仅在linux下有效, 没有使用其他python库, 比较精简


def color_print(msg, color):
    """
    color_print: 打印彩色字符.
    msg: 要打印的字符串
    color: 要使用的颜色(), 默认为red
    """
    ## color_msg字典的键值有两个'\33['标志, 这样在打印了'%s'代表的字符串后会将终端显示模式立刻改回默认的设置
    ## 这里单纯设置了显示模式与前景色, 背景色变量没有写, 默认不改变
    color_msg = {
        'blue':     '\033[1;36m%s\033[0m',
        'green':    '\033[1;32m%s\033[0m',
        'yellow':   '\033[1;33m%s\033[0m',
        'red':      '\033[1;31m%s\033[0m',
    }
    ## 字典类型的get()方法, 可以指定1到2个参数, 如果第1个参数为空值, 则取出第2个参数对应的键值.
    ## 将msg这个变量嵌入到两个'\033['标记内, 相当于输出彩色字符后立刻恢复默认设置
    msg = color_msg.get(color, 'red') % msg
    print(msg)


if __name__ == '__main__':

    ## 颜色格式: '\033[显示方式;前景色;背景色m'
    ## 显示方式取值: {0:终端默认设置;1:高亮显示;4:使用下划线;5:闪烁;7:反白显示;8:不可见}.
    ## 前景色取值: {30: 黑色(black); 31: 红色(red); 32: 绿色(green); 33: 黄色(yellow); 34: 蓝色(blue); 35: 紫红(purple); 36: 青色(cyan); 37: 白色(white)}
    ## 背景色取值: {40: 黑色(black); 41: 红色(red); 42: 绿色(green); 43: 黄色(yellow); 44: 蓝色(blue); 45: 紫红(purple); 46: 青色(cyan); 47: 白色(white)}

    ## 直接使用print 色彩设置, 会影响当前终端的颜色属性, 使得之后的输出都会以这种模式展示
    print '\033[5;m'
    print '单纯设置显示模式...应该是不生效的'

    print '\033[32m'
    print '单纯设置前景色'

    print '\033[;47m'
    print '单纯设置背景色, 没设置前景色, 所以会与上面的保持一致呢'

    print '\033[5;31m'
    print '设置显示模式与前景色, 都生效了'

    print '\033[4;;45m'
    print '设置显示模式, 背景色...只有背景色生效了'

    print '\033[;34;41m'
    print '设置前景色, 背景色...这样显示模式是不生效的'

    print '\033[5;32;43m'
    print '设置显示模式与前景色, 背景色'


    ## 使用color_print()函数
    ## color_print()函数的优势在于不为终端本身设置全局颜色显示格式, 而是打印出彩色字符串后立即恢复默认显示
    color_print('I\'m red word', 'red')
    color_print('I\'m green word', 'green')
    color_print('I\'m yellow word', 'yellow')
    color_print('I\'m blue word', 'blue')