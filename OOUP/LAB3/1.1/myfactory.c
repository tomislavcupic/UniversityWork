#include "myfactory.h"
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

void* myfactory(char const* libname, char const* ctorarg) {
   HINSTANCE hDll;
   void* (*create)(char const*);

   hDll = LoadLibrary(libname);
   if (!hDll) {
      fprintf(stderr, "Error opening library: %lu\n", GetLastError());
      return NULL;
   }

   create = (void* (*)(char const*))GetProcAddress(hDll, "create");
   if (!create) {
      fprintf(stderr, "Error loading symbol: %s\n", GetLastError());
      FreeLibrary(hDll);
      return NULL;
   }

   return create(ctorarg);
}

size_t sizeof_object(char const* libname) {
   HINSTANCE hDll;
   size_t (*get_size)();
   size_t size = 0;

   hDll = LoadLibrary(libname);
   if (!hDll) {
      fprintf(stderr, "Error opening library: %lu\n", GetLastError());
      return 0;
   }

   // Učitaj funkciju "get_size" iz biblioteke
   get_size = (size_t (*)())GetProcAddress(hDll, "sizeof_object");
   if (!get_size) {
      fprintf(stderr, "Error loading symbol: %s\n", GetLastError());
      FreeLibrary(hDll);
      return 0;
   }

   size = get_size();
   FreeLibrary(hDll);
   return size;
}

void construct_object(char const* libname, void* ptr, char const* ctorarg) {
   HINSTANCE hDll;
   void (*construct)(void*, char const*);

   hDll = LoadLibrary(libname);
   if (!hDll) {
      fprintf(stderr, "Error opening library: %lu\n", GetLastError());
      return;
   }

   construct = (void (*)(void*, char const*))GetProcAddress(hDll, "construct");
   if (!construct) {
      fprintf(stderr, "Error loading symbol: %s\n", GetLastError());
      FreeLibrary(hDll);
      return;
   }

   construct(ptr, ctorarg);
   FreeLibrary(hDll);
}