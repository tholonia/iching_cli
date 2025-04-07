#!/bin/env python3
import time

def compute_tholonic_pi():
    """
    Ultra-optimized pi calculation using minimal operations.
    """
    start_time = time.time()
    true_pi = "3.14159265358979323846264338327950288419716939937510582097494459230781640628620899"

    N = 1.0
    h=2
    hp2 = h**2  # h_step²
    ht2 = h*2  # h_step * 2
    D = 3.0
    C = 5.0
    iterations = 0

    # Print the initial value of π
    initial_pi = N * 4.0
    print(f"Initial π approximation: {initial_pi:.14f}")

    try:
        # Infinite loop
        while True:
            N = N - (1.0 / D) + (1.0 / C)
            D += hp2
            C += ht2
            iterations += 1

            if iterations % 50000000 == 0:  # Check every 50 million iterations
                final_pi = N * 4.0
                calc_pi = f"{final_pi:.14f}"

                # Compare digits and print matching ones
                matching = ""
                for i, (true_digit, calc_digit) in enumerate(zip(true_pi, calc_pi)):
                    if true_digit == calc_digit:
                        matching += true_digit
                    else:
                        break

                # Print matching digits and iteration count
                print(f"{matching} : {iterations}")

    except KeyboardInterrupt:
        print("\nCalculation stopped by user")
        final_pi = N * 4.0
        return final_pi

if __name__ == "__main__":
    compute_tholonic_pi()
