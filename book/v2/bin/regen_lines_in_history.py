#!/bin/env python

"""
=============================================================================
regen_lines_in_history.py - I Ching Line History Generator
=============================================================================

Description:
  This script generates the six stages of change for a specific hexagram's
  history section using the OpenAI API. It processes a JSON file containing
  hexagram data and updates it with generated line-by-line interpretations.

Usage:
  ./regen_lines_in_history.py <source_dir> <hexagram_number>

Arguments:
  source_dir: Directory containing hexagram JSON files
  hexagram_number: Number of hexagram to process (1-64)

Process:
  1. Validates input arguments and file existence
  2. Loads hexagram JSON data
  3. Extracts history section
  4. Uses OpenAI API to generate line interpretations
  5. Updates JSON with new line data:
     - name: Concept name for the line
     - meaning: Line interpretation
     - changing: Meaning when line changes

Dependencies:
  - Python 3.x
  - Required packages: openai, colorama
  - OpenAI API key in environment

File Structure:
  - Input/Output: <source_dir>/<hexagram_number>.json

Environment:
  OPENAI_API_KEY: OpenAI API authentication key

Author: JW
Last Updated: 2024
=============================================================================
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
    print("Usage: regen_lines_in_history.py <source_dir> <hexagram_number>")
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

# Extract the history section
if "history" in json_data:
    history = json_data["history"]
else:
    print("Error: 'history' section not found in the JSON data.")
    sys.exit(1)

# Prepare the prompt for the OpenAI API
iching_primer_path = "../includes/iching_primer.md"
tholonic_primer_path = "../includes/tholonic_primer.md"

with open(iching_primer_path, "r", encoding="utf-8") as f:
    iching_primer_content = f.read()

with open(tholonic_primer_path, "r", encoding="utf-8") as f:
    tholonic_primer_content = f.read()

prompt = f"""
Using the context from the I Ching and Tholonic primers, generate the six stages of change for the following history. Each stage should include a name that encapsulates the overall concept of this transformation, a description, and the significance when the line's yin or yang value changes to its opposite.

Title: {history['title']}
Subtitle: {history['subtitle']}
Summary: {history['summary']}

Return only valid JSON in the format:
{{
"1": ["name", "meaning", "changing"],
"2": ["name", "meaning", "changing"],
"3": ["name", "meaning", "changing"],
"4": ["name", "meaning", "changing"],
"5": ["name", "meaning", "changing"],
"6": ["name", "meaning", "changing"]
}}

IMPORTANT: Output JSON only, no other text or commentary.
IMPORTANT: Do not use terms like "Yin replaces Yang" or "Yang replaces Yin". This is INACCURATE. Use the terms "changing line" or "moving line" instead.

Do not refer top yin or yang lines changing, just refer to changing or moving lines.

I Ching Primer:
{iching_primer_content}

Tholonic Primer:
{tholonic_primer_content}
"""

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY environment variable is required")
    sys.exit(1)

# Make API request using the new ChatCompletion method
try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in I Ching analysis. Respond only with valid JSON."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract and parse the response
    response_text = response.choices[0].message.content.strip()

    # Ensure the response is valid JSON
    try:
        stages_of_change = json.loads(response_text)
    except json.JSONDecodeError:
        print(Fore.RED + "Error: The API response is not valid JSON." + Style.RESET_ALL)
        print("Response received:")
        print(response_text)
        sys.exit(1)

    # Update the JSON data with the new stages of change
    for line_number, (name, meaning, changing) in stages_of_change.items():
        if "lines_in_history" not in history:
            history["lines_in_history"] = {}
        history["lines_in_history"][line_number] = {
            "name": name,
            "meaning": meaning,
            "changing": changing
        }

    # Save the updated JSON file back to the original input file
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
    print(Fore.GREEN + f"Successfully updated the JSON file: {json_path}" + Style.RESET_ALL)

except Exception as e:
    print(Fore.RED + f"Error calling OpenAI API: {e}" + Style.RESET_ALL)
