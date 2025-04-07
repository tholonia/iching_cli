#!/bin/env python3


def compute_tholonic_pi(max_iter=1000000, tol=1e-10):
    # Initial conditions based on the Tholonic model diagram
    N_k = 1  # Starting value (analogous to N_0 in the diagram)
    h_step = 2  # Increment step for updating sum_d and prod_c in each iteration
    sum_d = 3  # Divisor term d (related to CN = 3 in the diagram)
    prod_c = 5  # Divisor term c (related to ND = 5 in the diagram)

    for count in range(max_iter):
        # Refinement step: Update N_k based on division and summation rules
        N_next = N_k + (1 / prod_c) - (1 / sum_d)

        # Update values for the next iteration
        N_k = N_next  # Set new N_k for the next step
        sum_d += h_step ** 2  # Increment sum_d (analogous to adding h²)
        prod_c += h_step * 2  # Increment prod_c (analogous to adding 2h)

        # Print progress every 1000 iterations
        if count % 1000 == 0:
            # print(f"Iteration {count}: π approximation = {N_next * 4}")

            # Check if the approximation is close enough to π
            if abs(N_next * 4 - 3.141592653589793) < tol:
                print(f"Converged at iteration {count}: π ≈ {N_next * 4}")
                return N_next * 4  # Return the computed approximation of π

    # If max iterations are reached without convergence
    print("Max iterations reached. Approximate π:", N_k * 4)
    return N_k * 4


# Run the optimized function
compute_tholonic_pi()
