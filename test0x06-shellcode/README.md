# shellcode

## 实验要求
- [] 1、详细阅读 www.exploit-db.com 中的shellcode。建议找不同功能的，不同平台的 3-4个shellcode解读。
- [] 2、修改示例代码的shellcode，将其功能改为下载执行。也就是从网络中下载一个程序，然后运行下载的这个程序。提示：Windows系统中最简单的下载一个文件的API是 UrlDownlaodToFileA
* 其中第二个作业，原参考代码只调用了一个API函数，作业要求调用更多的API函数了，其中涉及到的参数也更复杂，但是原理是相通的。
* URLDownloadToFileA函数在 Urlmon.dll 这个dll中，这个dll不是默认加载的，所以可能还需要调用LoadLibrary函数
## 实验步骤
### 实验一
#### shellcode示例1-linux-64位  
功能：Kill All Processes   
[shellcode-1来源](https://www.exploit-db.com/shellcodes/46492)
##### 实验环境
虚拟机：kali 64位  
物理机：win10
##### 实验步骤
1. scp拷贝shell-test.c文件到kali中  
2. 将shell-test.c编译链接成可执行文件```gcc -fno-stack-protector -z execstack shell-test.c -o shell-test```
3. 执行：```./shell-test```
##### 实验效果
![](video/kali64-shellcode.gif)
##### shellcode解读
* rax rbx rcx rdx：通用寄存器（注意 a, b, c, d）。rdi rsi：d 和 s 分别表示 “destination” 和 “source”，不过现在已经没有意义了。
* 在 Linux 使用的 System V 二进制接口中：前 6 个参数通过寄存器传参。函数的返回值则通过 rax 寄存器返回。当函数调用发生时，整型变量/指针按照如下顺序通过寄存器传递：rdi, rsi, rdx, rcx（后来换成了r10）, r8, r9。每个系统调用都有一个整数标识符。
* 在不同平台上，系统调用的编号可能不同。不过，在 Linux 中，这些标识符是永远不会变的。因此汇编代码中'push 0x3e'和'push	0x9'能够很明确地分别表示'sys kill'和'sig kill'。然后不断用rax、rdi、rsi来传递pid,依次pop出栈。
* 最后使用'syscall'指令向系统内核发起系统调用请求。
![](images/shellcode1.png)
C代码及分析如下：  
```
#include<stdio.h>
#include<string.h>
unsigned char code[] = \
"\x6a\x3e\x58\x6a\xff\x5f\x6a\x09\x5e\x0f\x05";
main()
{
printf("Shellcode Length:  %d\n", (int)strlen(code));//打印输出该shellcode的长度
int (*ret)() = (int(*)())code;//使用函数指针将code的地址赋给ret()，然后调用
ret();
}
```
>完整汇编及C代码存于code/shellcode-1.txt
#### shellcode示例2-linux-32位
功能：  
[shellcode-2来源]()
##### 实验环境
##### 实验步骤
##### 实验效果
##### shellcode解读
>完整汇编及C代码存于code/shellcode-2.txt
#### shellcode示例3-win-32位
功能：打开cmd.exe   
[shellcode-3来源](https://www.exploit-db.com/shellcodes/39900)
##### 实验环境
虚拟机：xp-sp3-32位  
物理机：win10
##### 实验步骤
1. 将汇编语言保存为winexec.asm,然后使用下列命令编译链接：  
```
# linux系统中使用
nasm -f win32 winexec.asm -o exec.obj
# vs命令行中使用
ld.exe -o winexec.exe exec.obj
```
2. xp-sp3中执行winexec.exe
##### 实验效果
![](video/xp32-shellcode.gif)
##### shellcode解读-win-64位
1. 加载PEB找kernel32.dll基地址  
![](images/3-1.png)  
2. 找kernel32.dll导出表
![](images/3-2.png)  
3. 在导出表中找到GetProcAddress()函数的名字  
![](images/3-3.png)  
4. 找到GetProcAddress()函数的地址  
![](images/3-4.png) 
5. 保存GetProcAddress()的地址和kernel32.dll的地址，以及找到Winexe()的地址  
![](images/3-5.png)  
6. 结束进程  
![](images/3-6.png)   
>完整汇编及C代码存于code/shellcode-3.txt

#### shellcode示例4
功能： 
[shellcode-4来源]()
##### 实验环境

##### 实验步骤

##### 实验效果

##### shellcode解读

>完整汇编及C代码存于code/shellcode-4.txt
### 实验二
#### 实验要求
修改[示例shellcode](https://www.exploit-db.com/shellcodes/48116),使其下载运行某个程序
[shellcode来源](https://www.exploit-db.com/shellcodes/24318)
#### 实验步骤
#### 实验效果

## 实验问题

## 实验总结
1. 经过此次实验作业，加深了对汇编语言的理解，首先是AT&T与Intel风格的汇编语言:  
DOS/Windows 下的汇编语言代码都是 Intel 风格的，而 Linux 和 Unix 系统中更多采用的是 AT&T 格式。  
2. shellcode示例C代码中多次使用到了函数指针。函数指针值得学习：  
[深入理解C语言函数指针](https://www.cnblogs.com/windlaughing/archive/2013/04/10/3012012.html)和[深入浅出——理解c/c++函数指针](https://zhuanlan.zhihu.com/p/37306637)  
函数指针学习总结： 
* 函数指针：将函数的首地址存储在某个函数指针变量中，被存储地址的函数指针称为函数指针常量，被赋予函数指针的称为函数指针变量，从而使两个不同函数名的函数拥有相同的函数调用效果。通俗地理解，就是将一个函数的首地址通过指针进行传参来调用。
* 函数指针变量跟普通的指针一样在32位系统下大小都为4。但是函数指针常量的大小为1.
* 函数指针变量和函数指针常量存储在内存的不同位置。
* 为负值的函数指针变量（全局）的值为0
* 函数指针同样要求返回值匹配和参数匹配
## 参考文献
[www.exploit-db.com 中的shellcode](https://www.exploit-db.com/shellcodes)  
[!peb](https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/-peb)  
[PEB结构学习](https://www.cnblogs.com/binlmmhc/p/6501545.html)  
[PEB structure](https://docs.microsoft.com/en-us/windows/win32/api/winternl/ns-winternl-peb)  
[Process Environment Block](https://en.wikipedia.org/wiki/Process_Environment_Block)  
[汇编语言--Linux 汇编语言开发指南](https://zhuanlan.zhihu.com/p/54853591)  
[Raw Linux Threads via System Calls](https://nullprogram.com/blog/2015/05/15/)  
[URLDownloadToFile function](https://docs.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/platform-apis/ms775123(v=vs.85)?redirectedfrom=MSDN)