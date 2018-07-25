#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
from pyquery import PyQuery as pyQuery

## 会话凭证
cookie = 'JSESSIONID=6E16412F3DC6CCB6FA51FF292C5B5579'
## 部署人
operator = '黄佳乐'
## 工单任务列表地址
addr = 'http://omssd.sky-mobi.com:9040/oms-workflow/workflow/myTask.action'
## 工单处理地址
operateAddr = 'http://omssd.sky-mobi.com:9040/oms-workflow/workflow/rundeploy/busiOpt!sendRetJSONStr.action'

reqHeader = {
    'Cookie': cookie
}
req = urllib2.Request(addr, headers = reqHeader)

print('正在读取任务列表, 等待响应, 大约需要10秒...')
result = urllib2.urlopen(req).read()
## print(result)
print('任务列表获取成功, 正在解析...')

###########################################################################################################

taskList = []
## 与jQ不同的是, pyQuery至少需要先实例化得到目标对象才行(毕竟不是内嵌的代码)
pyQuery = pyQuery(result)
## items()返回一个生成器, 适合用来处理list类型的元素
for item in pyQuery('.datalist').items():
    ele = item.find('td')
    firField = ele.eq(0).find('input')
    task = {
		'taskId': 					firField.eq(3).attr('value'),
		'workorderDefinitionKey': 	firField.eq(2).attr('value'),
		'orderId': 					ele.eq(1).text(),               ## 序号
		'invoiceId': 				ele.eq(2).text(),               ## 工单编号
		'invoiceName': 				ele.eq(3).text(),               ## 工单名称
		'customer': 				ele.eq(4).text(),               ## 提交人
		'project': 					ele.eq(5).text(),               ## 项目名称
		'createDate': 				ele.eq(6).text(),               ## 创建时间
		'status': 					ele.eq(7).text(),               ## 工单状态
		'detail': 					ele.eq(8).text()                ## 详情描述
    }
    taskList.append(task)

print('任务列表解析完成, 共 %d 个任务, 开始处理...' % len(taskList))

###########################################################################################################

counter, succSum, failSum = 0, 0, 0
for i in taskList:
    counter = counter + 1
    print('任务序号: %d' % counter)
    task = {
        'id': 						'',
		'optEmp': 					operator,
		'optTime': 					i['createDate'][0:-4], 			## 创建时间精确到了小数点后3位, 手动移除
		'compTime': 				i['createDate'][0:-4],
		'projectInfo': 				'',
		'compCaption': 				'完成',
		'remark': 					'',
		'compStatus': 				'成功',
		'taskId': 					i['taskId'],
		'instanceId': 				i['invoiceId'],
		'workorderDefinitionKey': 	i['workorderDefinitionKey']
    }
    ## md, 貌似不能用json格式
    ## task = json.dumps(task)
    task = urllib.unquote(urllib.urlencode(task))
    reqHeader = {
    	'Cookie': cookie,	
    	## 'Content-Type': 'application/json'
		'Content-Type': 'application/x-www-form-urlencoded'
    }
    req = urllib2.Request(operateAddr, data = task, headers = reqHeader) 
    try: 
    	## 这次的返回值直接是str类型而不是文件对象, 不需要read()了...mmp
        result = urllib2.urlopen(req)
    	result = json.load(result)
        if result['success']:
			print('处理状态: 成功')
			succSum = succSum + 1
        else:
			print('处理状态: 失败')
			failSum = failSum + 1
    except Exception as e:
        print('处理状态: 失败')
        print(e)
        failSum = failSum + 1
    if counter == 10:
        break

print('成功: %d, 失败: %d' % (succSum, failSum))
