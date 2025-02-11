#!/bin/env python

"""
This script uses the OpenAI API to generate a concise one- or two-word title that best expresses the concept of a hexagram.

Usage:
    ./regen_titles.py <source_dir> <hexagram_number>

Required Arguments:
    source_dir: The directory containing the source JSON files
    hexagram_number: The number of the hexagram to process (1-64)

Example:
    ./regen_titles.py ../path/to/source 01

Environment Variables:
    OPENAI_API_KEY: Your OpenAI API key (required)
"""

import os
import json
import sys
from openai import OpenAI
from colorama import Fore, Style, init

# Initialize colorama
init()

# Ensure exactly two command line arguments are provided
if len(sys.argv) != 3:
    print("Usage: regen_titles.py <source_dir> <hexagram_number>")
    sys.exit(1)

# Extract and validate the source directory and hexagram number
source_dir = sys.argv[1]
hex_num = sys.argv[2]

if not hex_num.isdigit() or not (1 <= int(hex_num) <= 64):
    print("Error: Hexagram number must be an integer between 1 and 64.")
    sys.exit(1)

hex_str = f"{int(hex_num):02}"
hex_filename = f"{hex_str}.json"
json_path = os.path.join(source_dir, hex_filename)

# Ensure the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file {json_path} not found.")
    sys.exit(1)

# Load the JSON data
with open(json_path, "r", encoding="utf-8") as f:
    json_data = json.load(f)

# Extract the current name
if "name" in json_data:
    old_name = json_data["name"]
else:
    print("Error: 'name' not found in the JSON data.")
    sys.exit(1)

# Prepare the prompt for the OpenAI API
prompt = f"""
Understand the significance of the following I Ching hexagram and provide a one- or two-word title that best expresses its concept.

Hexagram Number: {hex_num}
Current Name: {old_name}

Return only the new title.
"""

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY environment variable is required")
    sys.exit(1)

# Make API request to generate a new title
try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in I Ching analysis. Provide a concise title."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the new title from the response
    new_name = response.choices[0].message.content.strip()

    # Print the hex number, old name, and new name
    print(f"Hexagram Number: {hex_num}")
    print(f"Old Name: {old_name}")
    print(f"New Name: {new_name}")

    # Update the JSON data with the new name
    json_data["name"] = new_name

    # Save the updated JSON file back to the original input file
    # with open(json_path, "w", encoding="utf-8") as f:
    #     json.dump(json_data, f, indent=4, ensure_ascii=False)
    # print(Fore.GREEN + f"Successfully updated the JSON file: {json_path}" + Style.RESET_ALL)

except Exception as e:
    print(Fore.RED + f"Error calling OpenAI API: {e}" + Style.RESET_ALL)
