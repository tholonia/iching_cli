#!/bin/bash

# =============================================================================
# regen_gen_phrase_BATCH.sh - Batch Process I Ching Trigram Phrases
# =============================================================================
#
# Description:
#   This script automates the process of generating general trigram phrases
#   for all I Ching hexagrams. It processes each JSON file in the regen
#   directory, combining multiple philosophical perspectives into a single
#   comprehensive description.
#
# Usage:
#   ./regen_gen_phrase_BATCH.sh
#
# Process:
#   1. Checks for existence of regen directory
#   2. Iterates through all JSON files in directory
#   3. For each file:
#      - Calls regen_trigrams_phrase_general.py with --save flag
#      - Updates JSON with new general phrase and explanation
#      - Shows progress and completion status
#
# Dependencies:
#   - regen_trigrams_phrase_general.py must be in same directory
#   - JSON files must exist in ../regen directory
#   - OpenAI API key must be set in environment
#
# Input:
#   - ../regen/*.json files containing hexagram data
#
# Output:
#   - Updated JSON files with new general phrases
#   - Progress messages for each file processed
#
# Error Handling:
#   - Checks directory existence
#   - Validates file existence
#   - Shows clear error messages
#
# Author: JW
# Last Updated: 2024
# =============================================================================

# Directory containing JSON files
REGEN_DIR="../regen"

# Check if directory exists
if [ ! -d "$REGEN_DIR" ]; then
    echo "Error: Directory $REGEN_DIR not found"
    exit 1
fi

# Process each JSON file
for FILENAME in "$REGEN_DIR"/*.json; do
    if [ -f "$FILENAME" ]; then
        echo "Processing: $FILENAME"
        ./regen_tri_gen_phrase.py "$FILENAME" --save
        echo "----------------------------------------"
    fi
done

echo "All files processed"