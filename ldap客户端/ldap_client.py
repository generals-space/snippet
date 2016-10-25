#!/usr/bin/python
#!coding:utf-8

########################################################
## python-ldap客户端程序
## 环境要求
## $ yum install openldap-devel
## $ pip install python-ldap
########################################################

import ldap
from ldap import modlist

class LDAPConn():
    """
    LDAP连接管理类, 类似于数据库连接类, 实现增删改查的功能
    """
    def __init__ (self, *args, **kwargs):
        ## ldap_result为封装类中执行ldap相关函数的异常返回结果
        ## {'desc': "Can't contact LDAP server"},取其中desc字段的值
        self.ldap_result = ''
        ## ldap函数执行成功时为1, 异常时赋值为0
        self.ldap_status = 0
        ## 是否已绑定某个用户, 可看作是否已登录
        self.is_bind = 0
        self.base_dn = ''



        ## python没有?:三目运算符
        ## self.host       = 'host' in kwargs ? kwargs['host'] : 'localhost'
        self.host = kwargs['host'] if 'host' in kwargs else '127.0.0.1'
        self.port = kwargs['port'] if 'port' in kwargs else '389'
        self.ldap_addr = 'ldap://' + self.host + ':' + self.port
        ## initialize不会出现异常, 就算ldap服务器的地址写错也不会
        self.conn = ldap.initialize(self.ldap_addr)
        self.conn.set_option(ldap.OPT_REFERRALS, 0)
        self.conn.protocol_version = ldap.VERSION3

    def get_base_dn(self):
        return self.base_dn
    def set_base_dn(self, base_dn):
        self.base_dn = base_dn

    def verify(self, dn, pwd):
        try:
	    dn = dn if self.base_dn == '' else dn + ',' + self.base_dn
            ## 可以是任何用户, 验证后就获得该用户的相应权限
            self.conn.simple_bind_s(dn, pwd)
            self.ldap_status = 1
            self.ldap_result = ''
            ## 验证成功, 则可看作已登录, 拥有指定权限
            self.is_bind = 1
        except ldap.LDAPError, e:
            ## e貌似是list类型
            self.ldap_result = e[0]['desc']
            self.is_bind = 0
        return self.ldap_status

    def list(self,
        filter='',
        scope = ldap.SCOPE_SUBTREE,
        attr = None
    ):
        """
        param: scope, 所要查询的子树(目录树的根为base_dn), 例如
                "ou=People,$BASE_DN", "ou=Group,$BASE_DN)"
                对应命令行中ldapsearch中的-b参数的取值
        param: filter, 过滤语法, 可以指定cn值, ou类型等.
	return: 返回值为list类型
        """
        result = []
        try:
            search_result = self.conn.search_s(self.base_dn, scope, filter, attr)
            for entry in search_result:
                name, data = entry
                tmpObj = {}
                for key, val in data.items():
                    ## print '%s: %s' % (key, val)
                    tmpObj[key] = val
                result.append(tmpObj)
            self.ldap_status = 1
            self.ldap_result = ''
            return result
        except ldap.LDAPError, e:
            self.ldap_status = 0
            self.ldap_result = e[0]['desc']
            return result
    def add(self, dn, obj):
        """
        function: 添加对象, 可以是People, Group
        param: dn, 可以看作是对象在目录树中的唯一ID
        param: obj, 目标对象所拥有的属性
        """
        try:
	    dn = dn if self.base_dn == '' else dn + ',' + self.base_dn
            ldif = modlist.addModlist(obj)
            self.conn.add_s(dn, ldif)
            self.ldap_status = 1
            self.ldap_result = ''
	    return result
        except ldap.LDAPError, e:
            self.ldap_status = 0
            self.ldap_result = e[0]['desc']
            return e

    def delete(self, dn):
        try:
            del_result = self.conn.delete_s(dn)
        except ldap.LDAPError, e:
            ## {'matched': 'ou=People,dc=jumpserver,dc=org', 'desc': 'No such object'}
            return e

    def modify(self, dn, attrs):
        """
        这个函数的使用需要对ldap的命令行操作十分熟悉才行
        """
        try:
            pass
        except ldap.LDAPError, e:
            print e

if __name__ == '__main__':
    host = '172.17.0.16'
    base_dn = 'dc=jumpserver,dc=org'
    ## 尝试连接, ldap_conn是全局变量, 因为if语句的作用域就是全局的
    ldap_conn = LDAPConn(host = host)
    ## 最好记得设置base_dn, 会方便一些
    ldap_conn.set_base_dn(base_dn)
    ## 身份验证, 之后获得对应的用户权限
    status = ldap_conn.verify('cn=admin', 'secret234')
    if not status == 1:
        print ldap_conn.ldap_result

    ## 验证增删改查操作
    ## 添加用户
    user_name = 'general'
    user_pwd = '123456'
    user_id = 1003
    user_dn = 'uid=%s,ou=People' % user_name
    ## 注意user_obj的格式, 所有字段都是数组类型, 
    ## 并且uid,cn,uidNumber,gidNumber必须为字符串类型
    user_obj = {
        'uid': [str(user_name)],
        'cn': [str(user_name)],
        'objectClass': [
            'account',
            'posixAccount',
            'top',
            'shadowAccount'
        ],
        'userPassword': [user_pwd],
        'loginShell': ['/bin/bash'],
        'uidNumber': [str(user_id)],
        'gidNumber': [str(user_id)],
        'homeDirectory': ['/home/%s' % user_name]
    }
    status = ldap_conn.add(user_dn, user_obj)
    print 'here'
    if not status == 1:
        print ldap_conn.ldap_result
    else:
        print 'success'
 
    user = ldap_conn.list(filter = "cn=%s" % user_name)
    print user
