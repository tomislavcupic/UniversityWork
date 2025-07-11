import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
import numpy as np

def simulated_annealing(f, x0, T0=1.0, Tmin=1e-8, alpha=0.999, max_iter=10000):
   x = x0.copy()
   fx = f(x)
   T = T0

   for i in range(max_iter):
      if T < Tmin:
         print(f"Temperature too low, stopping at iteration {i}.")
         break

      x_new = x + np.random.uniform(-0.1, 0.1, size=len(x))
      fx_new = f(x_new)
      dE = fx_new - fx

      if dE < 0 or np.random.rand() < np.exp(-dE / T):
         x, fx = x_new, fx_new

      T *= alpha
   return x, fx, [x0] + [x.copy() for _ in range(max_iter)] 

def simulated_annealing_plot_optimization_path(func, history, xlim=(-6, 6), ylim=(-6, 6), levels=50):
   history = np.array(history)
   x1 = np.linspace(xlim[0], xlim[1], 400)
   x2 = np.linspace(ylim[0], ylim[1], 400)
   X1, X2 = np.meshgrid(x1, x2)
   Z = func([X1, X2])

   plt.figure(figsize=(8, 6))
   contour = plt.contour(X1, X2, Z, levels=levels, cmap='viridis')
   plt.clabel(contour, inline=1, fontsize=8)

   plt.plot(history[:, 0], history[:, 1], 'r.-', label='Path')
   plt.plot(history[0, 0], history[0, 1], 'bo', label='Start')
   plt.plot(history[-1, 0], history[-1, 1], 'gs', label='Minimum')

   plt.xlabel('$x_1$')
   plt.ylabel('$x_2$')
   plt.title('Simulated Annealing Optimization Path')
   plt.legend()
   plt.grid(True)
   plt.show()

def nelder_mead(f, x0, max_iter=1000, tol=1e-9):
   n = len(x0)
   alpha = 1.0  # reflection
   beta = 2.0   # expansion
   gamma = 0.5  # contraction
   delta = 0.5  # shrink

   simplex = [x0] + [x0 + np.eye(n)[i] for i in range(n)]
   history = [np.array(simplex)]

   for iteration in range(max_iter):
      simplex = sorted(simplex, key=f)
      best = simplex[0]
      worst = simplex[-1]
      second_worst = simplex[-2]
      centroid = np.mean(simplex[:-1], axis=0)

      reflected = centroid + alpha * (centroid - worst)
      f_reflected = f(reflected)

      if f(best) <= f_reflected < f(second_worst):
         simplex[-1] = reflected
      elif f_reflected < f(best):
         expanded = centroid + beta * (reflected - centroid)
         if f(expanded) < f_reflected:
            simplex[-1] = expanded
         else:
            simplex[-1] = reflected
      else:
         contracted = centroid + gamma * (worst - centroid)
         if f(contracted) < f(worst):
            simplex[-1] = contracted
         else:
            simplex = [best] + [best + delta * (x - best) for x in simplex[1:]]

      history.append(np.array(simplex))

      if np.max([np.linalg.norm(np.array(x) - np.array(best)) for x in simplex]) < tol:
         print(f"Konvergencija postignuta u {iteration} iteracija.")
         break

   return np.array(best), f(best), history


def nelder_mead_plot_optimization_path(f, history, xlim=(-5, 5), ylim=(-5, 5), levels=50):
   history = np.array(history)
   x1 = np.linspace(xlim[0], xlim[1], 400)
   x2 = np.linspace(ylim[0], ylim[1], 400)
   X1, X2 = np.meshgrid(x1, x2)
   Z = f([X1, X2])

   plt.figure(figsize=(8, 6))
   contour = plt.contour(X1, X2, Z, levels=levels, cmap='viridis')
   plt.clabel(contour, inline=1, fontsize=8)

   for i in range(len(history) - 1):
      plt.plot(history[i][:, 0], history[i][:, 1], 'r.-', alpha=0.5)

   plt.plot(history[0][0, 0], history[0][0, 1], 'bo', label='Početak')
   plt.plot(history[-1][0, 0], history[-1][0, 1], 'gs', label='Minimum')

   plt.xlabel('$x_1$')
   plt.ylabel('$x_2$')
   plt.title('Nelder-Mead optimizacija Bohachevsky funkcije')
   plt.legend()
   plt.grid(True)
   plt.show()

def bfgs(f, grad_func, x0, max_iter=100, tol=1e-8):
   x = x0.copy()
   n = len(x)
   H = np.eye(n)
   history = [x.copy()]

   for i in range(max_iter):
      grad = grad_func(x)
      if np.linalg.norm(grad) < tol:
         print(f"Converged in {i} iterations.")
         break

      p = -H @ grad  # smjer spuštanja
      alpha = line_search_wolfe(f, grad_func, x, p)
      s = alpha * p
      x_new = x + s
      grad_new = grad_func(x_new)
      y = grad_new - grad
      ys = np.dot(y, s)

      if ys > 1e-10:
         Hy = H @ y
         denom = float(np.dot(y, s))

         # Drugi član: (1 + y^T H y / y^T s) * (s s^T) / (y^T s)
         term2 = (1 + np.dot(y, Hy) / denom) * (np.outer(s, s) / denom)
         # Treći član: (H y s^T + s y^T H) / (y^T s)
         term3 = (np.outer(Hy, s) + np.outer(s, Hy)) / denom

         H = H + term2 - term3
      x = x_new
      history.append(x.copy())

      if i == max_iter - 1:
         print("Maximum iterations reached.")

   return x, f(x), history

def bfgs_plot_optimization_path(f, history, xlim=(-6, 6), ylim=(-6, 6), levels=50):
   history = np.array(history)
   x1 = np.linspace(xlim[0], xlim[1], 400)
   x2 = np.linspace(ylim[0], ylim[1], 400)
   X1, X2 = np.meshgrid(x1, x2)
   Z = f([X1, X2])

   plt.figure(figsize=(8, 6))
   contour = plt.contour(X1, X2, Z, levels=levels, cmap='viridis')
   plt.clabel(contour, inline=1, fontsize=8)

   plt.plot(history[:, 0], history[:, 1], 'r.-', label='Putanja')
   plt.plot(history[0, 0], history[0, 1], 'bo', label='Početak')
   plt.plot(history[-1, 0], history[-1, 1], 'gs', label='Minimum')

   plt.xlabel('$x_1$')
   plt.ylabel('$x_2$')
   plt.title('BFGS optimizacija Bohachevsky funkcije')
   plt.legend()
   plt.grid(True)
   plt.show()


def line_search_wolfe(f, grad_f, x, p, alpha_max=10.0, c1=1e-4, c2=0.9, max_iter=20):
   def phi(alpha):
      return f(x + alpha * p)
   
   def phi_prime(alpha):
      return np.dot(grad_f(x + alpha * p), p)

   alpha_0 = 0
   alpha_1 = 1.0
   i = 1

   while True:
      phi_i = phi(alpha_1)
      phi_0 = phi(0)
      phi_prime_0 = phi_prime(0)

      if (phi_i > phi_0 + c1 * alpha_1 * phi_prime_0) or (i > 1 and phi_i >= phi(alpha_0)):
         return zoom(f, grad_f, x, p, alpha_0, alpha_1, c1, c2)

      phi_prime_i = phi_prime(alpha_1)
      if abs(phi_prime_i) <= -c2 * phi_prime_0:
         return alpha_1

      if phi_prime_i >= 0:
         return zoom(f, grad_f, x, p, alpha_1, alpha_0, c1, c2)

      alpha_0 = alpha_1
      alpha_1 = min((alpha_1 + alpha_max) / 2, alpha_max)
      i += 1
      if i > max_iter:
         return alpha_1

def zoom(f, grad_f, x, p, alpha_lo, alpha_hi, c1, c2, max_iter=20):
   def phi(alpha):
      return f(x + alpha * p)
   
   def phi_prime(alpha):
      return np.dot(grad_f(x + alpha * p), p)

   phi_0 = phi(0)
   phi_prime_0 = phi_prime(0)

   for _ in range(max_iter):
      alpha_j = 0.5 * (alpha_lo + alpha_hi)

      if (phi(alpha_j) > phi_0 + c1 * alpha_j * phi_prime_0) or (phi(alpha_j) >= phi(alpha_lo)):
         alpha_hi = alpha_j
      else:
         phi_prime_j = phi_prime(alpha_j)
         if abs(phi_prime_j) <= -c2 * phi_prime_0:
            return alpha_j
         if phi_prime_j * (alpha_hi - alpha_lo) >= 0:
            alpha_hi = alpha_lo
         alpha_lo = alpha_j
   return alpha_j

def newtons_method_with_lm(func, grad_func, hessian_func, x0, max_iter=1000, tol=1e-8):
   x = x0.copy()
   history = [x.copy()]
   lambda_reg = 1e-3

   for i in range(max_iter):
      grad = grad_func(x)
      hess = hessian_func(x)

      #hess_reg = hess + lambda_reg * np.eye(len(x))
      try:
         p = -np.linalg.solve(hess, grad)
      except np.linalg.LinAlgError:
         print("Hessian je singularan. Koristi se pseudo-inverz.")
         p = -np.linalg.pinv(hess) @ grad

      # alpha = line_search_wolfe(func, grad_func, x, p)
      # x_new = x + alpha * p
      # history.append(x_new.copy())
      x_new = x + p
      fx_old = func(x)
      fx_new = func(x_new)

      if fx_new < fx_old:
         lambda_reg *= 0.7
         x = x_new
         history.append(x.copy())
      else:
         lambda_reg *= 1.5
         print(f"Funkcija nije smanjena u iteraciji {i+1}, povećavam regularizaciju.")
         continue

      if np.linalg.norm(grad) < tol:
         print(f"Konvergencija postignuta u {i+1} iteracija.")
         return x_new, func(x_new), history
      x = x_new

   print("Dosegnut maksimalan broj iteracija bez konvergencije.")
   return x, func(x), history

def newton_plot_optimization_path(f, history, title="Putanja optimizacije", levels=50):
   history = np.array(history)
   x_vals = history[:, 0]
   y_vals = history[:, 1]

   # Definiraj mrežu točaka
   x = np.linspace(-6, 6, 400)
   y = np.linspace(-6, 6, 400)
   X, Y = np.meshgrid(x, y)
   Z = np.array([[f(np.array([xi, yi])) for xi, yi in zip(row_x, row_y)]
               for row_x, row_y in zip(X, Y)])

   plt.figure(figsize=(10, 6))
   contour = plt.contour(X, Y, Z, levels=levels, cmap='viridis')
   plt.clabel(contour, inline=True, fontsize=8)

   plt.plot(x_vals, y_vals, 'ro--', label='Putanja')
   plt.plot(x_vals[0], y_vals[0], 'go', label='Početna točka')
   plt.plot(x_vals[-1], y_vals[-1], 'bo', label='Kraj (minimum)')
   plt.title(title)
   plt.xlabel("x")
   plt.ylabel("y")
   plt.legend()
   plt.grid(True)
   plt.show()

def gradient_descent_unconstrained(func, grad_func, x0, max_iter=1000, learning_rate=0.02, tol=1e-6):
   x = np.array(x0)
   history = [x.copy()]

   for i in range(max_iter):
      grad = grad_func(x)
      x_new = x - learning_rate * grad
      history.append(x_new.copy())
      if np.linalg.norm(x_new - x) < tol:
         print(f"Converged in {i+1} iterations.")
         break

      x = x_new
      if i == max_iter - 1:
         print("Maximum iterations reached without convergence.")

   return x, func(x), history

def grad_plot_optimization_path(f, history, title="Putanja optimizacije", levels=50):
   history = np.array(history)
   x_vals = history[:, 0]
   y_vals = history[:, 1]

   x = np.linspace(-6, 6, 400)
   y = np.linspace(-6, 6, 400)
   X, Y = np.meshgrid(x, y)
   Z = np.array([[f(np.array([xi, yi])) for xi, yi in zip(row_x, row_y)]
               for row_x, row_y in zip(X, Y)])

   plt.figure(figsize=(10, 6))
   contour = plt.contour(X, Y, Z, levels=levels, cmap='viridis')
   plt.clabel(contour, inline=True, fontsize=8)

   plt.plot(x_vals, y_vals, 'ro--', label='Putanja')
   plt.plot(x_vals[0], y_vals[0], 'go', label='Start')
   plt.plot(x_vals[-1], y_vals[-1], 'bo', label='Minimum')
   plt.title(title)
   plt.xlabel("x")
   plt.ylabel("y")
   plt.legend()
   plt.grid(True)
   plt.show()