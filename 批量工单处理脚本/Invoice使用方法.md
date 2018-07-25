# Invoice使用方法

1. 登录工单系统, 取得Cookie

![](https://gitimg.generals.space/611b1989818f9f5a9b3a7a063f993292.png)

成功后页面跳转到工单主页, 浏览器中按`F12`打开控制台, 选**网络**选项卡, 刷新页面, 得到网络请求队列. 

点击主页面`main.action`请求, 找到其`Request Headers`请求头中的`Cookie`字段值, 复制出来.

![](https://gitimg.generals.space/e613add4d95cbf46aa1bb673eeadf620.png)

2. 修改Invoice.py文件

首先安装依赖包`pyquery`

```
$ pip install pyquery
```

编辑`Invoice.py`, 修改其中`cookie`变量值为刚取到的`Cookie`值. 另外修改部署人姓名, 改成自己的.

![](https://gitimg.generals.space/4edf0aa825c29b14bf409d42e0b6e5de.png)

OK, 保存, 执行.

效果如下

![](https://gitimg.generals.space/3878bf4f2b48e443921340616b9a7e5f.png)

这里我只挑了10个工单做实验.

实际执行时, 可以将文件末尾的如下代码删除或注释

![](https://gitimg.generals.space/730cf6530e6da6daa0ea601c766efdb7.png)