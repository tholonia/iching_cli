#!/bin/env python3
import time
from colorama import init, Fore, Style
import math

# Initialize colorama
init()

# Color shortcuts
G, R, B, Y, M, C, X = (
    Fore.GREEN,
    Fore.RED,
    Fore.BLUE,
    Fore.YELLOW,
    Fore.MAGENTA,
    Fore.CYAN,
    Style.RESET_ALL,
)

# Mathematical constants
CONSTANTS = {
    "pi": {
        "value": 3.1415926535,
        "symbol": "π",
        "offset": 0,
        "init": {"parent": 1, "inst": 2, "limit": 3, "contrib": 5, "mult": 4},
    },

}



for i in range(0,1000000,4):
    ic = 1/i


def calculate_next(
    constant_type, PARENT, LIMITATION, CONTRIBUTION, count, INSTANTIATION=2
):
    """Calculate next value based on constant type"""
    if constant_type == "pi":
        CHILD = PARENT - (1 / LIMITATION) * (1 / CONTRIBUTION)
        LIMITATION += INSTANTIATION**INSTANTIATION
        CONTRIBUTION += INSTANTIATION * INSTANTIATION

        uCHILD = (LIMITATION + CONTRIBUTION)

        print(uCHILD, uCHILD * 4, 1/uCHILD, 1/(uCHILD*4))

        return CHILD, LIMITATION, CONTRIBUTION, uCHILD


def compute_tholonic_constant(constant_type, max_iter=1000, places=5):
    """Calculate mathematical constants using tholonic algorithms"""

    const = CONSTANTS[constant_type]
    true_value = str(const["value"])
    target_min = 3.1415926  # Minimum target value
    target_max = 3.14159261  # Maximum target value

    start_time = time.time()
    init = const["init"]

    # Initialize values
    PARENT = init["parent"]
    INSTANTIATION = init["inst"]
    LIMITATION = init["limit"]
    CONTRIBUTION = init["contrib"]
    multiplier = init["mult"]

    for count in range(max_iter):
        # Calculate next values
        PARENT, LIMITATION, CONTRIBUTION, uCHILD = calculate_next(
            constant_type, PARENT, LIMITATION, CONTRIBUTION, count, INSTANTIATION
        )

        current_value = PARENT * multiplier
        if target_min <= current_value < target_max:
            current_result = str(current_value)
            matching_digits = ""
            for i in range(min(len(current_result), len(true_value))):
                if current_result[i] == true_value[i]:
                    matching_digits += current_result[i]
                else:
                    break
            elapsed_time = time.time() - start_time
            print(
                G + f"{const['symbol']:>{col_var}} {matching_digits:<{col_res}} {str(count):<{col_count}} {elapsed_time:<{col_time}.2f}" + X
            )
            return current_value

    # If we didn't reach the target range
    elapsed_time = time.time() - start_time
    current_result = str(PARENT * multiplier)
    matching_digits = ""
    for i in range(min(len(current_result), len(true_value))):
        if current_result[i] == true_value[i]:
            matching_digits += current_result[i]
        else:
            break
    print(
        R + f"{const['symbol']:>{col_var}} {matching_digits:<{col_res}} {str(count):<{col_count}} {elapsed_time:<{col_time}.2f}" + X
    )
    return PARENT * multiplier


if __name__ == "__main__":
    places = 7

    # Define column widths
    col_var = 6  # Width for variable name
    col_res = 12  # Width for result (includes decimal places)
    col_count = 10  # Width for iteration count
    col_time = 8  # Width for time

    # Print header with consistent column widths
    print(
        f"{'Var':>{col_var}} {'Value':<{col_res}} {'Iters':<{col_count}} {'Time':<{col_time}}"
    )
    print(
        f"{'-'*4:>{col_var}} {'-'*8:<{col_res}} {'-'*6:<{col_count}} {'-'*6:<{col_time}}"
    )

    for const_type in CONSTANTS:
        compute_tholonic_constant(const_type, places=places)
