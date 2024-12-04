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

# Construct input filename (now used for both input and output)
input_file = f'/home/jw/store/src/iching_cli/defs/final/{file_num}.json'

# Load the JSON file
with open(input_file, 'r') as f:
   json_data = json.load(f)

# Load the CSV file
df = pd.read_csv('order_updated.csv')

# Get the row where hex matches king_wen_sequence
hex_val = json_data['hx']['core']['king_wen_sequence']
bin_val = json_data['hx']['core']['binary_sequence']

matching_row = df[df['hex'] == hex_val].iloc[0]

yp = {
   'pure yin': [0],
   'first yang': [1,2,4,8,16,32],
   'emerging yang': [3, 5, 6, 9, 10, 12, 17, 18, 20, 24, 33, 34, 36, 40, 48],
   'balanced': [7, 11, 13, 14, 19, 21, 22, 25, 26, 28, 35, 37, 38, 41, 42, 44, 49, 50, 52, 56],
   'dominant yang':[15, 23, 27, 29, 30, 39, 43, 45, 46, 51, 53, 54, 57, 58, 60],
   'last yin': [31, 47, 55, 59, 61, 62],
   'pure yang': [63]
}

# Find which list contains bin_val and assign the key to ybal
yinyang_balance = None
for key, values in yp.items():
    if bin_val in values:
        yinyang_balance = key
        break

energy_cycle = None
if bin_val < 32:
    energy_cycle = "ascending"
else:
    energy_cycle = "descending"

# Add order8child, order8parent and ybal to core
json_data['hx']['core'].update({
    'order8child': matching_row['order8child'],
    'order8parent': matching_row['order8parent'],
    'yinyang_balance': yinyang_balance,
    'energy_cycle': energy_cycle,
    'image_description': "image description goes here"
})

# Save updated JSON back to the same input file
with open(input_file, 'w') as f:
   json.dump(json_data, f, indent=4)