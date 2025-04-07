#!/bin/env python3
import time
from numba import cuda
import numpy as np


@cuda.jit
def pi_kernel(N_k, sum_d, prod_c, h2, h2x2, results):
    """
    CUDA kernel for parallel pi calculation using the Tholonic series
    """
    idx = cuda.grid(1)
    stride = cuda.gridsize(1)

    # Each thread processes a smaller chunk of iterations
    for i in range(idx, 100000, stride):
        # Update N_k based on the Tholonic series
        N_k[0] = N_k[0] - (1.0 / sum_d[0]) + (1.0 / prod_c[0])
        sum_d[0] += h2
        prod_c[0] += h2x2


def compute_tholonic_pi():
    """
    GPU-accelerated pi calculation
    """
    start_time = time.time()
    true_pi = "3.14159265358979323846264338327950288419716939937510582097494459230781640628620899"

    # Initialize arrays on GPU
    N_k = cuda.to_device(np.array([1.0], dtype=np.float64))
    sum_d = cuda.to_device(np.array([3.0], dtype=np.float64))
    prod_c = cuda.to_device(np.array([5.0], dtype=np.float64))
    h2 = 4.0
    h2x2 = 4.0
    results = cuda.device_array(1, dtype=np.float64)

    # Set up CUDA grid
    threadsperblock = 256
    blockspergrid = (1000000 + (threadsperblock - 1)) // threadsperblock
    iterations = 0  # Initialize iterations here
    last_matching = ""

    try:
        while True:
            print(f"Launching kernel at iteration {iterations}")
            pi_kernel[blockspergrid, threadsperblock](
                N_k, sum_d, prod_c, h2, h2x2, results
            )
            print(f"Kernel completed at iteration {iterations}")
            iterations += 1000000

            # Check every 10 million iterations
            if iterations % 10000000 == 0:
                # Get result from GPU
                final_pi = N_k.copy_to_host()[0] * 4.0
                calc_pi = f"{final_pi:.50f}"  # Increase precision

                # Debug: Print intermediate values
                print(f"Debug: N_k = {N_k.copy_to_host()[0]}, sum_d = {sum_d.copy_to_host()[0]}, prod_c = {prod_c.copy_to_host()[0]}")
                print(f"Debug: Calculated π = {calc_pi}")

                # Compare digits and print matching ones
                matching = ""
                for i, (true_digit, calc_digit) in enumerate(zip(true_pi, calc_pi)):
                    if true_digit == calc_digit:
                        matching += true_digit
                    else:
                        break

                # Print current status regardless of changes
                print(f"Iterations: {iterations:,}, Matching digits: {matching}")

    except KeyboardInterrupt:
        print("\nCalculation stopped by user")
        final_pi = N_k.copy_to_host()[0] * 4.0
        return final_pi


if __name__ == "__main__":
    compute_tholonic_pi()
