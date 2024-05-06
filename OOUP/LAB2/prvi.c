#include <string.h>
#include <stdio.h>

const void* mymax(const void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *)) {
    const void *max_element = base;
    for (size_t i = 1; i < nmemb; i++) {
        const void *element = (const char*)base + i * size;
        if (compar(element, max_element)) {
            max_element = element;
        }
    }
    return max_element;
}

int gt_int(const void *a, const void *b) {
    return (*(int*)a > *(int*)b);
}

int gt_char(const void *a, const void *b) {
    return (*(char*)a > *(char*)b);
}
    
int gt_str(const void *a, const void *b) {
    return (strcmp(*(const char**)a, *(const char**)b) > 0);
}

int main(){
    int arr_int[] = { 1, 3, 5, 7, 4, 6, 9, 2, 0 };
    char arr_char[]="Suncana strana ulice";
    const char* arr_str[] = {
        "Gle", "malu", "vocku", "poslije", "kise",
        "Puna", "je", "kapi", "pa", "ih", "njise"
    };

    int *max_int = (int*)mymax(arr_int, sizeof(arr_int) / sizeof(int), sizeof(int), gt_int);
    char *max_char = (char*)mymax(arr_char, strlen(arr_char), sizeof(char), gt_char);
    const char **max_str = (const char**)mymax(arr_str, sizeof(arr_str) / sizeof(char*), sizeof(char*), gt_str);
    printf("max_int = %d\n", *max_int);
    printf("max_char = %c\n", *max_char);
    printf("max_str = %s\n", *max_str);
    return 0;
}