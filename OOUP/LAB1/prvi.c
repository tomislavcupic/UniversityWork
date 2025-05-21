#include <stdio.h>
#include <stdlib.h>

typedef char const* (*PTRFUN)();

struct Animal {
   char* name;
   PTRFUN* functions;
};

char const* dogGreet(void) {
   return "vau!";
}

char const* dogMenu(void) {
   return "kuhanu govedinu";
}

char const* catGreet(void) {
   return "mijau!";
}

char const* catMenu(void) {
   return "konzerviranu tunjevinu";
}

void animalPrintGreeting(struct Animal* animal) {
   printf("%s pozdravlja: %s\n", animal->name, animal->functions[0]());
}

void animalPrintMenu(struct Animal* animal) {
   printf("%s voli %s\n", animal->name, animal->functions[1]());
}

void constructDog(struct Animal* animal, char* name) {
   animal->name = name;
   animal->functions = (PTRFUN*)malloc(2 * sizeof(PTRFUN));
   animal->functions[0] = &dogGreet;
   animal->functions[1] = &dogMenu;
}

void constructCat(struct Animal* animal, char* name) {
   animal->name = name;
   animal->functions = (PTRFUN*)malloc(2 * sizeof(PTRFUN)); 
   animal->functions[0] = &catGreet;
   animal->functions[1] = &catMenu;
}

struct Animal* createDog(char* name) {
   struct Animal* dog = (struct Animal*)malloc(sizeof(struct Animal));
   constructDog(dog, name);
   return dog;
}

struct Animal* createCat(char* name) {
   struct Animal* cat = (struct Animal*)malloc(sizeof(struct Animal));
   constructCat(cat, name);
   return cat;
}

struct Animal** createNDogs(int n) {
   struct Animal** dogs = (struct Animal**)malloc(n * sizeof(struct Animal*));
   for (int i = 0; i < n; ++i) {
      dogs[i] = (struct Animal*)malloc(sizeof(struct Animal));
      constructDog(dogs[i], "Dog");
   }
   return dogs;
}

void testAnimals(void) {
   struct Animal* p1 = createDog("Hamlet");
   struct Animal* p2 = createCat("Ofelija");
   struct Animal* p3 = createDog("Polonije");

   struct Animal dog;
   constructDog(&dog, "Hamlet");
   animalPrintGreeting(p1);
   animalPrintGreeting(p2);
   animalPrintGreeting(p3);
   animalPrintMenu(p1);
   animalPrintMenu(p2);
   animalPrintMenu(p3);

   animalPrintGreeting(&dog);
   animalPrintMenu(&dog);
   free(p1); 
   free(p2); 
   free(p3);
}

int main() {
   testAnimals();
   printf("\n");
   int n = 3;
   struct Animal** dogs = createNDogs(n);
   for (int i = 0; i < n; ++i) {
      animalPrintGreeting(dogs[i]);
      animalPrintMenu(dogs[i]);
      free(dogs[i]);
   }
   free(dogs);
   return 0;
}