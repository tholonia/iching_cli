#!/bin/env python3
import time
from colorama import init, Fore, Style

# Initialize colorama
init()

# Color shortcuts
G, R, B, Y, M, C, X = Fore.GREEN, Fore.RED, Fore.BLUE, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN, Style.RESET_ALL

# Mathematical constants
CONSTANTS = {
    "ln2": {
        "value": 1.6931471805,
        "symbol": "ln2",
        "offset": -1,
        "init": {"parent": 1, "inst": 2, "limit": 1, "contrib": 2, "mult": 1},
    },
    "pi": {
        "value": 3.1415926535,
        "symbol": "π",
        "offset": 0,
        "init": {"parent": 1, "inst": 2, "limit": 3, "contrib": 5, "mult": 4},
    },
    "phi": {
        "value": 1.6180339887,
        "symbol": "φ",
        "offset": 0,
        "init": {"parent": 1, "inst": 2, "limit": 2, "contrib": 3, "mult": 1},
    },
    "e": {
        # Initializing parent to 1 instead of 0 significantly reduces the computational time for convergence
        # without compromising accuracy, as it quickly moves closer to the target constant value.
        "value": 3.7182818284,
        "symbol": "e",
        "offset": 1,
        "init": {"parent": 1, "inst": 2, "limit": 1, "contrib": 1, "mult": 1},
    },
    "sqrt2": {
        "value": 1.4142135624,
        "symbol": "√2",
        "offset": 0,
        "init": {"parent": 1, "inst": 2, "limit": 2, "contrib": 2, "mult": 1},
    },
}

def calculate_next(constant_type, PARENT, LIMITATION, CONTRIBUTION, count, INSTANTIATION=2):
    """Calculate next value based on constant type"""
    if constant_type == "pi":
        CHILD = PARENT - (1/LIMITATION) + (1/CONTRIBUTION)
        LIMITATION += INSTANTIATION**INSTANTIATION
        CONTRIBUTION += INSTANTIATION * INSTANTIATION
        return CHILD, LIMITATION, CONTRIBUTION

    elif constant_type == "phi":
        CHILD = 1 + (1 / PARENT)
        temp = CONTRIBUTION
        CONTRIBUTION = CONTRIBUTION + LIMITATION
        LIMITATION = temp
        return CHILD, LIMITATION, CONTRIBUTION

    elif constant_type == "ORG phi":
        CHILD = 1 + (1 / PARENT)
        temp = CONTRIBUTION
        CONTRIBUTION = CONTRIBUTION + LIMITATION
        LIMITATION = temp
        return CHILD, LIMITATION, CONTRIBUTION

    elif constant_type == "e":
        CHILD = PARENT + (1 / CONTRIBUTION)
        CONTRIBUTION *= (count + 1) if count > 0 else 1
        return CHILD, LIMITATION, CONTRIBUTION

    elif constant_type == "sqrt2":
        CHILD = (PARENT + (2/PARENT))/2
        return CHILD, LIMITATION, CONTRIBUTION

    elif constant_type == "ln2":
        CHILD = PARENT + (1/(count + 1)) if count % 2 == 0 else PARENT - (1/(count + 1))
        return CHILD, LIMITATION, CONTRIBUTION

def compute_tholonic_constant(constant_type, max_iter=1000000, places=5):
    """Calculate mathematical constants using tholonic algorithms"""

    const = CONSTANTS[constant_type]

    start_time = time.time()
    init = const['init']

    # Initialize values
    PARENT = init['parent']
    INSTANTIATION = init['inst']
    LIMITATION = init['limit']
    CONTRIBUTION = init['contrib']
    multiplier = init['mult']


    for count in range(max_iter):
        # Calculate next values
        PARENT, LIMITATION, CONTRIBUTION = calculate_next(
            constant_type, PARENT, LIMITATION, CONTRIBUTION, count, INSTANTIATION
        )

        if count % 1 == 0:
            current_result = PARENT * multiplier
            rounded_result = round(current_result, places)

            # Handle comparison
            if const['value'] == 0:
                rounded_true = rounded_result
            else:
                rounded_true = round(const['value'], places)
                error = abs(current_result - const['value'])

            # Check for convergence
            if rounded_result == rounded_true:
                rounded_result += const['offset']
                elapsed_time = time.time() - start_time
                print(f"{const['symbol']:>{col_var}} {rounded_result:<{col_res}.{places}f} {str(count):<{col_count}} {elapsed_time:<{col_time}.2f}")
                return rounded_result

    # Handle non-convergence
    elapsed_time = time.time() - start_time
    final_result = round(PARENT * multiplier, places)
    print(R + f"{final_result:<{col_res}.{places}f} {str(count):<{col_count}} {elapsed_time:<{col_time}.2f}" + X)
    return final_result

if __name__ == "__main__":
    places = 6

    # Define column widths
    col_var = 6      # Width for variable name
    col_res = 12     # Width for result (includes decimal places)
    col_count = 10   # Width for iteration count
    col_time = 8     # Width for time

    # Print header with consistent column widths
    print(f"{'Var':>{col_var}} {'Value':<{col_res}} {'Iters':<{col_count}} {'Time':<{col_time}}")
    print(f"{'-'*4:>{col_var}} {'-'*8:<{col_res}} {'-'*6:<{col_count}} {'-'*6:<{col_time}}")

    for const_type in CONSTANTS:
        compute_tholonic_constant(const_type, places=places)
