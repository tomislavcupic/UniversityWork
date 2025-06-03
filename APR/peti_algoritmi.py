import numpy as np
from matrica import Matrica

def analytical_solution(t, x0):
   x1_0, x2_0 = x0[0][0], x0[1][0]
   x1 = x1_0 * np.cos(t) + x2_0 * np.sin(t)
   x2 = -x1_0 * np.sin(t) + x2_0 * np.cos(t)
   return x1, x2

def cumulative_error_pece(numerical_results, times, x0):
   error = [0, 0]
   count = 0
   for t, x_num in zip(times, numerical_results):
      x1_real, x2_real = analytical_solution(t, x0)
      error[0] = error[0] + abs(x1_real - x_num[0][0][0])
      error[1] = error[1] + abs(x2_real - x_num[0][0][1])
      count += 1
   return error

def cumulative_error(numerical_results, times, x0):
   error = [0, 0]
   count = 0
   for t, x_num in zip(times, numerical_results):
      x1_real, x2_real = analytical_solution(t, x0)
      error[0] = error[0] + abs(x1_real - x_num[0])
      error[1] = error[1] + abs(x2_real - x_num[1])
      count += 1
   return error

def pece_system(t, x, A, B, r):
  return A * x[0][0] + B * Matrica(data=[[val] for val in r(t).tolist()])

def system(t, x, A, B, r):
  return A * x + B * Matrica(data=[[val] for val in r(t).tolist()])

def euler(A, B, r, x0, t_max, h):
   times = [i * h for i in range(int(t_max / h))]
   x_values = []
   x = x0
   for t in times:
      x_values.append(x.tolist())
      x = x + h * system(t, x, A, B, r)
   return x_values, times

def obrnuti_euler(A, B, r, x0, t_max, h):
   times = [i * h for i in range(int(t_max / h))]
   x_values = []
   x = x0 
   
   for t in times:
      x_values.append(x.tolist())
      x_new = x
      for _ in range(10):
         x_new = x + h * system(t + h, x_new, A, B, r)
      x = x_new
   
   return x_values, times

def trapezoid(A, B, r, x0, t_max, h):
   times = [i * h for i in range(int(t_max / h))]
   x_values = []
   x = x0 
   
   for t in times:
      x_values.append(x.tolist())
      sys1 = system(t, x, A, B, r)
      sys2 = system(t + h, x + h * sys1, A, B, r)
      x = x + h * 0.5 * (sys1 + sys2)
   
   return x_values, times

def runge_kutta4(A, B, r, x0, t_max, h):
   times = [i * h for i in range(int(t_max / h))]
   x_values = []
   x = x0
   
   for t in times:
      x_values.append(x.tolist())
      k1 = h * system(t, x, A, B, r)
      k2 = h * system(t + 0.5 * h, x + 0.5 * k1, A, B, r)
      k3 = h * system(t + 0.5 * h, x + 0.5 * k2, A, B, r)
      k4 = h * system(t + h, x + k3, A, B, r)
      x = x + (1 / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
   
   return x_values, times

def pece_metoda_euler_obrnuti_euler(A, B, r, x0, t_max, h, p, c, corrector_iterations=1):
   times = [i * h for i in range(int(t_max / h))]
   x_values = []
   x = np.array(x0).reshape(-1, 1)
   
   for t in times:
      x_values.append(x.tolist())
      
      dx = pece_system(t, x, A, B, r)
      x_pred = x + h * dx 
      
      x_corr = x_pred
      for _ in range(corrector_iterations):
         dx_corr = pece_system(t + h, x_corr, A, B, r)
         x_corr = x + h * dx_corr
      x = x_corr
   
   return x_values, times

def pece_metoda_euler_trapez(A, B, r, x0, t_max, h, predictor, corrector, corrector_iterations=1):
   times = [i * h for i in range(int(t_max / h))]
   x = np.array(x0).reshape(-1, 1)
   x_values = []

   for t in times:
      x_values.append(x)
      x_pred = x + h * pece_system(t, x, A, B, r)
      x_corr = x_pred
      for _ in range(corrector_iterations):
         sys1 = pece_system(t, x, A, B, r)
         sys2 = pece_system(t + h, x_corr, A, B, r)
         x_corr = x + h * 0.5 * (sys1 + sys2)
      x = x_corr
   return x_values, times


def ljepsi_print(xv, t, n=100):
   for i in range(len(xv)):
      if i % n == 0:
         print(xv[i], end= " ")
         print(t[i])

def pece_ljepsi_print(xv, t, n=100):
   for i in range(len(xv)):
      if i % n == 0:
         print(xv[i][0][0].data, end= " ")
         print(t[i])