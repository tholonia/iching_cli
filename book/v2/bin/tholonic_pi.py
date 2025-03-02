#!/bin/env python3
def tholonic_pi(N, k, max_iter):
    # Constants from the diagram
    n = 2  # DC
    c = 5  # ND
    d = 3  # CN

    # Compute C_k and D_k from the formulas
    C_k = (N / d) + (n ** n)
    D_k = (N / c) + (n ** n)

    # Compute the next N_k
    N_next = (N * D_k) + C_k

    # Print intermediate values
    print(f"Iteration {k}: N_k = {N_next} | Approximation of π = {N_next}")

    # Stop condition
    if k >= max_iter or abs(N_next - 3.141592653589793) < 1e-10:
        print("Final approximation:", N_next)
        return N_next

    # Recursive call
    return tholonic_pi(N_next, k + 1, max_iter)

# Run the function with initial N_0 = 1, max 50 iterations
tholonic_pi(1, 1, 50)
