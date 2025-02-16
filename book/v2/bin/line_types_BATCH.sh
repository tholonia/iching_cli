#!/bin/bash

# =============================================================================
# line_types_BATCH.sh - I Ching Line Types Generator Batch Script
# =============================================================================
#
# Description:
#   This script automates the process of generating line types for all 64
#   hexagrams. It converts binary sequences into yin/yang line types and
#   updates or creates the line_type array in each hexagram's JSON file.
#
# Usage:
#   ./line_types_BATCH.sh
#
# Process:
#   1. Loops through hexagram numbers 1 to 64
#   2. Formats each number with leading zeros (01, 02, etc.)
#   3. Calls line_types.py for each hexagram with --save flag
#   4. Updates line_type array in corresponding JSON file
#
# Dependencies:
#   - line_types.py script in same directory
#   - Python environment with required packages
#   - Hexagram JSON files in ../regen/ directory
#
# File Structure:
#   - Input/Output: ../regen/XX.json
#     where XX is the hexagram number (01-64)
#
# Author: JW
# Last Updated: 2024
# =============================================================================

# Loop from 1 to 64
for i in $(seq -f "%02g" 1 64); do
    # Execute the command with the current number
    ./line_types.py ../regen/${i}.json --save
done
