#!/bin/env python3
import time
from colorama import init, Fore, Style

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

# Tholonic linear incremental recursion constants
CONSTANTS_LINEAR = {
    "phi_linear": {
        "value": 0.6180339887,
        "symbol": "1/φ",
        "offset": 0,
        "init": {"parent": 1, "limit": 2, "contrib": 3, "increment": 1},
    },
    "e_linear": {
        "value": 0.7182818285,
        "symbol": "e-2",
        "offset": 0,
        "init": {"parent": 2, "limit": 1, "contrib": 2, "increment": 1},
    },
    "ln2_linear": {
        "value": 0.6931471805,
        "symbol": "ln2",
        "offset": 0,
        "init": {"parent": 1, "limit": 1, "contrib": 2, "increment": 1},
    },
    "sqrt2_linear": {
        "value": 0.4142135623,
        "symbol": "√2-1",
        "offset": 0,
        "init": {"parent": 1, "limit": 2, "contrib": 4, "increment": 2},
    },
    "pi_linear": {
        "value": 3.1415926535,
        "symbol": "π",
        "offset": 0,
        "init": {"parent": 1, "limit": 3, "contrib": 5, "increment": 2},
    },
}


def calculate_next_linear(PARENT, LIMITATION, CONTRIBUTION, increment, count):
    CHILD = (
        PARENT
        + (1 / (LIMITATION + increment * count))
        - (1 / (CONTRIBUTION + increment * count))
    )
    return CHILD


def compute_linear_constant(constant_type, max_iter=1000000, places=10):
    const = CONSTANTS_LINEAR[constant_type]

    start_time = time.time()
    init = const["init"]

    PARENT = init["parent"]
    LIMITATION = init["limit"]
    CONTRIBUTION = init["contrib"]
    increment = init["increment"]

    for count in range(max_iter):
        CHILD = calculate_next_linear(
            PARENT, LIMITATION, CONTRIBUTION, increment, count
        )

        current_result = CHILD
        rounded_result = round(current_result, places)
        rounded_true = round(const["value"], places)

        if rounded_result == rounded_true:
            elapsed_time = time.time() - start_time
            print(
                f"{const['symbol']:>6} {rounded_result:<14.{places}f} {str(count):<10} {elapsed_time:<8.4f}"
            )
            return rounded_result

        PARENT = CHILD

    elapsed_time = time.time() - start_time
    final_result = round(PARENT, places)
    print(
        R
        + f"{const['symbol']:>6} {final_result:<14.{places}f} {str(count):<10} {elapsed_time:<8.4f}"
        + X
    )
    return final_result


if __name__ == "__main__":
    places = 10

    col_var = 6
    col_res = 14
    col_count = 10
    col_time = 8

    print(
        f"{'Var':>{col_var}} {'Value':<{col_res}} {'Iters':<{col_count}} {'Time':<{col_time}}"
    )
    print(f"{'-'*col_var} {'-'*col_res} {'-'*col_count} {'-'*col_time}")

    for const_type in CONSTANTS_LINEAR:
        compute_linear_constant(const_type, places=places)
