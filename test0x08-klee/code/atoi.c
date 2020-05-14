#include<klee/klee.h>
#include<stdio.h>
#include<assert.h>
int main(int argc, char* argv[]) {
        int input = atoi(argv[1]);
        return input;
    }