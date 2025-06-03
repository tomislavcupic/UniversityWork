import math
import numpy as np
import random
from drugi_algoritmi import *

class CiljnaFunkcija:
    def __init__(self):
        self.broj_evaluacija = 0
        #self.memo = {}

    def f(self, x):
        raise NotImplementedError("implementiraj funkciju cilja.")

    def povecaj_broj(self, x):
         self.broj_evaluacija += 1
    
    def evaluiraj(self, x):
       return self.f(x)

    def broj_evaluacija_funkcije(self):
        return self.broj_evaluacija

# Funkcija 1: Rosenbrockova funkcija
class Funkcija1(CiljnaFunkcija):
   def f(self, x):
      return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

# Funkcija 2
class Funkcija2(CiljnaFunkcija):
   def f(self, x):
      return (x[0] - 4)**2 + (x[1] - 2)**4

# Funkcija 3 (dimenzionalna)
class Funkcija3(CiljnaFunkcija):
   def __init__(self, n):
      super().__init__()
      self.n = n

   def f(self, x):
      return sum((i + 1 - xi)**2 for i, xi in enumerate(x))

# Funkcija 4: Jakobovićeva funkcija
class Funkcija4(CiljnaFunkcija):
   def f(self, x):
      return (x[0] - x[1])**2 + (x[0] + x[1])**2

# Funkcija 5 nije definisana, ali funkcija 6 jeste
class Funkcija6(CiljnaFunkcija):
   def f(self, x):
      return sum((np.sin(xi)**2 - 0.5) / (1 + 0.001 * (xi**2))**2 for xi in x)

# Funkcija za jednodimenzionalnu optimizaciju (f(x) = (x - 3)**2)
class JednodimenzionalnaFunkcija(CiljnaFunkcija):
   def f(self, x):
      if isinstance(x, float):
         x = [x]
      return (x[0] - 3)**2

def main():
   print("prvi zadatak:\n")
   # Primeri korišćenja sa jednostavnom funkcijom
   x0 = np.array([10.0])
   funkcija = JednodimenzionalnaFunkcija()
   minimum = optimizacija(funkcija, tocka=10.0, h=1.0, e=1e-6)
   print("Minimum je približno na x =", minimum)
   print("Broj evaluacija funkcije:", funkcija.broj_evaluacija_funkcije())
   minimum = KoordinatnoPretrazivanje(funkcija, x0, e=1e-6)
   print("Minimum je približno na x =", minimum[0])
   print("Broj evaluacija funkcije:", funkcija.broj_evaluacija_funkcije())
   minimum_nm = nelder_mead(funkcija, x0, alfa=1, beta=0.5, gama=2, sigma=0.5, epsilon=1e-6)
   print("Minimum je na x =", minimum_nm[0])
   print("Broj evaluacija funkcije:", funkcija.broj_evaluacija_funkcije())
   funkcija.broj_evaluacija = 0
   minimum_hj = hooke_jeeves(funkcija, x0, Dx=np.array([0.5]), e=np.array([1e-6]))
   print("Minimum je na x =", minimum_hj[0])
   print("Broj evaluacija funkcije:", funkcija.broj_evaluacija_funkcije())

   print("\nDrugi zadatak: \n")
   # Postavljanje parametara za funkcije 1-4
   f1 = Funkcija1()
   f2 = Funkcija2()
   f3 = Funkcija3(n=5)  # Funkcija 3 sa dimenzijom 5
   f4 = Funkcija4()

   # Pokretanje algoritama i beleženje broja evaluacija
   rezultati = []

   # Funkcija 1, početna točka [-1.9, 2]
   x0 = np.array([-1.9, 2.0])
   funkcija1_kp = KoordinatnoPretrazivanje(f1, x0, e=1e-6)
   rezultati.append(("Funkcija 1", "Koordinatno pretraživanje", f1.broj_evaluacija_funkcije(), funkcija1_kp))
   f1.broj_evaluacija = 0
   funkcija1_hj = hooke_jeeves(f1, x0, Dx=np.array([0.5, 0.5]), e=np.array([1e-6, 1e-6]))
   rezultati.append(("Funkcija 1", "Hooke-Jeeves", f1.broj_evaluacija_funkcije(), funkcija1_hj))
   f1.broj_evaluacija = 0
   funkcija1_nm = nelder_mead(f1, x0, alfa=1, beta=0.5, gama=2, sigma=0.5, epsilon=1e-6)
   rezultati.append(("Funkcija 1", "Nelder-Mead", f1.broj_evaluacija_funkcije(), funkcija1_nm))

   # Funkcija 2, početna točka [0.1, 0.3]
   x0 = np.array([0.1, 0.3])
   funkcija2_kp = KoordinatnoPretrazivanje(f2, x0, e=1e-6)
   rezultati.append(("Funkcija 2", "Koordinatno pretraživanje", f2.broj_evaluacija_funkcije(), funkcija2_kp))
   f2.broj_evaluacija = 0
   funkcija2_hj = hooke_jeeves(f2, x0, Dx=np.array([0.5, 0.5]), e=np.array([1e-6, 1e-6]))
   rezultati.append(("Funkcija 2", "Hooke-Jeeves", f2.broj_evaluacija_funkcije(), funkcija2_hj))
   f2.broj_evaluacija = 0
   funkcija2_nm = nelder_mead(f2, x0, alfa=1, beta=0.5, gama=2, sigma=0.5, epsilon=1e-6)
   rezultati.append(("Funkcija 2", "Nelder-Mead", f2.broj_evaluacija_funkcije(), funkcija2_nm))

   # Funkcija 3, početna točka 0, null vektor dimenzije 5
   x0 = np.zeros(5)
   funkcija3_kp = KoordinatnoPretrazivanje(f3, x0, e=1e-6)
   rezultati.append(("Funkcija 3", "Koordinatno pretraživanje", f3.broj_evaluacija_funkcije(), funkcija3_kp))
   f3.broj_evaluacija = 0
   funkcija3_hj = hooke_jeeves(f3, x0, Dx=np.array([0.5] * 5), e=np.array([1e-6] * 5))
   rezultati.append(("Funkcija 3", "Hooke-Jeeves", f3.broj_evaluacija_funkcije(), funkcija3_hj))
   f3.broj_evaluacija = 0
   funkcija3_nm = nelder_mead(f3, x0, alfa=1, beta=0.5, gama=2, sigma=0.5, epsilon=1e-6)
   rezultati.append(("Funkcija 3", "Nelder-Mead", f3.broj_evaluacija_funkcije(), funkcija3_nm))

   # Funkcija 4, početna točka [5.1, 1.1]
   x0 = np.array([5.1, 1.1])
   funkcija4_kp = KoordinatnoPretrazivanje(f4, x0, e=1e-6)
   rezultati.append(("Funkcija 4", "Koordinatno pretraživanje", f4.broj_evaluacija_funkcije(), funkcija4_kp))
   f4.broj_evaluacija = 0
   funkcija4_hj = hooke_jeeves(f4, x0, Dx=np.array([0.5, 0.5]), e=np.array([1e-6, 1e-6]))
   rezultati.append(("Funkcija 4", "Hooke-Jeeves", f4.broj_evaluacija_funkcije(), funkcija4_hj))
   f4.broj_evaluacija = 0
   funkcija4_nm = nelder_mead(f4, x0, alfa=1, beta=0.5, gama=2, sigma=0.5, epsilon=1e-6)
   rezultati.append(("Funkcija 4", "Nelder-Mead", f4.broj_evaluacija_funkcije(), funkcija4_nm))

   # Prikaz rezultata
   print("Funkcija | Algoritam | Broj Evaluacija | Pronađeni Minimum")
   for r in rezultati:
      print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]}")

   print("\nTreci zadatak: \n")
   #početna točka 5,5
   x0 = np.array([5, 5])
   funkcija = Funkcija4()
   # minimum_nm = nelder_mead(funkcija, x0, alfa=1, beta=0.5, gama=2, sigma=0.5, epsilon=1e-6)
   # print("Minimum je na x =", minimum_nm)
   # print("Broj evaluacija funkcije:", funkcija.broj_evaluacija_funkcije())
   funkcija.broj_evaluacija = 0
   minimum_hj = hooke_jeeves(funkcija, x0, Dx=np.array([0.5, 0.5]), e=np.array([1e-6, 1e-6]))
   print("Minimum je na x =", minimum_hj)
   print("Broj evaluacija funkcije:", funkcija.broj_evaluacija_funkcije())

   print("\nCetvrti zadatak: \n")
   x0 = np.array([0.5, 0.5])
   koraci = range(1, 21)
   for korak in koraci:
      f1.broj_evaluacija = 0
      simpleks = generiraj_simpleks(x0, korak)
      minimum_nm = nelder_mead(f1, x0, alfa=1, beta=0.5, gama=2, sigma=0.5, epsilon=1e-6, pomak=korak)
      print(f"Korak: {korak}, Broj evaluacija: {f1.broj_evaluacija_funkcije()}, Minimum: {minimum_nm}")

   x0 = np.array([20, 20])
   koraci = range(1, 21)
   for korak in koraci:
      f1.broj_evaluacija = 0
      simpleks = generiraj_simpleks(x0, korak)
      minimum_nm = nelder_mead(f1, x0, alfa=1, beta=0.5, gama=2, sigma=0.5, epsilon=1e-6, pomak=korak)
      print(f"Korak: {korak}, Broj evaluacija: {f1.broj_evaluacija_funkcije()}, Minimum: {minimum_nm}")


   print("\nPeti zadatak: \n")

   def optimizacija_funkcija6():
      funkcija = Funkcija6()
      tocno = 0
      pokusaji = 100

      for _ in range(pokusaji):
         x0 = np.array([random.uniform(-50, 50) for _ in range(2)])
         minimum_nm = nelder_mead(funkcija, x0, alfa=1, beta=0.5, gama=2, sigma=0.5, epsilon=1e-6)
         #minimum_hj = hooke_jeeves(funkcija, x0, Dx=np.array([0.5, 0.5]), e=np.array([1e-6, 1e-6]))
         #minimum_kp = KoordinatnoPretrazivanje(funkcija, x0, e=1e-6)
         
         if funkcija.evaluiraj(minimum_nm) < 1e-12:
            tocno += 1

      točnost = tocno / pokusaji
      print(f"Točnost pronalaženja globalnog minimuma: {točnost:.2f}")

   optimizacija_funkcija6()

if __name__ == "__main__":
   main()