#!/bin/env python3


def compute_tholonic_pi(N_k_init, h_step_init, sum_d_init, prod_c_init, max_iter=1000000):
    # Initial conditions based on input parameters
    N_k = N_k_init
    h_step = h_step_init
    sum_d = sum_d_init
    prod_c = prod_c_init

    for count in range(max_iter):
        # Refinement step: Update N_k based on division and summation rules
        N_next = N_k - (1 / sum_d) + (1 / prod_c)

        # Update values for the next iteration
        N_k = N_next
        sum_d += h_step ** 2
        prod_c += h_step * 2

    # Final result
    print(f"N_k={N_k_init}, h_step={h_step_init}, sum_d={sum_d_init}, prod_c={prod_c_init}: Result = {N_k * 4}")
    return N_k * 4


# Loop through different initial values
for i in range(1, 8):  # 1 to 7
    for j in range(1, 8):
        for k in range(1, 8):
            for l in range(1, 8):
                result = compute_tholonic_pi(
                    N_k_init=i,
                    h_step_init=j,
                    sum_d_init=k,
                    prod_c_init=l
                )
