#!/bin/env python

#The purpose of this script is to combine specific elements from two JSON files into a new JSON file. The script is designed to facilitate the aggregation of data from two sources, likely used in a larger system where JSON is a common format for data interchange.

import json
import sys

# Check if a parameter was provided
if len(sys.argv) < 2:
    print("Please provide a string parameter to construct filenames")
    sys.exit(1)

# Get the string parameter
param = sys.argv[1]

# Construct filenames using the parameter
rem_filename = f'rem/{param}-rem.json'
core_filename = f'core/{param}-core.json'
output_filename = f'out/{param}_c.json'

# Load the JSON data from the files
with open(rem_filename, 'r') as rem_file:
    rem_data = json.load(rem_file)

with open(core_filename, 'r') as core_file:
    core_data = json.load(core_file)


# Extract the children (fields) of the first node from each file
stories_node = rem_data[0]
history_node = rem_data[1]
core_node = core_data[0]

# Combine the children into a single structure under a new "hexagram" node
hx = {
    "core":core_node,
    "stories": stories_node,
     "history":history_node
}


# Save the combined data into a new JSON file
with open(output_filename, 'w') as combined_file:
    json.dump({"hx": hx}, combined_file, indent=4)

print(f"Combined JSON saved as '{output_filename}'")
