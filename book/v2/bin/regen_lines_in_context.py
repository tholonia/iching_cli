#!/bin/env python

"""
Generate six stages of change for a specific story in I Ching Hexagrams using OpenAI API.

This script loads a JSON file from a specified source directory based on the hexagram number, extracts a specific story by index, and uses the OpenAI API to generate the six stages of change. It updates the JSON file with the new data, including a name, meaning, and changing description for each line.

Usage:
    ./regen_lines_in_context.py <source_dir> <hexagram_number> <story_index>

Required Arguments:
    source_dir: The directory containing the source JSON files
    hexagram_number: The number of the hexagram to process (1-64)
    story_index: The index of the story to process (0-based index)

Example:
    ./regen_lines_in_context.py ../regen 01 0

Process:
    1. Validates input arguments and file paths
    2. Loads hexagram data from JSON file
    3. Extracts specified story by index
    4. Generates six stages of change using OpenAI API
    5. Updates JSON with new line data:
       - name: Concept title for the stage
       - meaning: Description of the stage
       - changing: Interpretation when line changes

Dependencies:
    - OpenAI Python package (v1.0.0 or later)
    - colorama: Terminal output formatting
    - Required files:
      - ../includes/iching_primer.md
      - ../includes/tholonic_primer.md

Environment Variables:
    OPENAI_API_KEY: Your OpenAI API key (required)

File Structure:
    Input:
        - <source_dir>/<hexagram_number>.json
        - ../includes/iching_primer.md
        - ../includes/tholonic_primer.md
    Output:
        - Updated JSON file with new lines_in_context data

Author: JW
Last Updated: 2024
"""

import os
import json
import sys
from openai import OpenAI
from colorama import Fore, Style, init

# Initialize colorama
init()

# Ensure exactly three command line arguments are provided
if len(sys.argv) != 4:
    print("Usage: regen_lines_in_context.py <source_dir> <hexagram_number> <story_index>")
    sys.exit(1)

# Extract and validate the source directory, hexagram number, and story index
source_dir = sys.argv[1]
hex_num = sys.argv[2]
story_index = sys.argv[3]

if not hex_num.isdigit() or not (1 <= int(hex_num) <= 64):
    print("Error: Hexagram number must be an integer between 1 and 64.")
    sys.exit(1)

if not story_index.isdigit():
    print("Error: Story index must be an integer.")
    sys.exit(1)

story_index = int(story_index)

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

# Extract the specified story
if "stories" in json_data and "entries" in json_data["stories"]:
    stories = json_data["stories"]["entries"]
    if 0 <= story_index < len(stories):
        story = stories[story_index]
    else:
        print(f"Error: Story index {story_index} is out of range.")
        sys.exit(1)
else:
    print("Error: 'stories' section not found in the JSON data.")
    sys.exit(1)

# Prepare the prompt for the OpenAI API
iching_primer_path = "../includes/iching_primer.md"
tholonic_primer_path = "../includes/tholonic_primer.md"

with open(iching_primer_path, "r", encoding="utf-8") as f:
    iching_primer_content = f.read()

with open(tholonic_primer_path, "r", encoding="utf-8") as f:
    tholonic_primer_content = f.read()

prompt = f"""
Using the context from the I Ching and Tholonic primers, generate the six stages of change for the following story. Each stage should include a name that encapsulates the overall concept of this transformation, a description, and the significance when the line's yin or yang value changes to its opposite.

Title: {story['title']}
Theme: {story['theme']}
Summary: {story['summary']}

Return only valid JSON in the format:
{{
"1": ["name", "meaning", "changing"],
"2": ["name", "meaning", "changing"],
"3": ["name", "meaning", "changing"],
"4": ["name", "meaning", "changing"],
"5": ["name", "meaning", "changing"],
"6": ["name", "meaning", "changing"]
}}

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
        if "lines_in_context" not in story:
            story["lines_in_context"] = {}
        story["lines_in_context"][line_number] = {
            "name": name,
            "meaning": meaning,
            "changing": changing
        }

    # Save the updated JSON file back to the original input file
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
    print(Fore.GREEN + f"Successfully updated stories.entries[{story_index}] in the JSON file: {json_path}" + Style.RESET_ALL)

except Exception as e:
    print(Fore.RED + f"Error calling OpenAI API on stories.entries[{story_index}] in {hex_filename}: {e}" + Style.RESET_ALL)
    print(f"{Fore.YELLOW}RERUN: ./regen_lines_in_context.py {source_dir} {hex_num} {story_index}" + Style.RESET_ALL)
