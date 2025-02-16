#!/bin/bash

# =============================================================================
# joe_BATCH.sh - I Ching Hexagram File Editor Batch Script
# =============================================================================
#
# Description:
#   This script automates the process of opening hexagram text files in sequence
#   using the Visual Studio Code editor. It iterates through hexagrams 23-64,
#   allowing for systematic review and editing of hexagram files.
#
# Usage:
#   ./joe_BATCH.sh
#
# Process:
#   1. Loops through hexagram numbers 23 to 64
#   2. Formats each number with leading zeros (e.g., 23 becomes "23")
#   3. Opens corresponding hexagram text file in VS Code
#
# Dependencies:
#   - Visual Studio Code (code command)
#   - Hexagram text files in /home/jw/src/iching_cli/defs/v2/
#
# File Structure:
#   - Input: /home/jw/src/iching_cli/defs/v2/XX_hex.txt
#     where XX is the hexagram number (23-64)
#
# Author: JW
# Last Updated: 2024
# =============================================================================

# Loop from 24 to 64
for i in $(seq -f "%02g" 23 64); do
    # Execute the command with the current number
    code /home/jw/src/iching_cli/defs/v2/${i}_hex.txt
done
