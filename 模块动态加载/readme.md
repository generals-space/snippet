动态加载的目的就是组件的热插拔. 

我们需要一个子组件目录, 在主模块中遍历所有组件, 然后通过python的`importlib`进行动态导入然后调用子模块的接口. 这样, 在组件目录增删py文件时, 就可以实现动态增删模块, 而不需要程序重启.

这需要子模块能实现同样的接口, 来保证在主模块中的调用不会出错.

此示例需要python3支持.