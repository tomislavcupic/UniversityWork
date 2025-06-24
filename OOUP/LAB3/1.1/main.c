#include "myfactory.h"
#include "animal.h"
#include <stdio.h>
#include <stdlib.h>

void animalPrintGreeting(struct Animal* animal) {
  if (animal && animal->vtable && animal->vtable[0]) {
    printf("%s says: %s\n", animal->vtable[0](animal), animal->vtable[1](animal));
  } else {
    printf("Animal is NULL or vtable is not properly initialized.\n");
  }
}

void animalPrintMenu(struct Animal* animal) {
  if (animal && animal->vtable && animal->vtable[2]) {
    printf("%s eats: %s\n", animal->vtable[0](animal), animal->vtable[2](animal));
  } else {
    printf("Animal is NULL or vtable is not properly initialized.\n");
  }
}

int main(int argc, char *argv[]){
  for (int i=0; i<argc/2; ++i){
    struct Animal* p=(struct Animal*)myfactory(argv[1+2*i], argv[1+2*i+1]);
    if (!p){
      printf("Creation of plug-in object %s failed.\n", argv[1+2*i]);
      continue;
    }

    animalPrintGreeting(p);
    animalPrintMenu(p);
    free(p); 
  }
  return 0;
}