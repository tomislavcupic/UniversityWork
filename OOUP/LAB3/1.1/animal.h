#ifndef ANIMAL_H
#define ANIMAL_H

typedef char const* (*PTRFUN)();

struct Animal {
    PTRFUN* vtable;
};

#endif /* ANIMAL_H */
