#!/bin/env python3

#!/usr/bin/env python3
import math


def calculate_pi_tholonic(iterations=1000000):
    """Calculate pi using the Tholonic perfect-square series explicitly."""
    total = 1.0  # Start with initial 1
    for n in range(1, iterations + 1):
        total -= 2 / (16 * n**2 - 1)
    pi_approx = 4 * total
    return pi_approx


def get_matching_digits(calculated, actual):
    """Return only the digits that match between calculated and actual π."""
    calc_str = str(calculated)
    actual_str = str(actual)

    matching = ""
    for i in range(min(len(calc_str), len(actual_str))):
        if calc_str[i] == actual_str[i]:
            matching += calc_str[i]
        else:
            break

    return matching


# Example usage explicitly
if __name__ == "__main__":
    iterations = 100000000  # Higher number of iterations increases accuracy
    pi_estimate = calculate_pi_tholonic(iterations)

    # Get and display only matching digits
    matching_digits = get_matching_digits(pi_estimate, math.pi)

    print(f"Calculated π (matching digits only): {matching_digits}")
    print(f"Number of correct digits: {len(matching_digits)}")
    print(f"Using {iterations} iterations")
    print(f"Error: {abs(math.pi - pi_estimate)}")
