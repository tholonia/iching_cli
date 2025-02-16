#!/usr/bin/python3

"""
=============================================================================
hexbinvals.py - Hexagram Binary Value Extractor
=============================================================================

Description:
  This script extracts and displays hexagram binary sequences and their
  corresponding hex values from JSON files. It processes one or more hexagram
  numbers provided as command-line arguments.

Usage:
  python hexbinvals.py num1,num2,num3,...
  Example: python hexbinvals.py 1,2,3

Arguments:
  numbers: Comma-separated list of hexagram numbers to process
          Numbers will be zero-padded to two digits (1 -> "01")

Process:
  1. Accepts comma-separated hexagram numbers from command line
  2. Converts numbers to zero-padded two-digit strings
  3. Loads corresponding JSON files from regen directory
  4. Extracts hex ID and binary sequence for each hexagram
  5. Displays results in format: "Hex X = binary_sequence"

Dependencies:
  - json: JSON file parsing
  - pathlib: Cross-platform path handling
  - sys: Command line argument processing

File Structure:
  Input:
    - ../regen/XX.json: Hexagram data files where XX is hexagram number
    Each JSON file contains:
      - id: Hexagram identifier
      - binary_sequence: Binary representation of hexagram

Output Format:
  Hex <id> = <binary_sequence>
  Example: "Hex 01 = 111111"

Error Handling:
  - Validates command line arguments
  - Checks for file existence
  - Verifies JSON structure
  - Reports specific error messages for each failure case

Author: JW
Last Updated: 2024
=============================================================================
"""

import sys
import json
import os
from pathlib import Path

def pad_number(num):
    """Convert integer to zero-padded two digit string"""
    return str(num).zfill(2)

def read_json_file(filepath):
    """Read and parse JSON file"""
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File {filepath} not found")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file {filepath}")
        return None

def main():
    # Check if arguments were provided
    if len(sys.argv) < 2:
        print("Usage: python script.py num1,num2,num3,...")
        sys.exit(1)

    # Get the numbers from command line and split by comma
    try:
        numbers = [int(x.strip()) for x in sys.argv[1].split(',')]
    except ValueError:
        print("Error: Please provide valid integers separated by commas")
        sys.exit(1)

    # Convert numbers to padded strings
    padded_numbers = [pad_number(num) for num in numbers]

    # Get the parent directory
    parent_dir = Path(__file__).parent.parent

    # Process each number
    for num in padded_numbers:
        # Construct the filepath
        filepath = parent_dir / "regen" / f"{num}.json"

        # Read the JSON file
        data = read_json_file(filepath)

        if data:
            try:
                hexval = data['id']
                binval = data['binary_sequence']
                print(f"Hex {hexval} = {binval}")
            except KeyError as e:
                print(f"Error: Missing required key {e} in file {filepath}")

if __name__ == "__main__":
    main()