import math
import numpy as np

# Zlatni rez
def Zlatni_rez(f, a, b, e=1e-6, ispis=False):
   k = (math.sqrt(5) - 1) / 2
   c = b - k * (b - a)
   d = a + k * (b - a)
   fc = f(c)
   fd = f(d)
   while abs(b - a) > e:
      if ispis:
         print(f"a: {a}, b: {b}, c: {c}, d: {d}, f(c): {fc}, f(d): {fd}")
      if fc < fd:
         b = d
         d = c
         c = b - k * (b - a)
         fd = fc
         fc = f(c)
      else:
         a = c
         c = d
         d = a + k * (b - a)
         fc = fd
         fd = f(d)
   return (a + b) / 2

def optimizacija(f, tocka=None, h=1.0, a=None, b=None, e=1e-6, ispis=False):
   if a is not None and b is not None:
      return Zlatni_rez(lambda x: f.povecaj_broj(x) or f.evaluiraj(x), a, b, e, ispis=ispis)
   elif tocka is not None:
      l, r = unimodalni(f, tocka, h)
      return Zlatni_rez(lambda x: f.povecaj_broj(x) or f.evaluiraj(x), l, r, e, ispis=ispis)
   else:
      raise ValueError("Morate navesti ili početnu točku (tocka) ili interval (a i b)")

def unimodalni(f, tocka, h):
   l = tocka - h
   r = tocka + h
   m = tocka
   step = 1

   fm = f.evaluiraj(m)
   f.povecaj_broj(m)
   fl = f.evaluiraj(l)
   f.povecaj_broj(l)
   fr = f.evaluiraj(r)
   f.povecaj_broj(r)

   if fm < fr and fm < fl:
      return (l, r)
   elif fm > fr:
      while fm > fr:
         l = m
         m = r
         fm = fr
         step *= 2
         r = tocka + h * step
         fr = f.evaluiraj(r)
         f.povecaj_broj(r)
   else:
      while fm > fl:
         r = m
         m = l
         fm = fl
         l = tocka - h * step
         fl = f.evaluiraj(l)
         f.povecaj_broj(l)
   return (l, r)

def KoordinatnoPretrazivanje(f, xnula, e=1e-6):
   x = np.copy(xnula)
   xs = np.inf
   n = len(xnula)
   while np.linalg.norm(x - xs) > e:
      xs = np.copy(x)
      for i in range(n):
         def flambda(lam):
               x_t = np.copy(x)
               x_t[i] += lam
               f.povecaj_broj(x_t)
               return f.evaluiraj(x_t)
         lam_opt = Zlatni_rez(flambda, -1, 1, e)
         x[i] += lam_opt
   return x

def generiraj_simpleks(x0, pomak):
   n = len(x0)
   simpleks = [x0]
   for i in range(n):
      tocka = np.copy(x0)
      tocka[i] += pomak
      simpleks.append(tocka)
   return simpleks

def nelder_mead(funkcija, x0, alfa=1, beta=0.5, gama=2, sigma=0.5, epsilon=1e-6, pomak=1.0):
   n = len(x0)
   simpleks = generiraj_simpleks(x0, pomak)

   while True:
      simpleks = sorted(simpleks, key=lambda x: funkcija.povecaj_broj(x) or funkcija.evaluiraj(x))
      Xh, Xl = simpleks[-1], simpleks[0]
      Xc = sum(simpleks[:-1]) / n
      Xr = Xc + alfa * (Xc - Xh)
      if funkcija.povecaj_broj(Xr) or funkcija.evaluiraj(Xr) < funkcija.evaluiraj(Xl):
         Xe = Xc + gama * (Xr - Xc)
         if funkcija.povecaj_broj(Xe) or funkcija.evaluiraj(Xe) < funkcija.evaluiraj(Xl):
               Xh = Xe
         else:
               Xh = Xr
      else:
         if all(funkcija.povecaj_broj(Xr) or funkcija.evaluiraj(Xr) > funkcija.evaluiraj(x) for x in simpleks[:-1]):
               Xk = Xc + beta * (Xh - Xc)
               if funkcija.povecaj_broj(Xk) or funkcija.evaluiraj(Xk) < funkcija.evaluiraj(Xh):
                  Xh = Xk
               else:
                  Xh = Xl + sigma * (Xl - Xh)
         else:
               Xh = Xr
      simpleks[-1] = Xh
      if np.linalg.norm(np.array(simpleks) - Xl) < epsilon:
         break
   return Xl

def istrazi(funkcija, xP, Dx):
   x = np.copy(xP)
   for i in range(len(x)):
      P = funkcija.evaluiraj(x)
      funkcija.povecaj_broj(x)
      x[i] += Dx[i]
      N = funkcija.evaluiraj(x)
      funkcija.povecaj_broj(x)
      if N > P:
         x[i] -= 2 * Dx[i]
         N = funkcija.evaluiraj(x)
         funkcija.povecaj_broj(x)
         if N > P:
               x[i] += Dx[i]
   return x

def hooke_jeeves(funkcija, x0, Dx=None, e=None):
   if Dx is None:
      Dx = np.array([0.5] * len(x0))
   if e is None:
      e = np.array([1e-6] * len(x0))

   xB = np.copy(x0)
   xP = np.copy(x0)

   while np.linalg.norm(Dx) > np.linalg.norm(e):
      xN = istrazi(funkcija, xP, Dx)
      if funkcija.povecaj_broj(xN) or funkcija.evaluiraj(xN) < funkcija.evaluiraj(xB):
         xP = 2 * xN - xB
         xB = xN
      else:
         Dx /= 2
         xP = xB

   return xB

def ucitaj_parametre(ime_datoteke):
   with open(ime_datoteke, 'r') as f:
      linije = f.readlines()
      
      x0 = np.array([float(x) for x in linije[0].strip().split()])
      e = np.array([float(eps) for eps in linije[1].strip().split()])
      Dx = np.array([float(dx) for dx in linije[2].strip().split()])
      parametri = [float(param) for param in linije[3].strip().split()]
      
      alfa, beta, gama, sigma = parametri
      return x0, e, Dx, alfa, beta, gama, sigma

