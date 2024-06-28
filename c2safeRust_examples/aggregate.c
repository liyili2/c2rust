#include <stdio.h>
#include <stdlib.h>

int* aggregate(int* list, int len) {
    int* ret = malloc(sizeof(int) * ((len >> 1) + (len & 0b0001)));
    for (int i = 0; i < len; i++) {
        if (i % 2) {
            ret[i/2] = ret[i/2] + list[i];
        } else {
            ret[i/2] = list[i];
        }
    }
    return ret;
}

void printall(int* list, int len) {
    printf("[");
    for (int i = 0; i < len; i++) {
        printf("%d, ", list[i]);
    }
    printf("]\n");
}

int main(int argc, char* argv[]) {
    int test1[] = {1,2,3,4,5,6};
    int* ret1 = aggregate(test1, 6);
    printall(test1, 6);
    printall(ret1, 3);
    free(ret1);
    int test2[] = {1,2,3,4,5};
    int* ret2 = aggregate(test2, 5);
    printall(test2, 5);
    printall(ret2, 3);
    free(ret2);
    return 0;
}