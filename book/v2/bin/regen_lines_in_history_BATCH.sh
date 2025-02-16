#!/bin/bash

# =============================================================================
# regen_lines_in_history_BATCH.sh - I Ching Line History Regenerator
# =============================================================================
#
# Description:
#   This script automates the regeneration of line history data for all
#   hexagrams from 2 to 64. It iterates through each hexagram number,
#   calling regen_lines_in_history.py for each one.
#
# Usage:
#   ./regen_lines_in_history_BATCH.sh
#
# Process:
#   1. Loops through hexagram numbers 2 to 64
#   2. Formats each number with leading zeros (02, 03, etc.)
#   3. Calls regen_lines_in_history.py for each hexagram
#
# Dependencies:
#   - regen_lines_in_history.py script in same directory
#   - Python environment with required packages
#
# File Structure:
#   - Input/Output: ../regen/<hexagram_number>.json
#
# Author: JW
# Last Updated: 2024
# =============================================================================

# Loop from 1 to 64
for i in $(seq -f "%02g" 2 64); do
    # Execute the command with the current number
    ./regen_lines_in_history.py ../regen $i
done
