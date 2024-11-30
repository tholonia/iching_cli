#!/bin/env python3
import json
import pandas as pd
import sys

# Get file number from command line argument
if len(sys.argv) != 2:
   print("Usage: script.py file_number")
   print("Example: script.py 01")
   sys.exit(1)

file_num = sys.argv[1]

# Construct input and output filenames
input_file = f'/home/jw/store/src/iching_cli/defs/alls/out/{file_num}_c.json'
output_file = f'/home/jw/store/src/iching_cli/defs/alls/out/update1/{file_num}_c.json'

# Load the JSON file
with open(input_file, 'r') as f:
   json_data = json.load(f)

# Load the CSV file
df = pd.read_csv('order_updated.csv')

# Get the row where hex matches king_wen_sequence
hex_val = json_data['hx']['core']['king_wen_sequence']
matching_row = df[df['hex'] == hex_val].iloc[0]

# Add order8child and order8parent to core
json_data['hx']['core'].update({
   'order8child': matching_row['order8child'],
   'order8parent': matching_row['order8parent']
})

# Save updated JSON back to file
with open(output_file, 'w') as f:
   json.dump(json_data, f, indent=4)