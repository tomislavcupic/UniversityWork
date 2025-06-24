#include "animal.h"
#include <stdlib.h>

typedef struct {
    struct Animal base;
    char* name;
} Parrot;

char const* parrotName(void* this) {
    return ((Parrot*)this)->name;
}

char const* parrotGreet() {
    return "Hello!";
}

char const* parrotMenu() {
    return "Seeds";
}

PTRFUN parrotVTable[3] = {parrotName, parrotGreet, parrotMenu};

__declspec(dllexport) void* create(char const* name) {
    Parrot* parrot = (Parrot*)malloc(sizeof(Parrot));
    parrot->base.vtable = parrotVTable;
    parrot->name = strdup(name);
    return parrot;
}

__declspec(dllexport) size_t sizeof_object() {
    return sizeof(Parrot);
}

__declspec(dllexport) void construct(void* ptr, char const* name) {
    Parrot* parrot = (Parrot*)ptr;
    parrot->base.vtable = parrotVTable;
    parrot->name = strdup(name);
}
