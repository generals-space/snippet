#!/usr/bin/python
# encoding: utf-8
# @author: eddy
# @contact: 278298125@qq.com
# @site: http://my.oschina.net/eddylinux
# @file: menu.py
# @time: 2016-01-18 21:58 
# @version: 1.0

import socket
import sys
from paramiko.py3compat import u

## 记录用户在远程主机上的操作及响应
log_file_path = '/tmp/inter_remote.log'
log_file = open(log_file_path, 'a')
try:
    import termios
    import tty
    has_termios = True
except ImportError:
    has_termios = False


def interactive_shell(chan):
    if has_termios:
        posix_shell(chan)
    else:
        windows_shell(chan)

#linux处理方法
def posix_shell(chan):
    import select
    #获取原来的tty
    oldtty = termios.tcgetattr(sys.stdin)
    try:
        #设置tty
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)

        while True:
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    ## 1024应该是缓冲区大小
                    x = u(chan.recv(1024))
                    if len(x) == 0:
                        sys.stdout.write('\r\n*** EOF\r\n')
                        break
                    sys.stdout.write(x)
                    sys.stdout.flush()
                    log_file.write(x)
                    log_file.flush()
                except socket.timeout:
                    pass
            if sys.stdin in r:
                x = sys.stdin.read(1)
                if len(x) == 0:
                    break
                chan.send(x)

    finally:
        #把终端的tty切换回原来的
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

    
#windows处理方法
def windows_shell(chan):
    import threading

    sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")
        
    def writeall(sock):
        while True:
            data = sock.recv(256)
            if not data:
                sys.stdout.write('\r\n*** EOF ***\r\n\r\n')
                sys.stdout.flush()
                break
            sys.stdout.write(data)
            sys.stdout.flush()
        
    writer = threading.Thread(target=writeall, args=(chan,))
    writer.start()
        
    try:
        while True:
            d = sys.stdin.read(1)
            if not d:
                break
            chan.send(d)
    except EOFError:
        # user hit ^Z or F6
        pass
