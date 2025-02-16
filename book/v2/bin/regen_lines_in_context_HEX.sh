#!/bin/bash

# =============================================================================
# regen_lines_in_context_HEX.sh - I Ching Hexagram Line Context Generator
# =============================================================================
#
# Description:
#   This script regenerates line context data for a specific I Ching hexagram.
#   It processes each line (0-2) of the specified hexagram, updating the
#   contextual information in the corresponding files.
#
# Usage:
#   ./regen_lines_in_context_HEX.sh <hexagram_number>
#
# Arguments:
#   hexagram_number: Number of the hexagram (1-64)
#
# Examples:
#   ./regen_lines_in_context_HEX.sh 1    # Process hexagram 1
#
# Process:
#   1. Validates input hexagram number (1-64)
#   2. For each line (0-2):
#      - Calls regen_lines_in_context.py
#      - Updates context data in ../regen directory
#
# Dependencies:
#   - regen_lines_in_context.py script
#   - Python environment with required packages
#
# File Structure:
#   - Input/Output: ../regen/<hexagram_number>_*.json
#
# Error Handling:
#   - Validates number of arguments
#   - Ensures hexagram number is valid integer
#   - Checks range (1-64)
#
# Author: JW
# Last Updated: 2024
# =============================================================================

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

