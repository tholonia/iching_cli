#!/bin/env python
#!/usr/bin/env python3

from fractions import Fraction
import sys
from decimal import Decimal


def calculate_fraction(fraction1, fraction2):
    # Parse fractions that might contain decimals
    def parse_fraction(frac_str):
        if '/' in frac_str:
            num, denom = frac_str.split('/')
            # Convert to Decimal first to preserve precision
            if '.' in num:
                # For decimal numerator, create fraction directly from float
                return Fraction(str(Decimal(num))) / Fraction(str(Decimal(denom)))
            else:
                # For simple fractions
                return Fraction(int(num), int(denom))
        else:
            return Fraction(frac_str)

    # Convert input strings to Fraction objects
    frac1 = parse_fraction(fraction1)
    frac2 = parse_fraction(fraction2)

    # Perform the calculation: frac1 - frac2
    result = frac1 - frac2

    # Simplify and return result
    return result


if __name__ == "__main__":
    if len(sys.argv) != 3:
        # Loop 100 times, incrementing denominators by 4 each time
        for i in range(1000):
            denom1 = 5 + (i * 4)
            denom2 = 3 + (i * 4)

            fraction1 = f"1/{denom1}"
            fraction2 = f"1/{denom2}"

            final_result = calculate_fraction(fraction1, fraction2)

            # Calculate (denominator + 1) / 16
            denom_plus_one = final_result.denominator + 1
            special_value = denom_plus_one / 16

            print(f"Iteration {i+1}: {fraction1} - {fraction2} = {final_result.numerator}/{final_result.denominator} --> ({denom_plus_one}/16 = {special_value})")
    else:
        fraction1, fraction2 = sys.argv[1], sys.argv[2]
        final_result = calculate_fraction(fraction1, fraction2)

        # Calculate (denominator + 1) / 16
        denom_plus_one = final_result.denominator + 1
        special_value = denom_plus_one / 16

        print(f"Result: {final_result.numerator}/{final_result.denominator} --> ({denom_plus_one}/16 = {special_value})")
