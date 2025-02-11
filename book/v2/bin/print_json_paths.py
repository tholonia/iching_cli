#!/usr/bin/env python

"""
This script processes a JSON file and prints all paths to each value in the JSON structure.
The user must specify the full path to the JSON file.

Usage:
    ./print_json_paths.py <file_path>

Where <file_path> is the full path to the JSON file.
"""

import json
import argparse
from pathlib import Path

def print_json_paths(data, prefix=''):
    """Recursively print all paths in a JSON object."""
    if isinstance(data, dict):
        for key, value in data.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            print(new_prefix)
            print_json_paths(value, new_prefix)
    elif isinstance(data, list):
        for i, value in enumerate(data):
            new_prefix = f"{prefix}.{i}"
            print(new_prefix)
            print_json_paths(value, new_prefix)

def process_json_file(file_path):
    """Process a JSON file given its full path."""
    filepath = Path(file_path)
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            print(f"\nPaths for {filepath.name}:")
            print_json_paths(data)
    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {filepath}")

def main():
    parser = argparse.ArgumentParser(description='Process a JSON file.')
    parser.add_argument('file_path', type=str, help='Full path to the JSON file')
    args = parser.parse_args()

    process_json_file(args.file_path)

if __name__ == "__main__":
    main() 