import pyopencl as cl
import numpy as np
import time
import math

KERNEL_CODE = """
__kernel void compute_pi(__global double* partial_sums, long N, long M) {
   long gid = get_global_id(0);
   long total_threads = get_global_size(0);

   double h = 1.0 / (double) N;
   double sum = 0.0;

   long start = gid * M;
   long end = min(start + M, N);

   for (long i = start; i < end; ++i) {
      double x = h * ((double)i + 0.5);
      sum += 4.0 / (1.0 + x * x);
   }

   partial_sums[gid] = sum * h;
}
"""


def pi_serial(N):
   h = 1.0 / N
   s = sum(4.0 / (1.0 + ((i + 0.5) * h)**2) for i in range(N))
   return h * s


def main():
   N =  10_000_000_000  # dovoljno velik da traje par sekundi
   #N = 32768 * 64
   M = 1000
   L = 128 

   G = (N + M - 1) // M 
   if G % L != 0:
      G = ((G + L - 1) // L) * L
   print(f"N = {N}, M = {M}, G = {G}, L = {L}")

   ctx = cl.create_some_context()
   queue = cl.CommandQueue(ctx)
   mf = cl.mem_flags
   partial_np = np.zeros(G, dtype=np.float64)
   partial_buf = cl.Buffer(ctx, mf.WRITE_ONLY, partial_np.nbytes)

   program = cl.Program(ctx, KERNEL_CODE).build()

   start = time.time()
   program.compute_pi(queue, (G,), (L,), partial_buf, np.int64(N), np.int64(M))
   queue.finish()
   cl.enqueue_copy(queue, partial_np, partial_buf)

   pi_approx = np.sum(partial_np)
   end = time.time()

   print(f"Pi ≈ {pi_approx}")
   print(f"Greška: {abs(pi_approx - math.pi)}")
   print(f"Vrijeme izvođenja: {end - start} s")

   # start_serial = time.time()
   # pi_seq = pi_serial(N)
   # end_serial = time.time()
   # print(f"[Serijski] Pi ≈ {pi_seq}, Greška = {abs(pi_seq - math.pi)}")
   # print(f"[Serijski] Vrijeme: {end_serial - start_serial} s")
   # print(f"Ubrzanje (serial / OpenCL): {(end_serial - start_serial)/(end - start)}")
   # za provjeru ubrzanja stavi 100 milja umjesto mlrfd
   # ubrzanje bi trebalo bit oko 520

if __name__ == "__main__":
   main()