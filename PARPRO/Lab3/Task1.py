import pyopencl as cl
import numpy as np
import time

KERNEL_CODE = """
__kernel void count_primes(__global const int* data, __global int* result, int N) {
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

    atomic_add(result, local_count);
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
    result_np = np.array([0], dtype=np.int32)
    result_buf = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=result_np)
    program = cl.Program(ctx, KERNEL_CODE).build()

    start = time.time()

    program.count_primes(queue, (global_size,), (local_size,), data_buf, result_buf, np.int32(N))

    queue.finish()
    end = time.time()

    cl.enqueue_copy(queue, result_np, result_buf)

    # with open("izlaz.txt", "a") as f:
    #     f.write(f"G = {global_size}, L = {local_size}, N = {N} ")
    #     f.write(f"Vrijeme izvođenja: {end - start} sekundi\n")
    print(f"Broj prostih brojeva u prvih {N} prirodnih brojeva: {result_np[0]}")
    print(f"Vrijeme izvođenja: {end - start} sekundi")
    print(f"G = {global_size}, L = {local_size}")

if __name__ == "__main__":
    main()