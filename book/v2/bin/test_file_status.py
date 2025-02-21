#!/usr/bin/env python
"""
=============================================================================
compare_json_dirs.py - JSON Directory Comparison Tool
=============================================================================

Description:
  Compares JSON files between two directories, showing differences only for
  files that don't match. Looks for files with matching names and compares
  their contents.

Usage:
  ./compare_json_dirs.py <comparison_dir> [--short]

Arguments:
  comparison_dir : Directory to compare against ../regen/
  --short       : Only print filenames of differing files

Output:
  Prints filenames and their differences when found (or just names with --short).
  Silent for matching files.

Author: Assistant
Last Updated: 2024-03
=============================================================================
"""

import json
import sys
import os
from pathlib import Path
import difflib
import argparse

def load_json(filepath):
    """Load and return JSON file contents"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def compare_files(base_dir, comp_dir, short=False):
    """Compare JSON files between directories"""
    base_path = Path('../regen')
    comp_path = Path(comp_dir)

    # Get all JSON files in base directory and sort them
    base_files = sorted(list(base_path.glob('*.json')), key=lambda x: x.name)

    for base_file in base_files:
        comp_file = comp_path / base_file.name

        # Skip if comparison file doesn't exist
        if not comp_file.exists():
            continue

        # Load both files
        base_data = load_json(base_file)
        comp_data = load_json(comp_file)

        if base_data is None or comp_data is None:
            continue

        # Convert to formatted strings for comparison
        base_str = json.dumps(base_data, sort_keys=True, indent=2)
        comp_str = json.dumps(comp_data, sort_keys=True, indent=2)

        # Compare and print differences if any
        if base_str != comp_str:
            if short:
                print(base_file.name)
            else:
                print(f"\nDifferences in {base_file.name}:")
                diff = difflib.unified_diff(
                    comp_str.splitlines(),
                    base_str.splitlines(),
                    fromfile=str(comp_file),
                    tofile=str(base_file),
                    lineterm=''
                )
                print('\n'.join(list(diff)))

def parse_args():
    parser = argparse.ArgumentParser(description='Compare JSON files between directories')
    parser.add_argument('comparison_dir', help='Directory to compare against ../regen/')
    parser.add_argument('--short', action='store_true', help='Only print filenames of differing files')
    return parser.parse_args()

def main():
    args = parse_args()
    compare_files('../regen', args.comparison_dir, args.short)

if __name__ == "__main__":
    main()
