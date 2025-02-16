#!/bin/env python

"""
=============================================================================
regen_lines_in_trans.py - I Ching Line Transition Generator
=============================================================================

Description:
  This script generates line transition interpretations for I Ching hexagrams
  using the OpenAI API. It processes JSON files containing hexagram data and
  updates them with new line-by-line transition meanings. For each line,
  it generates a name, meaning, and changing line interpretation based on
  the hexagram's context.

Usage:
  ./regen_lines_in_trans.py <source_dir> <dest_dir>

Arguments:
  source_dir: Directory containing source hexagram JSON files
  dest_dir: Directory to write updated JSON files

Process:
  1. Validates input/output directories
  2. Loads hexagram JSON data
  3. For each hexagram (1-64):
     - Extracts hexagram context and data
     - Uses OpenAI API to generate line transitions
     - For each line (1-6):
       * Generates name capturing transition concept
       * Generates meaning interpretation
       * Generates changing line interpretation
  4. Updates JSON with new line data
  5. Saves to destination directory

Dependencies:
  - Python 3.x
  - Required packages: openai, colorama
  - OpenAI API key in environment

File Structure:
  - Input: <source_dir>/<hexagram>.json
  - Output: <dest_dir>/<hexagram>.json

Environment:
  OPENAI_API_KEY: OpenAI API authentication key

Error Handling:
  - Validates directory paths
  - Ensures valid JSON formatting
  - Handles API errors gracefully

Author: JW
Last Updated: 2024
=============================================================================
"""

import os
import json
import re
import sys
from openai import OpenAI
from colorama import Fore, Style, init

# Initialize colorama
init()

# Hexagrams to process

# Predefined list of all hexagrams
HEXAGRAMS = ['01', '02','03']


HEXAGRAMS = [ '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
    '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
    '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
    '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
    '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
    '51', '52', '53', '54', '55', '56', '57', '58', '59', '60',
    '61', '62', '63', '64']

# Require both directory arguments
if len(sys.argv) != 3:
    print("Error: Both input and output directories are required")
    print("Usage: ./regen_lines_in_trans.py <from_dir> <to_dir>")
    sys.exit(1)

# Get directory paths from command line arguments
input_dir = sys.argv[1]
output_dir = sys.argv[2]

# Validate input directory exists
if not os.path.exists(input_dir):
    print(f"Error: Input directory {input_dir} does not exist")
    sys.exit(1)

# Ensure output directory exists
try:
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory ensured: {output_dir}")
except Exception as e:
    print(f"Error creating output directory {output_dir}: {e}")
    sys.exit(1)

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY environment variable is required")
    sys.exit(1)

print(f"Processing files from {input_dir} to {output_dir}")

def generate_all_line_interpretations(hexagram_data):
    """Generate interpretations for all 6 lines using a single OpenAI API call."""
    print(f"{Fore.CYAN}Generating interpretations for all lines of {hexagram_data['name']}...{Style.RESET_ALL}")

    prompt = f"""
    For I Ching hexagram {hexagram_data['name']}, generate new interpretations for all 6 lines.
    For each line (1-6), provide:
    1. A name that captures the essence of the line
    2. A meaning that explains its significance
    3. A yin_to_yang transformation description if applicable

    Return only a JSON object with keys "1" through "6", each containing "name", "meaning", and "yin_to_yang" fields.
    """

    try:
        print(f"{Fore.YELLOW}Calling OpenAI API...{Style.RESET_ALL}")
        response = client.chat.completions.create(
            model="o3-mini-2025-01-31",
            messages=[
                {"role": "system", "content": "You are an expert in the I Ching. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ]
        )

        # Get the response content
        response_text = response.choices[0].message.content.strip()
        print(f"{Fore.GREEN}Received response from API{Style.RESET_ALL}")

        try:
            result = json.loads(response_text)
            return result
        except json.JSONDecodeError:
            print(f"{Fore.RED}Error parsing API response as JSON{Style.RESET_ALL}")
            return {}

    except Exception as e:
        print(f"{Fore.RED}Error calling OpenAI API: {e}{Style.RESET_ALL}")
        return {}

def process_json(file_path):
    """Process JSON file, generate new interpretations, and update the file."""
    print(f"\n{Fore.CYAN}Processing file: {file_path}{Style.RESET_ALL}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"{Fore.GREEN}Successfully loaded JSON file{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error loading JSON file: {e}{Style.RESET_ALL}")
        return

    # Get all line interpretations in one call
    interpretations = generate_all_line_interpretations(data)
    if not interpretations:
        print(f"{Fore.RED}Failed to generate interpretations{Style.RESET_ALL}")
        return

    # Update lines array
    if "lines" in data:
        for line in data["lines"]:
            position = str(line.get("position", 0))
            if position in interpretations:
                result = interpretations[position]
                line["name"] = result.get("name", "")
                line["meaning"] = result.get("meaning", "")
                line["yin_to_yang"] = result.get("yin_to_yang", "")

    # Update stories key_elements
    if "stories" in data and "entries" in data["stories"]:
        for story in data["stories"]["entries"]:
            if "key_elements" in story:
                for pos in ["1", "2", "3", "4", "5", "6"]:
                    if pos in interpretations:
                        result = interpretations[pos]
                        story["key_elements"][pos] = {
                            "name": result.get("name", ""),
                            "meaning": result.get("meaning", "")
                        }

    # Update history key_elements
    if "history" in data and "key_elements" in data["history"]:
        for pos in ["1", "2", "3", "4", "5", "6"]:
            if pos in interpretations:
                result = interpretations[pos]
                data["history"]["key_elements"][pos] = {
                    "name": result.get("name", ""),
                    "meaning": result.get("meaning", "")
                }

    # Save the updated JSON
    output_path = os.path.join(output_dir, os.path.basename(file_path))
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"{Fore.GREEN}Successfully saved: {output_path}")
        print(f"Updated {len(data.get('lines', []))} lines")
        print(f"Updated {len(data.get('stories', {}).get('entries', []))} stories")
        print(f"Updated history key elements{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error saving file: {e}{Style.RESET_ALL}")

# Process selected JSON files in input directory
print(f"{Fore.CYAN}Starting processing of JSON files...{Style.RESET_ALL}")
for filename in sorted(os.listdir(input_dir)):  # Ensure proper ordering
    match = re.match(r"(\d{2}).json", filename)  # Match 2-digit filenames like '06.json'
    if match and match.group(1) in HEXAGRAMS:
        file_number = match.group(1)  # Extract the number part (e.g., '06')
        input_path = os.path.join(input_dir, filename)

        try:
            process_json(input_path)
        except Exception as e:
            print(f"{Fore.RED}Error processing {filename}: {e}{Style.RESET_ALL}")

print(f"\n{Fore.GREEN}Processing complete. All requested files updated.{Style.RESET_ALL}")
