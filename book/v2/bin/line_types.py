#!/bin/env python
"""
=============================================================================
line_types.py - I Ching Line Type Generator
=============================================================================

Description:
  This script processes hexagram JSON files to create or update line_type
  values based on binary sequences. It converts 6-digit binary numbers into
  an array of yin/yang symbols (⚊/⚋) for each hexagram.

Usage:
  ./line_types.py <json_file> [--save]

Arguments:
  json_file: Path to the hexagram JSON file to process
  --save: Optional flag to save changes back to the JSON file

Examples:
  ./line_types.py hexagram.json         # Display output only
  ./line_types.py hexagram.json --save  # Update JSON file

Process:
  1. Reads binary_sequence from input JSON file
  2. Converts to 6-digit binary string with zero padding
  3. Maps binary digits to yin/yang symbols (1->⚊, 0->⚋)
  4. Updates line_type array in JSON
  5. Optionally saves back to file

Dependencies:
  - Python 3.x
  - Required modules: json, argparse, sys

File Structure:
  - Input/Output: JSON file containing:
    - binary_sequence: Integer (0-63)
    - line_type: Array of 6 symbols

Author: JW
Last Updated: 2024
=============================================================================
"""
import json
import argparse
import sys

def binary_to_line_types(binary_sequence):
    # Convert to 6-digit binary string with zero padding
    binary_str = format(binary_sequence, '06b')
    # Reverse the string to match line ordering (line 1 at index 0)
    # binary_str = binary_str[::-1]

    # Convert binary digits to yin/yang values
    line_types = []
    for bit in binary_str:
        # line_types.append("Yang" if bit == "1" else "Yin")
        line_types.append("⚊" if bit == "1" else "⚋")

    return line_types

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process JSON file to create line_type values.")
    parser.add_argument("json_file", help="Path to the JSON file to process")
    parser.add_argument("--save", action="store_true", help="Save changes back to the JSON file")
    args = parser.parse_args()

    try:
        # Read the JSON file
        with open(args.json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Get binary sequence
        binary_sequence = data.get('binary_sequence')
        if binary_sequence is None:
            print("Error: No binary_sequence found in JSON file")
            sys.exit(1)

        # Convert binary sequence to line types
        line_types = binary_to_line_types(binary_sequence)

        data['line_type'] = line_types

        if args.save:
            # Save updated JSON back to file
            with open(args.json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Updated JSON file saved: {args.json_file}")
        else:
            # Print the updated JSON
            print(json.dumps(data, indent=4, ensure_ascii=False))

    except FileNotFoundError:
        print(f"Error: File not found: {args.json_file}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON file: {args.json_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()