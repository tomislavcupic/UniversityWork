#include "animal.h"
#include <stdlib.h>
#include <string.h>

typedef struct {
    struct Animal base;
    char* name;
} Tiger;

char const* tigerName(void* this) {
    return ((Tiger*)this)->name;
}

char const* tigerGreet() {
    return "Roar!";
}

char const* tigerMenu() {
    return "Meat";
}

PTRFUN tigerVTable[3] = {tigerName, tigerGreet, tigerMenu};

__declspec(dllexport) void* create(char const* name) {
    Tiger* tiger = (Tiger*)malloc(sizeof(Tiger));
    tiger->base.vtable = tigerVTable;
    tiger->name = strdup(name);
    return tiger;
}

__declspec(dllexport) size_t sizeof_object() {
    return sizeof(Tiger);
}

__declspec(dllexport) void construct(void* ptr, char const* name) {
    Tiger* tiger = (Tiger*)ptr;
    tiger->base.vtable = tigerVTable;
    tiger->name = strdup(name);
}
