# 内存管理2
## 实验要求
1、验证不同进程的相同的地址可以保存不同的数据。
- [x] （1）在VS中，设置固定基地址，编写两个不同可执行文件。同时运行这两个文件。然后使用调试器附加到两个程序的进程，查看内存，看两个程序是否使用了相同的内存地址。
- [x] （2）在不同的进程中，尝试使用VirtualAlloc分配一块相同地址的内存，写入不同的数据。再读出。
2、（难度较高）配置一个Windbg双机内核调试环境，查阅Windbg的文档，了解以下内容：
- [] （1）Windbg如何在内核调试情况下看物理内存，也就是通过物理地址访问内存。
- [] （2）如何查看进程的虚拟内存分页表，在分页表中找到物理内存和虚拟内存的对应关系。然后通过Windbg的物理内存查看方式和虚拟内存的查看方式，看同一块物理内存中的数据情况。
## 实验步骤
### 1、验证不同进程的相同的地址可以保存不同的数据
#### 1.1 两个不同可执行文件，设置相同固定及地址，看两个程序是否使用了相同的内存地址
1. 如下图进行基地址设置
![](images/set-address.png)
2. 如下图是本次实验的代码，让其大致相同。
![](images/samecode.png)
3. 看到结果，两个程序确实使用了相同的内存地址
![](images/samestart.png)
4. 总结：同时运行却能使用相同的地址，是因为使用的是虚拟地址，映射于不同的物理地址。
#### 1.2 使用VirtualAlloc分配一块相同地址的内存，写入不同的数据，再读出。
代码及实验结果如下图所示，确实可以使用VirtualAlloc在相同的内存地址写入不同的数据，同样使用的是虚拟映射的原理。
![](images/save-sameaddr.png)
### 2. 配置一个Windbg双机内核调试环境
#### 实验环境
物理机(Host):已安装windbg  
虚拟机(Guest):使用win7-64位系统
#### 2.0 实验准备：配置内核调试
1. Guest端：虚拟机串口设置如下图  
![](images/serialports.png)
2. Guest端：启动虚拟机，进入Window内部进行配置。以管理员身份启动CMD,输入以下命令。
* DebugEntry的方式启动win7
```
    bcdedit /dbgsettings serial baudrate:115200 debugport:1
    bcdedit /copy {current} /d DebugEntry
    bcdedit /displayorder {current} {替换第二个命令显示的UUID}
    bcdedit /debug {替换第二个命令显示的UUID} on
```
运行结果如下图：  
![](images/cmd.png)
3. Host:配置windbg符号下载地址  
![](images/symbols-path.png)
4. Host进入windbg.exe所在文件夹，以下命令启动windbg  
```windbg.exe -k com:port=\\.\pipe\com_1,baud=115200,pipe```  
在显示'Waiting ro reconnect......'之后下断点，成功连接  
![](images/windbg-ok.png)   
输入```!process 0 0```，显示出系统中的进程信息  
![](images/process-info.png)
#### 2.1 Windbg如何在内核调试情况下通过物理地址访问内存
1. 


#### 2.2 查看进程的虚拟内存分页表，在分页表中找到物理内存和虚拟内存的对应关系然后通过Windbg的物理内存查看方式和虚拟内存的查看方式，看同一块物理内存中的数据情况。

## 实验问题
1. 在guest串口设置后启动时出现如下图报错  
![](images/wrong1.png)  
解决：Pipe名写错了，改对即可。
2. Host打开windbg的时候一直reconnect
![](images/wrong2.png)
解决：一直以为是串口配置错误，还研究了很久想找到boot.ini，最后在waiting reconnect的时候下断点解决。
## 实验总结

## 参考文献
[VirtualAlloc function](https://docs.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualalloc)  
[Windows内核调试](https://zhuanlan.zhihu.com/p/47771088)
