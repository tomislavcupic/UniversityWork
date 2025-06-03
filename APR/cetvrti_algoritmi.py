import numpy as np

class BoxAlgorithm:
   def __init__(self, func, constraints, Xd, Xg, epsilon=1e-6, alpha=1.3, max_iterations=10000):
      self.func = func
      self.constraints = constraints
      self.Xd = np.array(Xd)
      self.Xg = np.array(Xg)
      self.epsilon = epsilon
      self.alpha = alpha
      self.max_iterations = max_iterations

   def is_feasible(self, X):
      """Provjera zadovoljava li točka X sva ograničenja."""
      return np.all(X >= self.Xd) and np.all(X <= self.Xg) and all(g(X) >= 0 for g in self.constraints)

   def reflect(self, Xc, Xh):
      """Izračun reflektirane točke."""
      Xr = (1 + self.alpha) * Xc - self.alpha * Xh
      Xr = np.clip(Xr, self.Xd, self.Xg)  # Primjena eksplicitnih ograničenja
      while any(g(Xr) < 0 for g in self.constraints):  # Provjera implicitnih ograničenja
         Xr = 0.5 * (Xr + Xc)
      return Xr

   def optimize(self, X0):
      """Glavna metoda za optimizaciju pomoću Box algoritma."""
      if not self.is_feasible(X0):
         raise ValueError("Početna točka X0 ne zadovoljava ograničenja!")

      n = len(X0)
      points = [X0.copy()]

      # Generiranje početnih točaka unutar ograničenja
      for _ in range(2 * n):
         X = self.Xd + np.random.rand(n) * (self.Xg - self.Xd)
         while any(g(X) < 0 for g in self.constraints):
               X = 0.5 * (X + points[-1])  # Pomicanje prema centroidu prihvaćenih točaka
         points.append(X)

      points = np.array(points)

      iteration = 0
      best_value = float('inf')
      stagnant_iterations = 0

      while True:
         # Sortiranje točaka prema vrijednosti ciljne funkcije
         points = sorted(points, key=self.func)
         Xh, Xh2 = points[-1], points[-2]
         Xc = np.mean(points[:-1], axis=0)  # Centroid bez najlošije točke

         # Refleksija
         Xr = self.reflect(Xc, Xh)

         if self.func(Xr) > self.func(Xh2):
               Xr = 0.5 * (Xr + Xc)  # Još jednom prema Xc ako je to i dalje najlošija

         points[-1] = Xr  # Zamjena najlošije točke reflektiranom

         # Provjera uvjeta zaustavljanja
         current_best = self.func(points[0])
         if abs(current_best - best_value) < self.epsilon:
               stagnant_iterations += 1
         else:
               stagnant_iterations = 0
               best_value = current_best

         if stagnant_iterations >= self.max_iterations:
               print("Divergencija: Nema poboljšanja u cilju kroz 100 iteracija.")
               break

         if np.std([self.func(p) for p in points]) < self.epsilon:
               print("Postignuta zadana preciznost.")
               break

         iteration += 1

      return points[0], self.func(points[0])
