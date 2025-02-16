#!/bin/bash

# =============================================================================
# get_new_hex_desc_LOCAL_BATCH.sh - I Ching Hexagram Description Generator
# =============================================================================
#
# Description:
#   This script automates the generation of hexagram descriptions by iterating
#   through all 64 hexagrams. For each hexagram, it calls the
#   get_new_hex_desc_LOCAL.py script to generate and save descriptions.
#
# Usage:
#   ./get_new_hex_desc_LOCAL_BATCH.sh
#
# Process:
#   1. Loops through numbers 1-64
#   2. For each number, formats it with leading zeros (01, 02, etc.)
#   3. Calls get_new_hex_desc_LOCAL.py with the formatted number
#   4. Automatically saves results (--save flag)
#
# Dependencies:
#   - get_new_hex_desc_LOCAL.py script in same directory
#   - Python environment with required packages
#
# Note:
#   This is a batch processing script that will process all hexagrams
#   sequentially. Ensure enough time and resources are available for
#   complete processing.
#
# Author: JW
# Last Updated: 2024
# =============================================================================

# Loop from 1 to 64
for i in $(seq -f "%02g" 1 64); do
    # Execute the command with the current number
    ./get_new_hex_desc_LOCAL.py "$i" --save
done
