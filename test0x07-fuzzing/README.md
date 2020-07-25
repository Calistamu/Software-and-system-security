# Fuzzing

## 实验要求
- [x] 搜集市面上主要的路由器厂家,在厂家的官网中寻找可下载的固件在CVE漏洞数据中查找主要的家用路由器厂家的已经公开的漏洞，选择一两个能下载到切有已经公开漏洞的固件。
- [x] 如果能下载对应版本的固件，在QEMU中模拟运行。确定攻击面（对哪个端口哪个协议进行Fuzzing测试），尽可能多的抓取攻击面正常的数据包（wireshark）
- [x] 查阅BooFuzz的文档，编写这对这个攻击面，这个协议的脚本，进行Fuzzing。配置BooFuzz QEMU的崩溃异常检测，争取触发一次固件崩溃，获得崩溃相关的输入测试样本和日志。
- [] 尝试使用调试器和IDA-pro监视目标程序的崩溃过程，分析原理。
## 实验环境
ubuntu-16.04-desktop
## 实验步骤
### 一、固件下载并提取
1. 固件准备。  
固件下载地址：[DIR 850l-Download direct](http://files.dlink.com.au/products/DIR-850L)，下载dir-850l-REV_A，固件名称： DIR850LA1_FW114WWb07.bin
```
# 物理机上操作：
scp DIR850LA1_FW114WWb07.bin mudou@192.168.57.117:/home/mudou/dir-850l/
# 虚拟机中操作：
mkdir dir850l
mv DIR850LA1_FW114WWb07.bin dir850l.bin
```
2. 安装binwalk  
* [ubuntu 16.04 LTS-binwalk-manual](http://manpages.ubuntu.com/manpages/xenial/en/man1/binwalk.1.html)
```
sudo apt install binwalk
```
![](images/binwalk-ok.png)    
3. 提取固件  
* M ，—matryoshka 递归扫描可解压的
* e，—extract 提取
* 解压到的是_XXXXXX.bin.extracted/
```
binwalk -Me dir850l.bin
unsquashfs 190090.squashfs
```
### 二、模拟运行固件（两种方式）
 
### 2-1.安装qemu
* [qume](https://qume.io/)和[qemu](https://www.qemu.org/)傻傻分不清
* [Download QEMU](https://www.qemu.org/download/)
```
sudo apt-get install qemu qemu-user-static 
sudo apt-get -y install qemu qemu-system qemu-user-static qemu-user

# install build-essential
sudo apt-get -y install build-essential

# 查看当前版本 
qemu-img --version
```      
![](images/qemu-version.png)
使用file查看固件架构
![](images/file-type.png)
根据ELF文件格式，使用相应的qemu程式模拟。
```
# 由于使用的是mips,查找qemu-mips-static,将qemu-mips-static拷贝到squashfs-root文件夹下
whereis  qemu-mips-static 
cp  qemu-mips-static squashfs-root/ 
```
![](images/copy-qemutool.jpg)
```
cp /usr/bin/qemu-mips-static ./
sudo chroot . ./qemu-mips-static ./bin/ls
ls
```
出现了目录，说明qemu可以正常使用了。    
![](images/chroot-ok.png) 
### 2-2.1：模拟运行方式一 ---（user mode）FAT模拟运行固件
* [QEMU User space emulator](https://www.qemu.org/docs/master/user/main.html)
* [QemuUserEmulation](https://wiki.debian.org/QemuUserEmulation)
* [路由器固件模拟环境搭建（超详细）](https://zhuanlan.zhihu.com/p/146228197)

```
sudo apt-get install bridge-utils uml-utilities
```
* FAT-[Firmware Analysis Toolkit](https://github.com/attify/firmware-analysis-toolkit):FIRMADYNE is an automated and scalable system for performing emulation and dynamic analysis of Linux-based embedded firmware.
```
# To install just clone the repository and run the script ./setup.sh.
git clone https://github.com/attify/firmware-analysis-toolkit
cd firmware-analysis-toolkit
./setup.sh

sudo vim fat.config
# edit as follows:
[DEFAULT]
sudo_password=attify123 # sudo password
firmadyne_path=/home/attify/firmadyne # address of firmadyne

# 将固件.bin文件拷贝到firmware-analysis-toolkit文件夹下,模拟运行
./fat.py dir850.bin
```
根据图中显示路由器固件监听的桥接网络192.168.0.1，访问'http://192.168.0.1'  
![](images/fat-ok.png)   
[默认用户名Admin,默认密码为空.](http://support.routercheck.com/D-Link/DIR-850L/DefaultPassword-3.html)

### 三、fuzzing
* 参考：  
[boofuzz: Network Protocol Fuzzing for Humans](https://boofuzz.readthedocs.io/en/stable/)    
[初探BooFuzz](https://xz.aliyun.com/t/5155)
1. 安装python3
```
Step1-安装python3
# install python3
sudo apt-get install python3
# or install python3.7
# 配置软件仓库，因为python3.7新版没有发布到ubuntu的正式仓库中，通过第3方仓库来做
sudo add-apt-repository ppa:jonathonf/python-3.7
# 检查系统软件包并安装 python 3.7
sudo apt-get update
sudo apt-get install python3.7
# 设置为默认使用
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2
sudo update-alternatives --config python3
# 确认版本
python3 -V
# output:
# mudou@mudou-VirtualBox:~$ python3 -V
# Python 3.5.2
```
2. 安装boofuzz
* [installing boofuzz](https://boofuzz.readthedocs.io/en/stable/user/install.html)
```
git clone https://github.com/jtpereyda/boofuzz.git
cd boofuzz
sudo pip install .
```
3. 编写fuzz脚本
* [quickstart](https://boofuzz.readthedocs.io/en/stable/user/quickstart.html)
* [使用boofuzz进行漏洞挖掘(一)](https://www.freebuf.com/column/185606.html)
* [使用boofuzz进行漏洞挖掘(二)](https://www.freebuf.com/column/185658.html)
修改example/ftp_simple.py中的地址为192.168.0.1，端口80，```python ftp_simple.py```看到确实路由器一开始没有设置用户名和密码。  
![](images/noname.png)
然后进入'127.0.0.1:26000'查看当前fuzzing进度。  
![](images/fuzzing-process.png)  
参考[iot学习-DIR-850L漏洞分析](https://xz.aliyun.com/t/5362) 编写Poc如下：  
```
POST /HNAP1/ HTTP/1.1
Host: 192.168.0.1
User-Agent: Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:49.0) Gecko/20100101
Firefox/49.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: text/xml; charset=utf-8
SOAPAction:
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXAAAA
HNAP_AUTH: BBD0605AF8690024AF8568BE88DD7B8E 1482588069
X-Requested-With: XMLHttpRequest
Referer: http://192.168.0.1/info/Login.html
Content-Length: 306
Cookie: uid=kV8BSOXCoc
Connection: close
```
### 四、调试分析
1. 安装gdb
```
sudo apt-get update
sudo apt-get install  gdb
```
2. 安装IDA-pro
下载[IDA Pro v6.4 for Linux](https://pan.baidu.com/s/1hNJ5Y7fqs6ONbwvHzv5qnA)-密码sshc。使用scp拷贝到虚拟机中。解压，安装依赖，运行。
[在linux mint/ubuntu16.04TLS上安装IDA PRO](https://blog.csdn.net/qq_36142158/article/details/79504415)
```
# 64位需要安装依赖
sudo apt-get install libc6-i686:i386 libexpat1:i386 libffi6:i386 libfontconfig1:i386 libfreetype6:i386 libgcc1:i386 libglib2.0-0:i386 libice6:i386 libpcre3:i386 libpng12-0:i386 libsm6:i386 libstdc++6:i386 libuuid1:i386 libx11-6:i386 libxau6:i386 libxcb1:i386 libxdmcp6:i386 libxext6:i386 libxrender1:i386 zlib1g:i386 libx11-xcb1:i386 libdbus-1-3:i386 libxi6:i386 libsm6:i386 libcurl3:i386

sudo apt-get install libstdc++5:i386
sudo apt-get install libc6:i386
sudo apt-get install lib32stdc++6
sudo apt-get install lib32z1
sudo apt-get  install libglib2.0-0:i386
sudo apt-get install libx11-6:i386

# 32位运行
./idaq   
# 64位运行
./idaq64
```
运行以后看到命令行如下图-没有连接server，但ida-pro已经可以成功运行。  
![](images/ida-ok.png)  
在虚拟机中弹出了ida-pro的启动弹窗   
![](images/ida-ok3.png)
任意打开dir850l.bin文件，看到如下图，ida-pro安装成功。  
![](images/ida-ok2.png)
3. 安装下载burpsuite  
下载[burpsuite](https://portswigger.net/burp/releases/professional-community-2020-6)，scp拷贝到Ubuntu中运行.sh文件，一直[enter]即可。
## 实验问题
### 1. 固件提取第一次尝试结果（没有错，但是下载的不是官方的文件，总有些别扭，因此重新再来）  

固件下载地址：  
* [D-Link DIR-850L 固件下载](http://driver.zol.com.cn/detail/47/463483.shtml#download-box)
* [D-Link DIR-850L 固件下载-驱动天空](https://www.drvsky.com/dlink/DIR-850L.htm#download)

使用scp将dir-850l.zip和dir-850l.exe拷贝到虚拟机中，解压缩dir-850l.zip,得到DIR850L_FW113WWb01_f4if.bin，更改文件名称为dir850l.bin。 
```binwalk -Me dir850l.bin```提取固件，得到_dir850l.bin.extracted文件夹。  
![](images/ex-1.png)  
可以看到Squashfs系统，小端法。压缩包的md5校验码和压缩包内部2888文件的校验码。   
重命名_dir850l.bin.extracted为dir850l。进入dir850l文件夹中看到190090.squashfs是我们的目标文件。
![](images/ex-2.png)   
提取文件，方式两种，无论哪种方法，得到的结果是一样的。  
一：使用 binwalk -Me 命令提取该文件。  
二：使用 unsquashfs 190090.squashfs 命令来提取文件。  
* [SquashFS HOWTO](https://www.tldp.org/HOWTO/html_single/SquashFS-HOWTO/)
* 重命名原有的squashfs-root为squashfs-root-old.  

binwalk提取的结果如下图：   
![](images/ex-3.png)  
unsquashfs 190090.squashfs提取结果如下图：  
![](images/ex-4.png)
* 此处的'create_inode: could not create character device squashfs-root/dev/XXX, because you're not superuser!'是正常的，因此需要特别的权限create device files，并不会影响本次实验.[could not create character device "foo" because you're not superuser!](https://github.com/devttys0/sasquatch/issues/14)  

![](images/ex-5.png)

### 2. 第一次拷贝qemu tool时弄错了二进制结构  
进入squashfs-root目录，将将qemu-mipsel-static拷贝到当前目录下  
![](images/run-1.png)   
总结：应该先查看类型再拷贝

### 3. ```sudo chroot . ./qemu-mips-static ./bin/sh```开启模拟运行以后，报错'command not found'.  
![](images/wrong1.png)
解决：  
```
$ exit
$ sudo modprobe binfmt_misc
$ sudo mount binfmt_misc -t binfmt_misc /proc/sys/fs/binfmt_misc
$ sudo -s
# echo ':mips:M::\x7fELF\x01\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x08:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff:/qemu:' > /proc/sys/fs/binfmt_misc/register
# exit
$ cp ./qemu-mips-static ./qemu
```

### 4. 虚拟机扩容 - 仅仅磁盘扩容是不够的，系统依然无法使用
解决：[VirtualBox文件系统已满--磁盘扩容](https://www.cnblogs.com/cthon/p/9334828.html)

### 5. ```sudo chroot . ./qemu-mips-static ./bin/ls```后输入```ls```会出现ls:not found的错误.
解决：  
```
$ exit
$ sudo modprobe binfmt_misc
$ sudo mount binfmt_misc -t binfmt_misc /proc/sys/fs/binfmt_misc
$ sudo -s
# echo ':mips:M::\x7fELF\x01\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x08:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff:/qemu:' > /proc/sys/fs/binfmt_misc/register
# exit
$ cp ./qemu-mips-static ./qemu
```
再次运行```sudo chroot . ./qemu-mips-static ./bin/sh```成功，说明qemu可以正常使用了。    
![](images/chroot-ok.png) 

### 6. ```sudo apt-get install curses-devel```报错：'Unable to locate package curses-devel'  
解决：参考[ubuntu16.04安装ncurses-devel](https://blog.csdn.net/WANG__RONGWEI/article/details/54846759)，使用```sudo apt-get install libncurses5-dev```

### 7. 执行```sudo apt-get```的时候出现报错'Unable to lock the administration directory (/var/lib/dpkg/), is another process using it?'   
解决：[Unable to lock the administration directory (/var/lib/dpkg/) is another process using it?  ](https://askubuntu.com/questions/15433/unable-to-lock-the-administration-directory-var-lib-dpkg-is-another-process),执行```sudo rm /var/lib/apt/lists/lock```

### 8. Ubuntu16.04安装Wireshark
```
# 添加wireshark的源
$ sudo apt-add-repository ppa:wireshark-dev/stable
# 更新软件源
sudo apt-get update
# 安装wireshark
sudo apt-get install wireshark
# 新增wireshark用户组
$ sudo groupadd  wireshark
# 将dumpcap更改为wireshark用户组 
$sudo chgrp wireshark /usr/bin/dumpcap 
# 让wireshark用户组有root权限使用dumpcap
$ sudo chmod 4755 /usr/bin/dumpcap
# 将需要使用的普通用户名加入wireshark用户组
$ sudo gpasswd -a mudou wireshark 
```
## 实验总结
### 1. 路由器厂家学习总结
* 参考[全球最好的八大消费类路由器品牌商](https://tnext.org/3773.html)
* [Netgear](https://en.wikipedia.org/wiki/Netgear)
* [Linksys](https://en.wikipedia.org/wiki/Linksys)
* [TP-Link](https://en.wikipedia.org/wiki/TP-Link)
* [D-Link](https://en.wikipedia.org/wiki/D-Link)
* [Cisco Systems](https://en.wikipedia.org/wiki/Cisco_Systems)
* 总结：  
高端品牌：华硕、网件、领势等  
传统老牌：TP-LINK、水星、腾达等等    
新进品牌：小米（红米）、华为（荣耀）、360   

### 2. 路由器漏洞的威胁-有这么可怕吗？   
* 参考：
  - [WiFi审判日：黑客劫持全球30万台无线路由器](https://www.aqniu.com/threat-alert/1998.html)  
  - [路由器漏洞频发，有些永远不会修补？！](https://www.mottoin.com/detail/2596.html)
  - [The 5 most common router attacks on a network](https://www.intelligentcio.com/eu/2017/10/16/the-5-most-common-router-attacks-on-a-network/)
  - [Router attacks: Five simple tips to lock criminals out](https://www.welivesecurity.com/2014/05/23/router-attacks-five-simple-tips-lock-criminals/)
  - [中国十大路由器厂家排行榜](https://www.douban.com/note/548077904/)  

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

### 3. qume运行两种模式：  
* [Qemu: User mode emulation and Full system emulation](https://www.cnblogs.com/pengdonglin137/p/5020143.html)  
* [QEMU-wiki](https://zh.wikipedia.org/wiki/QEMU)   

user mode : qemu-mips(mipsel/arm)-static。User mode：又称作“用户模式”，在这种模块下，QEMU运行针对不同指令编译的单个Linux或Darwin/macOS程序。系统调用与32/64位接口适应。在这种模式下，我们可以实现交叉编译（cross-compilation）与交叉侦错（cross- debugging）。  

system mode:qemu-system-mips(mipsel) : “系统模式”，在这种模式下，QEMU模拟一个完整的计算机系统，包括外围设备。它可以用于在一台计算机上提供多台虚拟计算机的虚拟主机。 QEMU可以实现许多客户机OS的引导，比如x86，MIPS，32-bit ARMv7，PowerPC等等。   

因此，在qemu运行固件的方式也有两种：  
① 将文件系统上传到 qemu mips 虚拟机中运行（system mode）    
② 借助 firmadyne 工具运行固件(user mode)

### 4. 熵：一个系统越是有序，信息熵就越低；反之，一个系统越是混乱，信息熵就越高。  
* 参考：  
   - [Differentiate Encryption From Compression Using Math](http://www.devttys0.com/2013/06/differentiate-encryption-from-compression-using-math/):The entropy of data can tell us a lot about the data’s contents. Encrypted data is typically a flat line with no variation, while compressed data will often have at least some variation.  
  - [Encryption vs Compression, Part 2](http://www.devttys0.com/2013/06/encryption-vs-compression-part-2/)  

### 5. 本次实验dir-850l固件下载地址集锦：
* [D-Link DIR-850L 固件下载](http://driver.zol.com.cn/detail/47/463483.shtml#download-box)
* [D-Link DIR-850L 固件下载-驱动天空](https://www.drvsky.com/dlink/DIR-850L.htm#download)
* [D-LINK官网](https://support.dlink.com/ProductInfo.aspx?m=dir-850L)
* [DIR-850L-D-Link Australia & New Zealand Support Resources](http://support.dlink.com.au/Download/download.aspx?product=DIR-850L)  

### 6. 查看固件架构两种方式。  
查看方法一：使用[rabin](http://www.linuxcertif.com/man/1/rabin/) - Binary program info extractor
```
# install radare
git clone https://github.com/radare/radare2.git
cd radare2/sys
./install.sh 
cd ..

ls -lF ./bin/ls
# output:
# lrwxrwxrwx 1 mudou mudou 7 6月  16 14:11 ./bin/ls -> busybox*
rabin2 -I ./bin/busybox
# output: arch mips
rabin2 -l ./bin/busybox
```
![](images/mips.png)    
查看方法二：使用file
使用file得到更多详细信息  
![](images/file-type.png)

### 7. mips vs mipsel vs mips64el  
[MIPSPort](https://wiki.debian.org/MIPSPort):Through the Debian 10 ("buster") release, Debian currently provides 3 ports, 'mips', 'mipsel', and 'mips64el'. The 'mips' and 'mipsel' ports are respectively big and little endian variants, using the O32 ABI with hardware floating point. They use the MIPS II ISA in Jessie and the MIPS32R2 ISA in Stretch and later. The 'mips64el' port is a 64-bit little endian port using the N64 ABI, hardware floating point and the MIPS64R2 ISA.   
总结：   
mips 是32位大端字节序   
mipsel 是32位小端字节序   
mips64el 是64位小端字节序 
### 8.---2-2.2：模拟运行方式二 --- （system mode）qemu安装mips虚拟机
* 完成到一半，先交作业，在这里总结出已学习的内容
* [QEMU System Emulator Targets](https://www.qemu.org/docs/master/system/targets.html)
* [MIPS System emulator](https://www.qemu.org/docs/master/system/target-mips.html)
* [How to build a Debian MIPS image on QEMU](https://markuta.com/how-to-build-a-mips-qemu-image-on-debian/) 
* [MIPS环境填坑指南](https://zhuanlan.zhihu.com/p/110365843) 
* [Emulating Embedded Linux Devices with QEMU](https://www.novetta.com/2018/02/emulating-embedded-linux-devices-with-qemu/)
* [QEMU System Emulation User’s Guide](https://www.qemu.org/docs/master/system/index.html)

* [Fuzzing Embedded Linux Devices](https://www.novetta.com/2018/07/fuzzing-embedded-linux-devices/)  
* [Emulating Embedded Linux Devices with QEMU](https://www.novetta.com/2018/02/emulating-embedded-linux-devices-with-qemu/)  
* [Emulating Embedded Linux Systems with QEMU](https://www.novetta.com/2018/02/emulating-embedded-linux-systems-with-qemu/)
* [Dynamic Analysis of Firmware Using Firmadyne](https://opensourceforu.com/2018/09/dynamic-analysis-of-firmware-using-firmadyne/)  
* [D-Link: A Firmware Security Analysis – Part 2](https://www.refirmlabs.com/d-link-a-firmware-security-analysis-part-2/)
* [D-Link: A Firmware Security Analysis – Part 3](https://www.refirmlabs.com/d-link-a-firmware-security-analysis-part-3/)
* [D-Link: A Firmware Security Analysis – Part 4](https://www.refirmlabs.com/d-link-a-firmware-security-analysis-part-4/)
* [Getting started with Firmware Emulation for IoT Devices](https://blog.attify.com/getting-started-with-firmware-emulation/) 
* [DLink RCE 漏洞 CVE-2019-17621 分析](https://www.geekmeta.com/article/1292672.html) 
* [IoT安全：调试环境搭建教程(MIPS篇)](https://bbs.pediy.com/thread-229583.htm)
* [在QEMU MIPS虚拟机上运行MIPS程序（ssh方式](http://zeroisone.cc/2018/03/20/%E5%9B%BA%E4%BB%B6%E6%A8%A1%E6%8B%9F%E8%B0%83%E8%AF%95%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA/#qemu%E6%A8%A1%E6%8B%9Fmips%E7%A8%8B%E5%BA%8F)
* [DLink RCE漏洞CVE-2019-17621分析](https://www.freebuf.com/vuls/228726.html)
* [使用QEMU配置一台虚拟MIPS系统](https://blog.sbw.so/u/create-mips-virtual-machine-in-qemu.html)
* [路由器逆向分析------在QEMU MIPS虚拟机上运行MIPS程序（ssh方式）](https://blog.csdn.net/QQ1084283172/article/details/69652258)
* [详细的路由器漏洞分析环境搭建教程](https://chuansongme.com/n/864762852648)
* [路由器固件安全分析技术（一）](https://www.vulbox.com/knowledge/detail/?id=35%20%20)
* [路由器固件安全分析技术（二）](https://www.vulbox.com/knowledge/detail/?id=42%20)
* [msfvenom生成各类Payload命令](https://www.huo119.com/post/909.shtm)
1. 查看qemu版本信息```qemu-img --version```  
![](images/qemu-version.png)
2. 使用debian开发人员做好的镜像，其中已经包含了debian的squeeze版,下载[debian_squeeze_mips_standard.qcow2和vmlinux-2.6.32-5-4kc-malta](https://people.debian.org/~aurel32/qemu/mips/),使用scp拷贝到虚拟机中。  

3. 配置
```
# 安装依赖
sudo apt-get install bridge-utils uml-utilities

# 修改ubuntu主机网络配置
sudo vim /etc/network/interfaces
# change as follows:
auto lo
iface lo inet loopback
 
# ubuntu 16.04的系统用ens33代替eth0
auto ens33
iface ens33 inet manual
up ifconfig ens33 0.0.0.0 up
 
auto br0
iface br0 inet dhcp
bridge_ports ens33
bridge_stp off
bridge_maxwait 1


# 修改QEMU的网络接口启动脚本，重启网络使配置生效
sudo vim /etc/qemu-ifup
# as follows:
#!/bin/sh
echo "Executing /etc/qemu-ifup"
echo "Bringing $1 for bridged mode..."
sudo /sbin/ifconfig $1 0.0.0.0 promisc up
echo "Adding $1 to br0..."
sudo /sbin/brctl addif br0 $1
sleep 3
```

### 本次实验心得
1. 做实验的过程中，没有思路，或者忘了方法，回头看看老师曾经说了什么。
## 实验效果
[fuzzing实验](https://www.bilibili.com/video/BV1BK4y1e7oG)
## 参考文献
[boofuzz: Network Protocol Fuzzing for Humans](https://boofuzz.readthedocs.io/en/stable/)  
[QEMU](https://www.qemu.org/)  
[QEMU version 4.2.0 User Documentati](https://qemu.weilnetz.de/doc/qemu-doc.html)  
[QEMU System Emulator Targets](https://www.qemu.org/docs/master/system/targets.html)

[路由器漏洞分析系列（1）：路由器固件模拟环境搭建](https://xz.aliyun.com/t/5697)  
[D-Link 850L&645路由漏洞分析](https://xz.aliyun.com/t/2941)    

漏洞分析：  
[路由器漏洞复现分析第二弹：CNVD-2018-01084 ](https://www.freebuf.com/vuls/162627.html)  
[D-Link系列路由器漏洞挖掘入门](https://paper.seebug.org/429/)  
[D-Link DIR-850L 路由器漏洞验证报告](https://gorgias.me/2017/08/11/D-Link-DIR-850L-%E8%B7%AF%E7%94%B1%E5%99%A8%E6%BC%8F%E6%B4%9E%E9%AA%8C%E8%AF%81%E6%8A%A5%E5%91%8A/)   
[D-Link DIR-850L路由器分析之获取设备shell](https://cq674350529.github.io/2019/03/18/D-Link-DIR-850L%E8%B7%AF%E7%94%B1%E5%99%A8%E5%88%86%E6%9E%90%E4%B9%8B%E8%8E%B7%E5%8F%96%E8%AE%BE%E5%A4%87shell/)    
[一个路由器竟然被曝10个零日漏洞](https://www.aqniu.com/threat-alert/28078.html)   
[Pwning the Dlink 850L routers and abusing the MyDlink Cloud protocol](https://pierrekim.github.io/blog/2017-09-08-dlink-850l-mydlink-cloud-0days-vulnerabilities.html)  
关于fuzzing非常有用的总结文章：  
[fuzzing-stuff](https://github.com/alphaSeclab/fuzzing-stuff)  
[OWASP 固件安全性测试指南 ](https://www.anquanke.com/post/id/202942#h2-0)

