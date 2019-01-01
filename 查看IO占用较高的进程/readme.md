# Python-查看IO占用较高的进程

参考文章

1. [怎么查看linux的哪个进程占用磁盘io较多](https://zhidao.baidu.com/question/1882904486137130588.html)

Linux下查看IO占用较高的进程可以用`iotop`, 但它需要内核支持, 大概是2.6.xxx吧, 与python版本没有太大关系. 下面这个脚本只依赖`python2.6+`, 不依赖内核.

直接运行脚本，默认情况下收集3秒钟数据，显示读写最高的前三个进程。如用参数可以使用命令“python fhip.py 4 5 3”，第一个数位每次收集读写数据的间隔秒数，第二个数是打印出读写最多的n个进程，第三个为运行脚本的次数。因为参数部分写的比较简单那，所以用参数必须3个全写.

```
$ python iotest.py 
pid     process     read(bytes) pid     process     write(btyes)
2849    (krfcommd)  0           18610   (java)      159744
664     (python)    0           20034   (java)      122880
8018    (mingetty)  0           2022    (kjournald) 110592
```