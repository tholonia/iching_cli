#!/bin/env python3


def compute_tholonic_constant(constant_type="pi", max_iter=1000000):
    """
    Calculate various mathematical constants using tholonic algorithm variations

    Constants:
    - "pi": π (3.14159...)
    - "phi": φ Golden ratio (1.61803...)
    - "e": Euler's number (2.71828...)
    - "sqrt2": Square root of 2 (1.41421...)
    - "ln2": Natural log of 2 (0.69314...)
    """

    # Initial conditions vary based on constant
    if constant_type == "pi":
        N_k = 1
        h_step = 2
        sum_d = 3
        prod_c = 5
        multiplier = 4  # Final result multiplier

    elif constant_type == "phi":
        N_k = 1
        h_step = 1
        sum_d = 1
        prod_c = 2
        multiplier = 1

    elif constant_type == "e":
        N_k = 2
        h_step = 1
        sum_d = 1
        prod_c = 1
        multiplier = 1

    elif constant_type == "sqrt2":
        N_k = 1
        h_step = 1
        sum_d = 2
        prod_c = 2
        multiplier = 1

    elif constant_type == "ln2":
        N_k = 0.5
        h_step = 1
        sum_d = 1
        prod_c = 2
        multiplier = 1

    for count in range(max_iter):
        if constant_type == "pi":
            N_next = N_k - (1 / sum_d) + (1 / prod_c)
            sum_d += h_step**2
            prod_c += h_step * 2

        elif constant_type == "phi":
            N_next = 1 + (1 / N_k)
            temp = prod_c
            prod_c = prod_c + sum_d
            sum_d = temp

        elif constant_type == "e":
            N_next = N_k + (1 / prod_c)
            prod_c *= count + 1 if count > 0 else 1

        elif constant_type == "sqrt2":
            N_next = (N_k + (2 / N_k)) / 2

        elif constant_type == "ln2":
            N_next = (
                N_k + (1 / (count + 1)) if count % 2 == 0 else N_k - (1 / (count + 1))
            )

        N_k = N_next

        if count % 1000 == 0:
            print(f"Iteration {count}: Result = {N_k * multiplier}")

    print(f"Final {constant_type} Result:", N_k * multiplier)
    return N_k * multiplier


# Example usage:
print("\nCalculating π:")
compute_tholonic_constant("pi")

print("\nCalculating φ (Golden Ratio):")
compute_tholonic_constant("phi")

print("\nCalculating e (Euler's number):")
compute_tholonic_constant("e")

print("\nCalculating √2:")
compute_tholonic_constant("sqrt2")

print("\nCalculating ln(2):")
compute_tholonic_constant("ln2")
