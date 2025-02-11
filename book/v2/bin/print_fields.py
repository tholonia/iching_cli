#! /usr/bin/env python3
import os
import json

# Define the folder containing the JSON files
folder_path = "../_v2"

# Define the specific keys to extract from "lines_in_transition"
keys = ["6", "5", "4", "3", "2", "1"]

# Iterate over each file in the folder
for filename in sorted(os.listdir(folder_path)):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)
        
        # Open and parse the JSON file
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        
        # Extract and print the values from lines_in_transition
        try:
            print(f"\n--- {filename} ---")
            for key in keys:
                if key in data["hx"]["core"]["lines_in_transition"]:
                    # Get the value and print only the first four words
                    value = data["hx"]["core"]["lines_in_transition"][key]
                    first_four_words = ' '.join(value.split()[:4])
                    print(first_four_words)
        except KeyError:
            print(f"Warning: {filename} does not contain expected structure.")
