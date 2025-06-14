import numpy as np

def jacobi_sequential(psitmp, psi, m, n):
   for i in range(1, m + 1):
      for j in range(1, n + 1):
         psitmp[i, j] = 0.25 * (psi[i - 1, j] + psi[i + 1, j] + psi[i, j - 1] + psi[i, j + 1])
   return psitmp