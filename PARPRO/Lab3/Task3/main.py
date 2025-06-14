import numpy as np
import time
from jacobi_opencl import jacobi_opencl
from jacobi_sequential import jacobi_sequential

def deltasq(newarr, oldarr, m, n):
   diff = newarr[1:m+1, 1:n+1] - oldarr[1:m+1, 1:n+1]
   return np.sum(diff ** 2)

def boundarypsi(psi, m, n, b, h, w):
   for i in range(b+1, b+w):
      psi[i, 0] = i - b
   for i in range(b+w, m+2):
      psi[i, 0] = w
   for j in range(1, h+1):
      psi[m+1, j] = w
   for j in range(h+1, h+w):
      psi[m+1, j] = w - (j - h)

def run_simulation(parallel=True):
   scalefactor = 64
   # za usporedbu smanji na onak 10 da se napravi u ovom stoljeću
   numiter = 1000

   bbase, hbase, wbase = 10, 15, 5
   mbase, nbase = 32, 32

   b = bbase * scalefactor
   h = hbase * scalefactor
   w = wbase * scalefactor
   m = mbase * scalefactor
   n = nbase * scalefactor

   psi = np.zeros((m+2, n+2), dtype=np.float64)
   psitmp = np.zeros_like(psi)

   boundarypsi(psi, m, n, b, h, w)
   bnorm = np.sqrt(np.sum(psi ** 2))

   start = time.time()
   for iter in range(1, numiter + 1):
      if parallel:
         psitmp = jacobi_opencl(psitmp.flatten(), psi.flatten(), m, n).reshape((m+2, n+2))
      else:
         psitmp = jacobi_sequential(psitmp, psi, m, n)

      if iter == numiter:
         error = np.sqrt(deltasq(psitmp, psi, m, n)) / bnorm

      psi[1:m+1, 1:n+1] = psitmp[1:m+1, 1:n+1]
   end = time.time()

   return end - start, error

def main():
   print("Running parallel (OpenCL) version...")
   parallel_time, parallel_error = run_simulation(parallel=True)
   print(f"Time: {parallel_time:.2f}s | Error: {parallel_error:.8f}\n")

   # print("Running sequential version...")
   # sequential_time, sequential_error = run_simulation(parallel=False)
   # print(f"Time: {sequential_time:.2f}s | Error: {sequential_error:.8f}\n")

   # speedup = sequential_time / parallel_time
   # print(f"Speedup (sequential / parallel): {speedup:.2f}x")

if __name__ == "__main__":
   main()