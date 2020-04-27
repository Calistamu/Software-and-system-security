# shellcode

## 实验要求
- [] 1、详细阅读 www.exploit-db.com 中的shellcode。建议找不同功能的，不同平台的 3-4个shellcode解读。
- [] 2、修改示例代码的shellcode，将其功能改为下载执行。也就是从网络中下载一个程序，然后运行下载的这个程序。提示：Windows系统中最简单的下载一个文件的API是 UrlDownlaodToFileA
* 其中第二个作业，原参考代码只调用了一个API函数，作业要求调用更多的API函数了，其中涉及到的参数也更复杂，但是原理是相通的。
* URLDownloadToFileA函数在 Urlmon.dll 这个dll中，这个dll不是默认加载的，所以可能还需要调用LoadLibrary函数
## 实验步骤
### 实验一
#### shellcode示例1

#### shellcode示例2

#### shellcode示例3

#### shellcode示例4

## 实验问题

## 实验总结

## 参考文献
[www.exploit-db.com 中的shellcode](https://www.exploit-db.com/shellcodes)  
[!peb](https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/-peb)  
[PEB结构学习](https://www.cnblogs.com/binlmmhc/p/6501545.html)  
[PEB structure](https://docs.microsoft.com/en-us/windows/win32/api/winternl/ns-winternl-peb)  
[Process Environment Block](https://en.wikipedia.org/wiki/Process_Environment_Block)