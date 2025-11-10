import math, random, sys

class SimulatedAnnealing:
   def __init__(self, func, dim, minimize=True, nbmc=0.1, max_iter=100000, equilibrium=100, T=50.0, alpha=0.9):
      self.func = func
      self.dim = dim
      self.minimize = minimize
      self.nbmc = nbmc
      self.max_iter = max_iter
      self.equilibrium = equilibrium
      self.T = T
      self.alpha = alpha

   def get_neighbor(self, params):
      return [p + random.uniform(-self.nbmc, self.nbmc) for p in params]

   def solve(self, initial=None):
      if initial is None:
         current = [random.uniform(-1, 1) for _ in range(self.dim)]
      else:
         current = initial[:]
      current_eval = self.func(current)
      best = current[:]
      best_eval = current_eval

      T = self.T
      iter_count = 0
      while iter_count < self.max_iter:
         for _ in range(self.equilibrium):
            neighbor = self.get_neighbor(current)
            neighbor_eval = self.func(neighbor)
            delta = neighbor_eval - current_eval
            if (self.minimize and delta < 0) or (not self.minimize and delta > 0) or \
               random.random() < math.exp(-abs(delta) / max(T, 1e-12)):
               current = neighbor
               current_eval = neighbor_eval
               if (self.minimize and current_eval < best_eval) or (not self.minimize and current_eval > best_eval):
                  best, best_eval = current[:], current_eval
            iter_count += 1
            if iter_count >= self.max_iter:
               break
         T *= self.alpha
      return best, best_eval

def model(params, x1, x2, x3, x4, x5):
   a, b, c, d, e, f = params
   arg = d * x3
   #arg = max(min(arg, 50), -50)
   return a * x1 + b * (x1 ** 3) * x2 + c * math.exp(arg) * (1 + math.cos(e * x4)) + f * x4 * (x5 ** 2)

def make_mse(data):
   def mse(params):
      s = 0.0
      for (x1, x2, x3, x4, x5, y) in data:
         ypred = model(params, x1, x2, x3, x4, x5)
         s += (y - ypred) ** 2
      return s / len(data)
   return mse

def load_data(path):
   data = []
   with open(path) as f:
      for line in f:
         parts = line.strip().strip('[]').replace(',', ' ').split()
         if len(parts) == 6:
            data.append(tuple(map(float, parts)))
   return data

if __name__ == "__main__":
   if len(sys.argv) < 3:
      print("Upotreba: python prijenosna.py <maxIter> <ulazna_datoteka>")
      sys.exit(1)

   max_iter = int(sys.argv[1])
   path = sys.argv[2]
   data = load_data(path)

   mse_func = make_mse(data)
   sa = SimulatedAnnealing(mse_func, dim=6, minimize=True, max_iter=max_iter, nbmc=0.1, equilibrium=100, T=50, alpha=0.9)

   best, best_eval = sa.solve()

   print("\nNajbolje pronađeno rješenje:")
   names = ['a', 'b', 'c', 'd', 'e', 'f']
   for n, v in zip(names, best):
      print(f"{n} = {v:.6f}")
   print(f"Minimalna pogreška (MSE): {best_eval:.6f}")