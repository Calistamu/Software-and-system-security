# KLEE

## 实验要求
- [x]安装KLEE
- []完成官方tutorials
## 实验环境
ubuntu 18.04 server
## 实验步骤
* klee的安装有多种方式：  
![](images/install-klee.png)  
本次试验选用docker的方式。

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
clang版本信息如下图：  
![](images/clang-version.png) 
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
3. First tutorial: Testing a small function.  
```
# 启动klee
docker run -ti --name=my_first_klee_container --ulimit='stack=-1:-1' klee/klee
# 进入get_sign.c所在目录
cd klee_src/examples/get_sign/
# Compiling to LLVM bitcode
clang -I ../../include -emit-llvm -c -g -O0 -Xclang -disable-O0-optnone get_sign.c
# Running KLEE
klee get_sign.bc
# ls klee-last/
```
* -I参数，以便编译器可以找到klee/klee.h其中包含用于与KLEE虚拟机交互的内在函数的定义。
* -c是因为我们只想将代码编译成一个目标文件(而不是一个本机可执行文件)。
* -g导致将其他调试信息存储在目标文件中，KLEE将使用这些信息来确定源代码行号信息。
* -O0 -Xclang -disable-O0-optnone编译时不进行任何优化，但不阻止KLEE执行自己的优化，而使用-O0编译则会。

运行结果如下图：  
![](images/1-1.png)
查看测试结果,每一个测试文件包括调用的参数、符号对象、路径的数量(只有一个)、象征性的对象的名字(a)、它的大小(4)
* int占4字节

![](images/1-2.png)
4. Second tutorial: Testing a simple regular expression library.
```
cd klee_src/examples/regexp/

clang -I ../../include -emit-llvm -c -g -O0 -Xclang -disable-O0-optnone Regexp.c

klee --only-output-states-covering-new Regexp.bc
```
运行结果如下图：  
![](images/2-1.png)
klee总共执行了4848113条指令，探索了7438条路径，生成了16个测试用例。上图红色字样告诉我们23、25行出现了报错，因此查看报错信息。进入相应的output文件夹，可以看到是ptr（存储或加载无效的内存位置）错误，详细如下图所示：  
![](images/2-2.png)
分析：出现内存错误，不是因为正则表达式函数有一个错误，而是按时测试驱动程序有一个错误。因为输入的正则表达式序列完全是符号的，但是match函数期望它是一个以null结尾的字符串。  
解决：将' \0 '符号化后存储在缓冲区的末尾。如图进行修改：
* 也可以增加：klee_assume(re[SIZE - 1] == '\0'); 
* klee_assume接受一个参数(一个无符号整数)，该参数通常应该是某种条件表达式，并且“假定”该表达式在当前路径上为真(如果这种情况永远不会发生，即该表达式可证明为假，那么KLEE将报告错误)。
* klee_assume可以用来编码更复杂的约束。例如，我们可以使用klee_assume(re[0] != '^')使KLEE只探索第一个字节不是'^'的状态。像'&&'和'||'这样的布尔条件可能会被编译成在计算表达式结果之前进行分支的代码。在这种情况下，KLEE将在进程到达对klee_assume的调用之前对进程进行分支，这可能会导致探索不必要的附加状态。出于这个原因，最好使用尽可能简单的表达式来进行klee_assume(例如，将一个调用拆分为多个调用)，并使用'&'和'|'操作符，而不是短路操作符。

![](images/2-3.png) 
再次编译链接后运行，发现报错已解决。  
![](images/2-4.png)
5. tutorial 3:Solving a maze with KLEE
6. tutorial 4:
7. tutorial 5:
8. tutorial 6:
9. tutorial 7:
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
3. 【tutorial-1】编译链接.c文件时出现报错  
![](images/wrong3.png)  
解决：进错了目录，应该是'klee/examples/get_sign/',然后再编译链接。
4. 【tutorial-2】修改.c文件时，使用vi/vim报错，因为docker容器中vim无法使用  
![](images/wrong4.png)  
解决：```sudo apt-get update && sudo apt-get install vim```
## 实验结论
## 参考文献
[klee-tutorials](https://klee.github.io/tutorials/)
[Get Docker Engine - Enterprise for Ubuntu](https://docs.docker.com/ee/docker-ee/ubuntu/)
[Using KLEE with Docker](https://klee.github.io/docker/)
