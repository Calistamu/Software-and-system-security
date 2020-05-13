# KLEE

## 实验要求
- [x]安装KLEE
- []完成官方tutorials
## 实验环境
ubuntu 18.04 server
## 实验步骤
1.安装Docker Engine - Enterprise
```
1.设置仓库
# 更新 apt 包索引。
$ sudo apt-get update
# 安装 apt 依赖包，用于通过HTTPS来获取仓库:
$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
# 添加 Docker 的官方 GPG 密钥：
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
# 得到9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88 通过搜索指纹的后8个字符，验证您现在是否拥有带有指纹的密钥。
$ sudo apt-key fingerprint 0EBFCD88    
pub   rsa4096 2017-02-22 [SCEA]
      9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88
uid           [ unknown] Docker Release (CE deb) <docker@docker.com>
sub   rsa4096 2017-02-22 [S]
# 使用以下指令设置稳定版仓库
$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) \
  stable"

2. 安装 Docker Engine-Community
# 更新 apt 包索引。
$ sudo apt-get update
# 安装最新版本的 Docker Engine-Community 和 containerd ，或者转到下一步安装特定版本：
$ sudo apt-get install docker-ce docker-ce-cli containerd.io
# 列出您的仓库中可用的版本：
$ apt-cache madison docker-ce
# 这里直接安装，没有指定序列号
$ sudo apt-get install docker-ce 
测试 Docker 是否安装成功
$ sudo docker run hello-world
```
当前docker版本信息如下图：  
![](images/docker-version.png)  
2. 安装klee和基本使用
```
# Pulling from the Docker Hub
$ docker pull klee/klee:2.0

# Building the Docker image locally
$ git clone https://github.com/klee/klee.git
$ cd klee
$ docker build -t klee/klee 

# Creating a KLEE Docker container
# --ulimit option sets an unlimited stack size inside the container. This is to avoid stack overflow issues when running KLEE.
docker run --rm -ti --ulimit='stack=-1:-1' klee/klee
```
klee版本信息如下图：  
![](images/klee-version.png)  
```
# Persistent Containers
docker run -ti --name=my_first_klee_container --ulimit='stack=-1:-1' klee/klee
```
```
klee@1fd39056dfa5:~$ pwd
/home/klee
klee@1fd39056dfa5:~$ echo "int main(int argn, char** argv) { return 0; }" > test.c
klee@1fd39056dfa5:~$ clang -emit-llvm -g -c test.c -o test.bc
klee@1fd39056dfa5:~$ klee --libc=uclibc --posix-runtime test.bc
KLEE: NOTE: Using POSIX model: /tmp/klee_build60stp_z3/Debug+Asserts/lib/libkleeRuntimePOSIX.bca
KLEE: NOTE: Using klee-uclibc : /tmp/klee_build60stp_z3/Debug+Asserts/lib/klee-uclibc.bca
KLEE: output directory is "/home/klee/klee-out-0"
KLEE: Using STP solver backend
warning: Linking two modules of different target triples: test.bc' is 'x86_64-unknown-linux-gnu' whereas '__uClibc_main.os' is 'x86_64-pc-linux-gnu'
KLEE: WARNING ONCE: calling external: syscall(16, 0, 21505, 47460912) at /tmp/klee_src/runtime/POSIX/fd.c:980 10
KLEE: WARNING ONCE: calling __user_main with extra arguments.
KLEE: WARNING ONCE: Alignment of memory from call "malloc" is not modelled. Using alignment of 8.
KLEE: done: total instructions = 13174
KLEE: done: completed paths = 1
KLEE: done: generated tests = 1
klee@1fd39056dfa5:~$ ls
klee-last  klee-out-0  klee_build  klee_src  test.bc  test.c
klee@1fd39056dfa5:~$ exit
```
使用命名的方式很明显看到确实多了一个docker image  
![](images/named-image.jpg)  
```
# restart the container
docker start -ai my_first_klee_container
# remove
docker rm my_first_klee_container
```
删除docker image前后对比   
![](images/delete-image.png)  
3. 
## 实验问题
1. 安装docker-ce时指定版本出错  
![](images/wrong1.png)    
解决：不指定序列号，直接安装。  
2. 创建klee的docker镜像出错
![](images/wrong2.png)  
解决：[解决办法](https://www.digitalocean.com/community/questions/how-to-fix-docker-got-permission-denied-while-trying-to-connect-to-the-docker-daemon-socket)，详细如下：  
```
# Create the docker group.
sudo groupadd docker
# Add your user to the docker group.
sudo usermod -aG docker ${USER}
Y# ou would need to loog out and log back in so that your group membership is re-evaluated or type the following command:
su -s ${USER}
# Verify that you can run docker commands without sudo.
docker run hello-world
```
## 实验结论
## 参考文献
[klee-tutorials](https://klee.github.io/tutorials/testing-function/)
[Get Docker Engine - Enterprise for Ubuntu](https://docs.docker.com/ee/docker-ee/ubuntu/)
[Using KLEE with Docker](https://klee.github.io/docker/)