#!/bin/env python3


def compute_tholonic_phi(max_iter=1000000):
    # Initial conditions modified for phi calculation
    # Phi is related to the ratio of consecutive Fibonacci numbers
    # and can be expressed as (1 + √5) / 2
    N_k = 1  # Starting value
    h_step = 1  # Using smaller step for phi
    sum_d = 2  # Using smaller divisor
    prod_c = 3  # Using smaller multiplier

    for count in range(max_iter):
        # Modified formula to approach phi
        # Using the relationship that phi = 1 + 1/phi
        N_next = 1 + (1 / N_k)

        # Update values for the next iteration
        N_k = N_next
        sum_d += h_step  # Linear growth
        prod_c += h_step  # Linear growth

        # Print progress every 1000 iterations
        if count % 1000 == 0:
            print(f"Iteration {count}: φ = {N_next}")

    # Final result
    print("Final Result (φ):", N_k)
    return N_k


# Run the function
compute_tholonic_phi()
