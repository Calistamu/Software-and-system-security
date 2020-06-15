# cuckoo
## 实验要求
- [] 安装并使用cuckoo
- [] 任意找一个程序，在cuckoo中trace获取软件行为的基本数据。
## 实验环境
host：ubuntu 18.04 LTS    
guest: windows xp-sp3     
两个主机都是双网卡：NAT+host-only(并且是同一个网络)   
## 实验步骤

### 宿主机HOST准备
#### 一、 安装cuckoo  
1. 安装依赖
* 本次实验安装了:所有相关的python libraries,virtualbox,tcpdump,M2Crypto,guacd.没有安装Volatility
* [Volatility](https://github.com/volatilityfoundation):内存取证工具,结合cuckoo,分析更深度与全面，可以防止恶意软件利用rookit技术逃逸沙箱。要根据python的版本进行选择安装。
* [M2Crypto](https://pypi.org/project/M2Crypto/)
* [guacamole/guacd](https://hub.docker.com/r/guacamole/guacd):guacd is the native server-side proxy used by the Apache Guacamole web application.
* [pydeep](https://pydeep.readthedocs.io/en/latest/welcome.html):PyDeep is a machine learning / deep learning library with focus on unsupervised learning. 
```
# install python libraries
$ sudo apt-get install python python-pip python-dev libffi-dev libssl-dev
$ sudo apt-get install python-virtualenv python-setuptools
$ sudo apt-get install libjpeg-dev zlib1g-dev swig
$ sudo apt-get install mongodb
$ sudo apt-get install postgresql libpq-dev
$ sudo apt-get install qemu-kvm libvirt-bin ubuntu-vm-builder bridge-utils python-libvirt
$ sudo pip install XenAPI
# 以上步骤发现官方指南安装的依赖不够，所有本次实验要用的依赖：
sudo apt-get install git mongodb libffi-dev build-essential python-django python python-dev python-pip python-pil python-sqlalchemy python-bson python-dpkt python-jinja2 python-magic python-pymongo python-gridfs python-libvirt python-bottle python-pefile python-chardet tcpdump -y

# install virtual software
$ echo deb http://download.virtualbox.org/virtualbox/debian xenial contrib | sudo tee -a /etc/apt/sources.list.d/virtualbox.list
$ wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo apt-key add -
$ sudo apt-get update
$ sudo apt-get install virtualbox-5.1

# install Tcpdump
sudo apt-get install tcpdump apparmor-utils
sudo aa-disable /usr/sbin/tcpdump
# to make sure it is correctly installed 
sudo setcap cap_net_raw,cap_net_admin=eip /usr/sbin/tcpdump
getcap /usr/sbin/tcpdump
# right output:
# /usr/sbin/tcpdump = cap_net_admin,cap_net_raw+eip

# install Volatility(optional and not be installed this time)
sudo pip install openpyxl ujson pycrypto distorm3 pytz
git clone https://github.com/volatilityfoundation/volatility.git
cd volatility
python setup.py build
python setup.py install
# 确认volatility安装无误
python vol.py -h
# Output:Volatility Foundation Volatility Framework 2.6.1

# install M2Crypto(optional)
$ sudo apt-get install swig
$ sudo pip install m2crypto==0.24.0

# install guacd(optional)
$ sudo apt install libguac-client-rdp0 libguac-client-vnc0 libguac-client-ssh0 guacd

# install pydeep
wget http://sourceforge.net/projects/ssdeep/files/ssdeep-2.13/ssdeep-2.13.tar.gz/download -O ssdeep-2.13.tar.gz
tar -zxf ssdeep-2.13.tar.gz
cd ssdeep-2.13
./configure
make
sudo make install
# 确认pydeep安装无误：
#检查版本
ssdeep -V 
#再安装一次看看会不会提示已安装
pip show pydeep  
# output:2.13
```
volatility版本信息
![](images/volatility-ok.png)
pydeep版本：  
![](images/pyseep-version.png)  
2. 安装cuckoo
* 第一次直接安装很顺畅，第二次使用官网推荐的(可选但推荐就试了试)虚拟机内安装，安装后出现太多报错。无奈之后很多次报错，最后只好直接安装。
* [KVM](https://help.ubuntu.com/community/KVM)
```
# 如果没有安装依赖，安装以下依赖
sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk

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
第一次启动cuckoo看到如下页面说明安装成功,版本是2.0.7,CWD目录为'home/mudou/.cuckoo'.

* CWD的具体路径默认是在当前用户目录下 ~/.cuckoo.配置文件在$CWD/conf目录下,CWD的具体路径可更改。

![](images/setup-ok.png)   
第二次启动cuckoo,看到如下'报错'，是正常的因为我们还没有配置相关的文件。  
![](images/cuckoo-second.png) 
3. 更改配置文件  
修改cuckoo.conf
```
cd ~/.cuckoo/conf
sudo vim cuckoo.conf

# 确保以下内容:
# This option defines which Machinery module you want Cuckoo to use to interact with your analysis machines. The value must be the name of the module without extension (e.g., virtualbox or vmware).
[cuckoo]
machinery = virtualbox
```
![](images/define-machinery.png)

4.
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
4. 第二次安装了虚拟机后启动cuckoo出现了:  
'Vulnerable dependencies found
--> Vulnerable version of virtualbox installed (5.1.38). It is highly recommended to update. Please update and restart Cuckoo. Recommended version: >=5.2.28'  
![](images/wrong4.png)  
解决：[Cuckoo Sandbox 2.0.7](https://cuckoosandbox.org/blog/207-interim-release/) 
进入到工作目录下修改配置文件cuckoo.conf:  
![](images/wrong6.png)  
设置ignore_vulnerabilities = yes  
![](images/wrong5.png)  
出现报错'CuckooCriticalError: Unable to bind ResultServer'  
![](images/wrong8.png)  
参考[FAQ](https://cuckoo.sh/docs/faq/#troubles-problem),执行：  
```
# If the hostonly interface vboxnet0 does not exist already.
$ VBoxManage hostonlyif create

# Configure vboxnet0.
$ VBoxManage hostonlyif ipconfig vboxnet0 --ip 192.168.56.1 --netmask 255.255.255.0
```
启动,出现报错'CuckooCriticalError: Please update your configuration.'：  
![](images/wrong7.png)
但是出现这样的错误是因为此时还没有修改配置文件进行修改，并不是真的错。
## 实验总结
1. cuckoo configuration files
* ~/.cuckoo/conf/
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