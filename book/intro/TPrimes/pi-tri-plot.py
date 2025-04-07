#!/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')

def compute_tholonic_pi(max_iter=100000000):
    # Arrays to store the component values
    Dary = []
    Cary = []
    Delta = []  # Array to store the difference

    # Initial conditions based on the Tholonic model diagram
    N_k = 1  # Starting value (analogous to N_0 in the diagram)
    h_step = 2  # Increment step for updating sum_d and prod_c in each iteration
    sum_d = 3  # Divisor term d (related to CN = 3 in the diagram)
    prod_c = 5  # Divisor term c (related to ND = 5 in the diagram)

    for count in range(max_iter):
        # Store component values
        d_val = 1/sum_d
        c_val = 1/prod_c
        Dary.append(d_val)
        Cary.append(c_val)
        Delta.append(c_val - d_val)  # Calculate and store the delta

        # Refinement step: Update N_k based on division and summation rules
        # print(N_k)
        N_next = N_k - (1 / sum_d) + (1 / prod_c)

        # Update values for the next iteration
        N_k = N_next  # Set new N_k for the next step
        sum_d += h_step ** 2  # Increment sum_d (analogous to adding h²)
        prod_c += h_step * 2  # Increment prod_c (analogous to adding 2h)

        if count % 1 == 0:
            print(f"Iteration {count}: Delta = {Delta[-1]}", N_next * 4)
        if N_next * 4 > 3.1415926 and N_next * 4 < 3.1415927: #53589793238462643383279502884197:
            print(count)
            exit()

    # Plot delta values
    plt.figure(figsize=(12, 8))
    plt.plot(Delta[1000:], 'r-', label='Delta (1/prod_c - 1/sum_d)', linewidth=2)
    plt.xlabel('Iterations')
    plt.ylabel('Delta Value')
    plt.title('Evolution of Delta between 1/prod_c and 1/sum_d')
    plt.grid(True)
    plt.legend()
    plt.show()

    return N_k * 4

# Run the optimized function
compute_tholonic_pi()
