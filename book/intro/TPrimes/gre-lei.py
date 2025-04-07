#!/bin/env python3
import time


def compute_gregory_pi(max_iter=100000000):
    start_time = time.time()
    true_pi = "3.14159265358979"

    pi_sum = 0.0
    step = 100

    # Process terms directly without storing
    for i in range(max_iter):
        # Calculate current term: (-1)^n / (2n + 1)
        term = (-1.0)**i / (2.0*i + 1.0)
        pi_sum += term

        # Check convergence every step iterations
        if i % step == 0:
            approx = pi_sum * 4.0
            if 3.141592653589793 < approx < 3.141592653589794:
                break

    final_pi = pi_sum * 4.0
    calc_pi = f"{final_pi:.14f}"

    # Compare digits and print matching ones
    matching = ""
    for j, (true_digit, calc_digit) in enumerate(zip(true_pi, calc_pi)):
        if true_digit == calc_digit:
            matching += true_digit
        else:
            break

    # Print matching digits and iteration count
    print(f"{matching} : {i}")

    # Print runtime
    print(f"{(time.time() - start_time):.4f}")

    return final_pi


# Run the function
if __name__ == "__main__":
    result = compute_gregory_pi()
