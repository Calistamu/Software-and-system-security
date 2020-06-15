# Fuzzing

## 实验要求
- [] 搜集市面上主要的路由器厂家,在厂家的官网中寻找可下载的固件在CVE漏洞数据中查找主要的家用路由器厂家的已经公开的漏洞，选择一两个能下载到切有已经公开漏洞的固件。
- [] 如果能下载对应版本的固件，在QEMU中模拟运行。确定攻击面（对哪个端口那个协议进行Fuzzing测试），尽可能多的抓取攻击面正常的数据包（wireshark）
- [] 查阅BooFuzz的文档，编写这对这个攻击面，这个协议的脚本，进行Fuzzing。配置BooFuzz QEMU的崩溃异常检测，争取触发一次固件崩溃，获得崩溃相关的输入测试样本和日志。尝试使用调试器和IDA-pro监视目标程序的崩溃过程，分析原理。
## 实验环境
## 实验步骤
1. 
### 固件下载并提取
* [D-Link DIR-850L 固件下载](http://driver.zol.com.cn/detail/47/463483.shtml#download-box)或[D-Link DIR-850L 固件下载-驱动天空](https://www.drvsky.com/dlink/DIR-850L.htm#download)
* [ubuntu 16.04 LTS-binwalk-manual](http://manpages.ubuntu.com/manpages/xenial/en/man1/binwalk.1.html)
## 实验问题
## 实验总结
1. 路由器厂家学习
* [全球最好的八大消费类路由器品牌商](https://tnext.org/3773.html)
* [Netgear](https://en.wikipedia.org/wiki/Netgear)
* [Linksys](https://en.wikipedia.org/wiki/Linksys)
* [TP-Link](https://en.wikipedia.org/wiki/TP-Link)
* [D-Link](https://en.wikipedia.org/wiki/D-Link)
* [Cisco Systems](https://en.wikipedia.org/wiki/Cisco_Systems)
* 高端品牌：华硕、网件、领势等  
传统老牌：TP-LINK、水星、腾达等等    
新进品牌：小米（红米）、华为（荣耀）、360   
2. 路由器漏洞的威胁-有这么可怕吗？
参考：  
* [WiFi审判日：黑客劫持全球30万台无线路由器](https://www.aqniu.com/threat-alert/1998.html)  
* [路由器漏洞频发，有些永远不会修补？！](https://www.mottoin.com/detail/2596.html)
* [The 5 most common router attacks on a network](https://www.intelligentcio.com/eu/2017/10/16/the-5-most-common-router-attacks-on-a-network/)
* [Router attacks: Five simple tips to lock criminals out](https://www.welivesecurity.com/2014/05/23/router-attacks-five-simple-tips-lock-criminals/)
* [中国十大路由器厂家排行榜](https://www.douban.com/note/548077904/)  
威胁总结：  
* 信息窃取：除了直接获取账号和密码，也可能跳转到钓鱼网站
* 通过路由器控制智能家居，危险无处不在
* 促进黑产
* 厂商的不安全亦是用户的不安全
* 路由器被当作犯罪跳板

常见的攻击手段总结：  
* Denial of Service (DOS)
* Packet Mistreating Attacks (PMA)
* Routing Table Poisoning (RTP)
* Hit and Run (HAR)
* Persistent Attacks (PA)
## 参考文献
[boofuzz: Network Protocol Fuzzing for Humans](https://boofuzz.readthedocs.io/en/stable/)  
[QUME](https://www.qemu.org/)  
[QEMU version 4.2.0 User Documentati](https://qemu.weilnetz.de/doc/qemu-doc.html)  
[路由器漏洞分析系列（1）：路由器固件模拟环境搭建](https://xz.aliyun.com/t/5697)  
[路由器漏洞挖掘之栈溢出入门（二）](https://juejin.im/entry/5c79430df265da2db5424f94)  
[D-Link系列路由器漏洞挖掘入门](https://paper.seebug.org/429/)  
[利用DVRF学习固件分析系列（一）](https://www.anquanke.com/post/id/84580)  
[D-Link DIR-850L路由器分析之获取设备shell](https://cq674350529.github.io/2019/03/18/D-Link-DIR-850L%E8%B7%AF%E7%94%B1%E5%99%A8%E5%88%86%E6%9E%90%E4%B9%8B%E8%8E%B7%E5%8F%96%E8%AE%BE%E5%A4%87shell/)  
