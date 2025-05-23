#!/bin/bash
# =============================================================================
# regen_trigram_phrase_BATCH.sh - I Ching Trigram Phrase Batch Generator
# =============================================================================
#
# Description:
#   This script automates the regeneration of trigram phrases for all hexagrams
#   from 1 to 64. It iterates through each hexagram number, calling
#   regen_trigram_phrase.py for each one to generate new interpretations of
#   the upper and lower trigram combinations.
#
# Usage:
#   ./regen_trigram_phrase_BATCH.sh
#
# Process:
#   1. Loops through hexagram numbers 1 to 64
#   2. Formats each number with leading zeros (01, 02, etc.)
#   3. Calls regen_trigram_phrase.py with --save flag for each hexagram
#
# Dependencies:
#   - regen_trigram_phrase.py script in same directory
#   - Python environment with required packages
#
# File Structure:
#   - Input/Output: ../regen/<hexagram_number>.json
#
# Author: JW
# Last Updated: 2024
# =============================================================================

# Loop from 1 to 64
for i in $(seq -f "%02g" 1 64); do
    # Execute the command with the current number
    ./regen_history.py --filename ../regen/${i}.json --provider openai --save
done
