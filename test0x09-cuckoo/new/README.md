# cuckoo
## 实验要求
- [] 安装并使用cuckoo
- [] 任意找一个程序，在cuckoo中trace获取软件行为的基本数据。
## 实验环境
host：ubuntu 18.04 LTS  
guest: windows xp-sp3  
两个主机都是双网卡：NAT+host-only
## 实验步骤
1. 换源
```
sudo gedit /etc/apt/sources.list
# change as follows:
deb http://mirrors.aliyun.com/ubuntu/ disco main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ disco main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ disco-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ disco-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ disco-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ disco-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ disco-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ disco-backports main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ disco-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ disco-proposed main restricted universe multiverse
# 删除缓存：
sudo rm -vfr /var/lib/apt/lists/*
# 更新：
sudo apt-get update
sudo apt-get upgrade
```
## 实验问题
## 实验总结
## 参考文献