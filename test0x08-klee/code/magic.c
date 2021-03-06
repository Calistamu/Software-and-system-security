#include<stdio.h>
#include <assert.h>
#include <klee/klee.h>
int magic_computation(int input) {
    for (int i = 0; i < 32; ++i)
        input ^= 1 << i;
    return input;
}
int main(int argc, char* argv[]) {
        int input, result;
        klee_make_symbolic(&input, sizeof(int), "input");
        result = magic_computation(input);
        if (result == 253)
            klee_assert(0);
        return 0;
    }
