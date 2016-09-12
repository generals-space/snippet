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
    def __init__ (self, opts):

        ## python没有?:三目运算符
        ## self.host       = 'host' in opts ? opts['host'] : 'localhost'
        self.host = opts['host'] if 'host' in opts else 'localhost'
        self.base_dn    = opts['base_dn']
        self.root_cn    = opts['root_cn']
        self.root_pwd   = opts['root_pwd']

        self.conn = ldap.initialize(self.host)
        self.conn.set_option(ldap.OPT_REFERRALS, 0)
        self.conn.protocol_version = ldap.VERSION3
        self.conn.simple_bind_s(self.root_cn, self.root_pwd)

    def list(self,
        filter,
        scope = ldap.SCOPE_SUBTREE,
        attr = None
    ):
        """
        param: scope, 所要查询的子树(目录树的根为base_dn), 例如
                "ou=People,$BASE_DN", "ou=Group,$BASE_DN)"
                对应命令行中ldapsearch中的-b参数的取值
        param: filter, 过滤语法, 可以指定cn值, ou类型等.
        """
        result = {}
        try:
            ldap_result = self.conn.search_s(self.base_dn, scope, filter, attr)
            for entry in ldap_result:
                name, data = entry
                for key, val in data.items():
                    print '%s: %s' % (key, val)
                    result[key] = val
            return result
        except ldap.LDAPError, e:
            print e
    def add(self, dn, obj):
        """
        function: 添加对象, 可以是People, Group
        param: dn, 可以看作是对象在目录树中的唯一ID
        param: obj, 目标对象所拥有的属性
        """
        try:
            ldif = modlist.addModlist(obj)
            self.conn.add_s(dn, ldif)
        except ldap.LDAPError, e:
            print e

    def delete(self, dn):
        try:
            self.conn.delete_s(dn)
        except ldap.LDAPError, e:
            print e

    def modify(self, dn, attrs):
        """
        这个函数的使用需要对ldap的命令行操作十分熟悉才行
        """
        try:
            pass
        except ldap.LDAPError, e:
            print e

def ldap_add_user():
    user_name = 'general'
    user_pwd = '123456'
    user_id = 1003
    user_dn = 'uid=%s,ou=People,%s' % (user_name, ldap_cfg['base_dn'])
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
    ## 这里ldap_conn是全局变量
    ldap_conn.add(user_dn, user_obj)
    
def ldap_del_user(user_name, base_dn):
    dn = "uid=%s,ou=People,%s" % (user_name, base_dn)
    ldap_conn.delete(dn)

if __name__ == '__main__':
    ldap_cfg = {
        'host': 'ldap://172.17.0.16:389',
        'base_dn': 'dc=jumpserver,dc=org',
        'root_cn': 'cn=admin,dc=jumpserver,dc=org',
        'root_pwd': 'secret234'
    }
    ldap_conn = LDAPConn(ldap_cfg)
    ldap_add_user()
    ldap_conn.list('cn=general')
    ldap_del_user('general','dc=jumpserver,dc=org')
    ldap_conn.list('cn=general')