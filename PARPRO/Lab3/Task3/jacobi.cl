__kernel void jacobistep_kernel(
   __global double* psitmp,
   __global const double* psi,
   int m, int n
) {
   int i = get_global_id(0) + 1;
   int j = get_global_id(1) + 1;

   if (i <= m && j <= n) {
      int idx = i * (m + 2) + j;
      psitmp[idx] = 0.25 * (
         psi[(i - 1) * (m + 2) + j] +
         psi[(i + 1) * (m + 2) + j] +
         psi[i * (m + 2) + j - 1] +
         psi[i * (m + 2) + j + 1]
      );
   }
}
