#!/bin/env python
"""
=============================================================================
get_binhex_json.py - Hexagram JSON Data Extractor
=============================================================================

Description:
    Reads all JSON files from ../regen directory and extracts specific values
    including hexagram ID, code, name, and binary sequence.

Usage:
    python get_binhex_json.py

Input Files:
    - All JSON files in ../regen directory with structure:
      {
          "id": int,
          "hexagram_code": str,
          "name": str,
          "binary_sequence": int
      }

Output:
    Pretty prints sorted array of hexagram data:
    [id, hexagram_code, binary_sequence, name]

Functions:
    read_hexagram_info(file_path)
        - Reads JSON file and extracts hexagram information
        - Handles file not found and JSON parsing errors
        - Returns formatted output of hexagram data

Dependencies:
    - json: JSON file parsing
    - os: File system operations
    - pathlib: Path handling
    - pprint: Pretty printing of data structures

Author: JW
Last Updated: 2024
=============================================================================
"""
import json
import os
from pathlib import Path
from pprint import pprint

# Initialize the list to store all hexagram data
hexagram_data_list = []

def read_hexagram_info(file_path):
    try:
        # Read and parse the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Get the requested values (using get() to handle missing keys safely)
        hexagram_id = data.get('id')
        hexagram_code = data.get('hexagram_code')
        binary_sequence = data.get('binary_sequence')
        hexagram_name = data.get('name')

        # Create list with items in specified order
        hexagram_data = [hexagram_id, hexagram_code, binary_sequence, hexagram_name]

        # Add to the list of lists
        hexagram_data_list.append(hexagram_data)

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
    except json.JSONDecodeError:
        print(f"Error: File '{file_path}' is not valid JSON")
    except KeyError as e:
        print(f"Error: Missing expected key in JSON structure: {e}")

if __name__ == "__main__":
    # Get the parent directory
    parent_dir = Path(__file__).parent.parent
    regen_dir = parent_dir / "regen"

    # Process all JSON files in the regen directory
    for json_file in sorted(regen_dir.glob("*.json")):
        read_hexagram_info(json_file)

    # Sort hexagram_data_list by the first element (hexagram_id)
    hexagram_data_list.sort(key=lambda x: x[2])

    # Print hexagram codes
    for hexagram in hexagram_data_list:
        print(hexagram[1])

    # Pretty print the sorted array
    # pprint(hexagram_data_list)

