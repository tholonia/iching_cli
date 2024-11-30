#!/bin/env python

import json
import sys

if len(sys.argv) != 2:
    print("Usage: python validate_json.py <file_path>")
    sys.exit(1)

file_path = sys.argv[1]

try:
    with open(file_path, 'r') as file:
        json.load(file)
    print("JSON is valid.")
except json.JSONDecodeError as e:
    print(f"Invalid JSON: {e}")
except FileNotFoundError:
    print(f"File not found: {file_path}")
