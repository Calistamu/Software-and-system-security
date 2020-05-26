# cuckoo
## 实验要求
- [] 安装并使用cuckoo
- [] 任意找一个程序，在cuckoo中trace获取软件行为的基本数据。
## 实验环境
ubuntu 16.04 desktop
## 实验步骤
1. 安装cuckoo  
```
$ sudo pip install -U pip setuptools
$ sudo pip install -U cuckoo
```

## 实验问题
1. win10不可直接安装cuckoo  
![](images/wrong1.png)  
因为现在的cuckoo只支持python2，因此只有在win10上使用ubuntu系统或者虚拟机的方式，不可直接安装使用。
2. 执行pip install -U cuckoo时出现报错  
![](images/wrong2.png)    
解决：[解决参考：解决 Package 'setuptools' requires a different Python: 2.7.12 not in '>=3.5' 问题](https://blog.csdn.net/weixin_43350700/article/details/104597730)  
## 实验总结
## 参考文献
[cuckoosandbox](https://cuckoosandbox.org/)  
[Introduction](https://cuckoo.readthedocs.io/en/latest/introduction/)