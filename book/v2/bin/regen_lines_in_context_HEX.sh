#!/bin/bash

# This script regenerates lines in context for a specific I Ching hexagram.
# It requires exactly one argument: the hexagram number (an integer between 1 and 64).
#
# Usage:
#   ./regen_lines_in_context_HEX.sh <hexagram_number>
#
# Example:
#   ./regen_lines_in_context_HEX.sh 1

# Check if exactly one argument is provided
if [ "$#" -ne 1 ]; then
    echo "Error: Exactly one argument is required."
    echo "Usage: ./regen_lines_in_context_HEX.sh <hexagram_number>"
    exit 1
fi

# Check if the argument is an integer
if ! [[ "$1" =~ ^[0-9]+$ ]]; then
    echo "Error: Argument must be an integer."
    exit 1
fi

# Check if the integer is between 1 and 64
if [ "$1" -lt 1 ] || [ "$1" -gt 64 ]; then
    echo "Error: Hexagram number must be between 1 and 64."
    exit 1
fi

# Run the Python script with the provided hexagram number
./regen_lines_in_context.py ../regen "$1" 0
./regen_lines_in_context.py ../regen "$1" 1
./regen_lines_in_context.py ../regen "$1" 2

