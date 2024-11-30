#!/bin/env python

import json
import sys
from colorama import Fore, Style

def print_text_elements(data, parent_key=""):
    if isinstance(data, dict):
        for key, value in data.items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            print_text_elements(value, new_key)
    elif isinstance(data, list):
        for index, value in enumerate(data):
            new_key = f"{parent_key}[{index}]"
            print_text_elements(value, new_key)
    else:
        print(f"{Fore.GREEN}{parent_key}{Style.RESET_ALL}: {data}")

# Get filename parameter from command line
if len(sys.argv) < 2:
    print("Please provide a string parameter to construct the filename")
    sys.exit(1)

param = sys.argv[1]
filename = f'{param}_c.json'

# Load the JSON file
with open(filename, 'r') as json_file:
    data = json.load(json_file)

# Print all text elements
print_text_elements(data)
print("\n--------------------------------------------------------------------\n")