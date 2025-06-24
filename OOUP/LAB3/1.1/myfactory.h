#ifndef MYFACTORY_H
#define MYFACTORY_H

#include <stddef.h>

void* myfactory(char const* libname, char const* ctorarg);
size_t sizeof_object(char const* libname);
void construct_object(char const* libname, void* ptr, char const* ctorarg);

#endif /* MYFACTORY_H */
