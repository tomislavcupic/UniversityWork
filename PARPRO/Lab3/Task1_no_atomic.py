import pyopencl as cl
import numpy as np
import time

KERNEL_CODE = """
__kernel void count_primes_no_atomic(__global const int* data,
                                     __global int* partial_counts,
                                     int N) {
    int gid = get_global_id(0);
    int size = get_global_size(0);
    int local_count = 0;

    for (int i = gid; i < N; i += size) {
        int num = data[i];
        if (num < 2) continue;
        int is_prime = 1;
        for (int j = 2; j * j <= num; ++j) {
            if (num % j == 0) {
                is_prime = 0;
                break;
            }
        }
        if (is_prime) {
            local_count++;
        }
    }

    // Svaka dretva piše u svoje mjesto
    partial_counts[gid] = local_count;
}
"""

def main():
    N = 2**25
    global_size = 2**19
    local_size = 128

    data_np = np.arange(N).astype(np.int32)

    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)
    mf = cl.mem_flags
    data_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=data_np)
    partial_counts_np = np.zeros(global_size, dtype=np.int32)
    partial_buf = cl.Buffer(ctx, mf.WRITE_ONLY, partial_counts_np.nbytes)

    program = cl.Program(ctx, KERNEL_CODE).build()
    start = time.time()

    program.count_primes_no_atomic(queue, (global_size,), (local_size,), data_buf, partial_buf, np.int32(N))

    queue.finish()
    end = time.time()

    cl.enqueue_copy(queue, partial_counts_np, partial_buf)
    total_primes = np.sum(partial_counts_np)

    print(f"Broj prostih brojeva u prvih {N} prirodnih brojeva: {total_primes}")
    print(f"Vrijeme izvođenja (bez atomic_add): {end - start:.4f} sekundi")
    print(f"G = {global_size}, L = {local_size}")

if __name__ == "__main__":
    main()