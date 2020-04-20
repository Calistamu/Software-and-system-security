# 内存管理

## 实验要求
- [x] 阅读[VirtualAlloc](https://docs.microsoft.com/zh-cn/windows/win32/api/memoryapi/nf-memoryapi-virtualalloc)、[VirtualFree](https://docs.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualfree)、[VirtualProtect](https://docs.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualprotect)等函数的官方文档。
- [x] 编程使用malloc分配一段内存，测试是否这段内存所在的整个4KB都可以写入读取。
- [x] 使用VirtualAlloc分配一段，可读可写的内存，写入内存，然后将这段内存改为只读，再读数据和写数据，看是否会有异常情况。然后VirtualFree这段内存，再测试对这段内存的读写释放正常。

## 实验步骤
### 一、malloc分配一段内存
实验代码如下：
* CHAR 类型数据占 1 个字节，4KB 为 4096 个字节
```
#include<iostream>
using namespace std;
int cnt = 0;
int main()
{
	char* a = (char*)malloc(100);
	int write_num = 0, read_num = 0;
	for (int i = 0; i < 4095; i++)
	{		a[i] = i;
	write_num++;
}
	cout << "可写入字节数：" << write_num << endl;
	for (int i = 0; i < 4095; i++)
		if (a[i] == i)
			read_num++;
	cout << "可读取字节数：" << read_num << endl;
	return 0;
}
```
1. 如果字节数大于4096，无法正常运行，既不能写入，也不能读取。
* 如果字节数在已分配的长度内，可以成功运行，且读写长度一致，很好理解，在这里就不列出示例。
![](images/wrong-4.png)
调试时出现了溢出报错。这是因为我们写入和读取的长度超过了基本管理单元4KB，判定为无效。
![](images/wrong-1.png)
2. 如果字节数刚好等于4096或小于4096，可以正常运行，可以写入，也可以读取，但写入字节数和读取字节数不一样。
![](images/wrong-2.png)
这是因为我们只分配了100字节，写入时出现了堆损坏报错，写入时超出了已分配的长度，覆盖了多余的内存因此读取为128字节。
![](images/wrong-3.png)
3. 结论：经过实验，加深了对“以4KB（页）作为基本管理单元的虚拟内存管理”的理解。
### 二、VirtualAlloc分配内存
实验代码：  
>code/virtualtry.cpp
1. 使用VirtualAlloc分配一段可读可写的内存
* 参考[Memory Protection Constants](https://docs.microsoft.com/zh-cn/windows/win32/memory/memory-protection-constants)  
结果如下图所示：  
![](images/virtualalloc.png)
2. 用VirtualProtect修改内存为只读  
![](images/readonly.png)
3. VirtualFree该段内存,再对这段内存进行读写，得到结果：异常退出,结果如下图所示  
![](images/virtualfree.png)  
## 实验总结
经过此次实验明白：内存的有效性和访问属性，都是以4Kb为单位的，访问属性在分配内存时可以设置。
## 参考文献
[VirtualAlloc](https://docs.microsoft.com/zh-cn/windows/win32/api/memoryapi/nf-memoryapi-virtualalloc)  
[VirtualFree](https://docs.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualfree)  
[VirtualProtect](https://docs.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualprotect)  
[Memory Protection Constants](https://docs.microsoft.com/zh-cn/windows/win32/memory/memory-protection-constants)