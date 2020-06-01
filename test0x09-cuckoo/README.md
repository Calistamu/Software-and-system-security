# cuckoo
## 实验要求
- [] 安装并使用cuckoo
- [] 任意找一个程序，在cuckoo中trace获取软件行为的基本数据。
## 实验环境
ubuntu 16.04 desktop
## 实验步骤
### 一、 安装cuckoo  
1. 安装依赖
* 本次实验安装了:所有相关的python libraries,virtualbox,tcpdump,M2Crypto,guacd.没有安装Volatility
* [Volatility](https://github.com/volatilityfoundation):内存取证工具,结合cuckoo,分析更深度与全面，可以防止恶意软件利用rookit技术逃逸沙箱。要根据python的版本进行选择安装。
* [M2Crypto](https://pypi.org/project/M2Crypto/)
* [guacamole/guacd](https://hub.docker.com/r/guacamole/guacd)
```
# install python libraries
$ sudo apt-get install python python-pip python-dev libffi-dev libssl-dev
$ sudo apt-get install python-virtualenv python-setuptools
$ sudo apt-get install libjpeg-dev zlib1g-dev swig
$ sudo apt-get install mongodb
$ sudo apt-get install postgresql libpq-dev
$ sudo apt-get install qemu-kvm libvirt-bin ubuntu-vm-builder bridge-utils python-libvirt
$ sudo pip install XenAPI

# install virtual software
$ echo deb http://download.virtualbox.org/virtualbox/debian xenial contrib | sudo tee -a /etc/apt/sources.list.d/virtualbox.list
$ wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo apt-key add -
$ sudo apt-get update
$ sudo apt-get install virtualbox-5.1

# install Tcpdump
$ sudo apt-get install tcpdump apparmor-utils
$ sudo aa-disable /usr/sbin/tcpdump

# install Volatility(optional and not be installed this time)

# install M2Crypto(optional)
$ sudo apt-get install swig
$ sudo pip install m2crypto==0.24.0

# install guacd(optional)
$ sudo apt install libguac-client-rdp0 libguac-client-vnc0 libguac-client-ssh0 guacd
```
2. 安装cuckoo
* [KVM](https://help.ubuntu.com/community/KVM)
```
# add user
$ sudo adduser cuckoo
# If you’re using VirtualBox, make sure the new user belongs to the “vboxusers” group (or the group you used to run VirtualBox):
$ sudo usermod -a -G vboxusers cuckoo
#If you’re using KVM or any other libvirt based module, make sure the new user belongs to the “libvirtd” group (or the group your Linux distribution uses to run libvirt):
$ sudo usermod -a -G libvirtd cuckoo

# install cuckoo (using virtualenv)
$ virtualenv venv
$ . venv/bin/activate
(venv)$ pip install -U pip setuptools
(venv)$ pip install -U cuckoo
# 启动cuckoo
cuckoo
# 查看帮助
cuckoo --help
```
看到如下页面说明安装成功,版本是2.0.7    
![](images/setup-ok.png)  
* 
2. 
```
# 开启mongodb
sudo systemctl enable mongodb
sudo systemctl start mongodb
```
## 实验问题
1. win10不可直接安装cuckoo  
![](images/wrong1.png)  
因为现在的cuckoo只支持python2，因此只有在win10上使用ubuntu系统或者虚拟机的方式，不可直接安装使用。
2. 执行pip install -U cuckoo时出现报错  
![](images/wrong2.png)    
解决：[解决参考：解决 Package 'setuptools' requires a different Python: 2.7.12 not in '>=3.5' 问题](https://blog.csdn.net/weixin_43350700/article/details/104597730)    
之后又出现这样的报错  
![](images/wrong2.png)  
解决：没有好好读文档，先安装依赖
3. 没有安装ssh，报错：'ssh: connect to host localhost port 22: Connection refused'  
解决：  
```
# install
sudo apt-get install openssh-server 
# start
sudo /etc/init.d/ssh start  
# see stauts
ps -e|grep ssh 
# change port
vim /etc/ssh/sshd_config
```
## 实验总结
1. cuckoo configuration files
* cuckoo.conf: for configuring general behavior and analysis options.
* auxiliary.conf: for enabling and configuring auxiliary modules.
* <machinery>.conf: for defining the options for your virtualization software (the file has the same name of the machinery module you choose in cuckoo.conf).
* memory.conf: Volatility configuration.
* processing.conf: for enabling and configuring processing modules.
* reporting.conf: for enabling or disabling report formats.

* To get Cuckoo working you should at the very least edit cuckoo.conf and <machinery>.conf.
## 参考文献
[cuckoosandbox](https://cuckoosandbox.org/)  
[Introduction](https://cuckoo.readthedocs.io/en/latest/introduction/)  
[usage](https://cuckoo.readthedocs.io/en/latest/usage/start/)