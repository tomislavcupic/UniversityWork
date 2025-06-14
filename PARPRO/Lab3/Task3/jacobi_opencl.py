import pyopencl as cl
import numpy as np

def jacobi_opencl(psitmp, psi, m, n):
    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)
    mf = cl.mem_flags
    size = (m + 2) * (n + 2)

    psi_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=psi)
    psitmp_buf = cl.Buffer(ctx, mf.WRITE_ONLY, psi.nbytes)

    with open("jacobi.cl", "r") as f:
        kernel_src = f.read()

    program = cl.Program(ctx, kernel_src).build()
    kernel = program.jacobistep_kernel

    kernel.set_args(psitmp_buf, psi_buf, np.int32(m), np.int32(n))

    global_size = (m, n)
    cl.enqueue_nd_range_kernel(queue, kernel, global_size, None)
    cl.enqueue_copy(queue, psitmp, psitmp_buf)
    queue.finish()

    return psitmp
