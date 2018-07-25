# Invoice代码分析

知识点有两个

1. 使用cookie模拟登录, 需要`urllib`和`urllib2`两个模块

2. 使用PyQuery分析网页文档树, 需要`pyquery`

## 1. 模拟登录

一般web系统的登录行为都是在提交用户名和密码数据后与数据库中存储的数据进行比对, 成功后的返回值除了正常的网页内容外, 还有一个隐藏的Cookie值, 浏览器会将这个值保存下来, 之后每一次在这个网站上的请求都会携带这个Cookie(这个操作对普通用户不可见, 浏览器会静默完成). 

这个Cookie就是用户的登录凭证, 收到带有Cookie请求的网站会验证这个Cookie, 如果合法, 就认为这个请求是已登录用户发出的, 从而返回正确内容. 

Cookie是有有效期的, 而且这个时间的长短由服务端设置, 如果超过了这个时间, 网站会认为用户已经下线. 此时只能重新登录.

我们拿到这个Cookie后, 就开始获取任务列表.

实际上任务列表可以在[这个地址](http://omssd.sky-mobi.com:9040/oms-workflow/workflow/myTask.action)直接查看, 如下

![](https://gitimg.generals.space/a39a5ceae1b6ceac06caa6cb31f8951c.png)

我们用`urllib2`模块提供的`urlopen()`函数访问这个地址. 但是我们需要手动带上我们Cookie值, `Request()`方法可以把这个值添到我们这个模拟的请求操作里面. 这就是下面这部分代码所做的事情.

```py
reqHeader = {
    'Cookie': cookie
}
req = urllib2.Request(addr, headers = reqHeader)

print('正在读取任务列表, 等待响应, 大约需要10秒...')
result = urllib2.urlopen(req).read()
```

## 2. 解析页面

`result`是我们拿到的这个网页的内容. 你可以打印出来看看它的值, 很长. 我们要的无非就是表格里的每行数据. 但是解析这么长的字符串太难了, 用正则写会死人的.

这里引用了`pyquery`这个模块, 它模仿了前端开发的js库`jQuery`(很多做网页的开发就在用这个工具), 用它能很方便地拿到我们想要的数据.

我们想要是所有`class`属性为`datalist`的`<tr>`标签, 然后从里面找到每一个`<td>`标签的值, 它们每个表示的数据就不用说了吧.

![](https://gitimg.generals.space/b0564f98e8bf59f89216e41d5b0ee3a2.png)

这也正是下面这段代码的作用, 我们取得所有工单信息, 放在`taskList`列表里, 待用.

```py
taskList = []
## 与jQ不同的是, pyQuery至少需要先实例化得到目标对象才行(毕竟不是内嵌的代码)
pyQuery = pyQuery(result)
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

```

## 3. 模拟工单处理请求

我们点开一个工单, 按`F12`打开浏览器控制台, 按照正常方法填写内容, 提交, 同时捕捉这次请求. 截个图

![](https://gitimg.generals.space/3088d88617a7b3bd2efbf2a128e264dd.png)

我们发现了实际工单处理的地址, 还有每次一请求所携带的数据, 这会告诉服务端操作哪一个工单, 部署人是谁等等这些信息. 当然, 不要忘了我们的Cookie.

这次请求本质上与我们获取任务列表那次没什么区别, 所以我们还是用`urllib2`的`urlopen`来做.

在`Invoice.py`的for循环中, 我们为每一个工单都构造了这样的请求, 把服务端需要的信息都填进去, 这就是`task`字典变量. 但字典变量是`python`中的概念, http协议中不会认识这样的格式, 所以在构造`Request`时, 还用了`urllib`模块去格式化`task`变量, 然后再发送这次请求.

之后得到的`result`就是本次请求的响应结果, 你可以打印出来看看它的格式. 

`try...except...`是为了防止本次请求失败导致for循环被打断的问题.

## 3. 不足

限制还是蛮大的, 没写批工单的流程, 而且如下情况会导致请求失败, 不过我145个工单里只有一个这样的, 手动搞一下都没关系了.

![](https://gitimg.generals.space/9443c85f92e80d80c40ac429758608de.png)
