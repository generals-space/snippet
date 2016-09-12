#!/usr/bin/python
#!coding:utf-8

## 演示了paramiko模块的基本用法
## paramiko的安装方法: pip install paramiko

## author: general
## email: generals.space
## date: 2016-08-16

import paramiko

## host = '172.17.0.13'
host = '216.189.52.44'
port = 22
user = 'longbei'
passwd = 'LuBei!123'

def execute():
    """
    function: 远程执行命令 
    且远程主机的标准输入, 标准输出, 标准错误不会自动输出, 
    而是需要程序自行取回, 然后选择性输出
    """
    try:
        command = 'ls /'
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ## 这一行是必须的, paramiko需要再本地的known_hosts中查找目标主机
        ## 如果没有就会拒绝连接
        ## AutoAddPolicy()就是自动接受未知的key
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, passwd)
        stdin, stdout, stder = ssh.exec_command(command)
        print stdout.read()
        ssh.close()
    except Exception, e:
        print str(e)
def sftp():
    """
    使用sftp工具进行上传, 下载, 列出文件等操作
    """
    try:
        ## 注意参数为元组类型...好像不用元组也可以啊
        ## remote = paramiko.Transport(host, port)
        remote = paramiko.Transport((host, port))
        ## connect的参数需要指定username与password,
        ## 这样可以不必指定其他参数并且不遵循参数列表的顺序
        ## 当然, 其他参数是有默认值的
        remote.connect(username=user, password=passwd)
        sftp = paramiko.SFTPClient.from_transport(remote)
        remote_path = '/tmp/profile'
        remote_path2 = '/tmp'
        local_path = '/etc/profile'
        local_path2 = '/tmp/profile'
        sftp.put(local_path, remote_path)
        sftp.get(remote_path, local_path2)
        
        tmp_list = sftp.listdir(remote_path2)
        print tmp_list
        remote.close()
    except Exception, e:
        print str(e)
def interact():
    """
    建立交互式shell
    """
    ## interactive文件在当前目录, 是自行编写的
    import interactive
    ps1 = "PS1='[\u@%s \W]\$ '\n" % host
    login_msg = "clear;echo -e '\\033[32mLogin %s done. Enjoy it.\\033[0m'\n" % host

    ## paramiko内置日志
    paramiko.util.log_to_file('/tmp/inter_debug.log')
    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ## 这一行是必须的, paramiko需要再本地的known_hosts中查找目标主机
        ## 如果没有就会拒绝连接
        ## AutoAddPolicy()就是自动接受未知的key
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, passwd)
        
        channel = ssh.invoke_shell()
        ## 可以选择修改命令提示符, 登陆欢迎信息等.
        ## 在正式进入交互模式之前发送
        channel.send(ps1)
        channel.send(login_msg)

        interactive.interactive_shell(channel)
        channel.close()
        ssh.close()
    except Exception, e:
        print str(e)
if __name__ == '__main__':
    ## execute()
    ## sftp()
    interact()
