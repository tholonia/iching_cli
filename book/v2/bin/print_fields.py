#!/usr/bin/env python3

"""
=============================================================================
print_fields.py - I Ching Hexagram Field Extractor
=============================================================================

Description:
  This script extracts and displays specific fields from hexagram JSON files.
  It focuses on the "lines_in_transition" data, showing the first four words
  of each line's description for quick reference and verification.

Usage:
  ./print_fields.py

Process:
  1. Scans ../_v2 directory for JSON files
  2. For each hexagram file:
     - Extracts "lines_in_transition" data
     - Shows first four words for lines 1-6
     - Displays in order by hexagram number

Dependencies:
  - Python 3.x
  - Required modules: json, os

File Structure:
  Input:
    - ../_v2/*.json: Hexagram JSON files
  Output Format:
    --- filename.json ---
    [first four words of line 6]
    [first four words of line 5]
    ...etc

Author: JW
Last Updated: 2024
=============================================================================
"""
import os
import json

# Define the folder containing the JSON files
folder_path = "../_v2"

# Define the specific keys to extract from "lines_in_transition"
keys = ["6", "5", "4", "3", "2", "1"]

# Iterate over each file in the folder
for filename in sorted(os.listdir(folder_path)):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)

        # Open and parse the JSON file
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Extract and print the values from lines_in_transition
        try:
            print(f"\n--- {filename} ---")
            for key in keys:
                if key in data["hx"]["core"]["lines_in_transition"]:
                    # Get the value and print only the first four words
                    value = data["hx"]["core"]["lines_in_transition"][key]
                    first_four_words = ' '.join(value.split()[:4])
                    print(first_four_words)
        except KeyError:
            print(f"Warning: {filename} does not contain expected structure.")
