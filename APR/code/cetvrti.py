import numpy as np
from matrica import Matrica
from cetvrti_algoritmi import *

# Funkcija 1: Rosenbrockova banana funkcija
def rosenbrock(X):
   return 100 * (X[1] - X[0]**2)**2 + (1 - X[0])**2

# Funkcija 2: Druga ciljna funkcija
def quadratic(X):
   return (X[0] - 4)**2 + 4 * (X[1] - 2)**2

# Implicitna ograničenja
def constraint1(X):
   return X[1] - X[0]  # x2 - x1 >= 0

def constraint2(X):
   return 2 - X[0]  # 2 - x1 >= 0

def main():
   Xd = [-100, -100]
   Xg = [100, 100]

   # Optimizacija za funkciju 1
   X0_f1 = [-1.9, 2]
   alg_f1 = BoxAlgorithm(rosenbrock, [constraint1, constraint2], Xd, Xg)
   X_opt_f1, F_opt_f1 = alg_f1.optimize(X0_f1)
   print("Funkcija 1: Optimizirana točka:", X_opt_f1)
   print("Funkcija 1: Vrijednost ciljne funkcije u optimiziranoj točki:", F_opt_f1)

   # Optimizacija za funkciju 2
   X0_f2 = [0.1, 0.3]
   alg_f2 = BoxAlgorithm(quadratic, [constraint1, constraint2], Xd, Xg)
   X_opt_f2, F_opt_f2 = alg_f2.optimize(X0_f2)
   print("Funkcija 2: Optimizirana točka:", X_opt_f2)
   print("Funkcija 2: Vrijednost ciljne funkcije u optimiziranoj točki:", F_opt_f2)

if __name__ == "__main__":
   main()