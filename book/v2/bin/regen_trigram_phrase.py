#!/bin/env python

"""
This script creates a trigram phrase for a specific hexagram JSON file and updates the file with the new phrase.

Usage:
    ./regen_trigram_phrase.py <source_dir> <hexagram_number> [--save]

Required Arguments:
    source_dir: The directory containing the source JSON files
    hexagram_number: The number of the hexagram to process (1-64)

Optional Arguments:
    --save: If provided, the script will save the updated JSON file.

Environment Variables:
    OPENAI_API_KEY: Your OpenAI API key (required)
"""

import os
import json
import sys
import argparse
from openai import OpenAI
from colorama import Fore, Style, init

# Initialize colorama
init()

#style = "Jungian"
# style = "Platonic"
# style = "Taoist"

# style = "Tholonic"
style = "Thermodynamics"


# Set up argument parser
parser = argparse.ArgumentParser(description="Generate and optionally save a trigram phrase for a hexagram JSON file.")
parser.add_argument("source_dir", help="The directory containing the source JSON files")
parser.add_argument("hexagram_number", type=int, choices=range(1, 65), help="The number of the hexagram to process (1-64)")
parser.add_argument("--save", action="store_true", help="Save the updated JSON file if this flag is set")
args = parser.parse_args()

# Extract and validate the source directory and hexagram number
source_dir = args.source_dir
hex_num = args.hexagram_number

hex_str = f"{hex_num:02}"
hex_filename = f"{hex_str}.json"
json_path = os.path.join(source_dir, hex_filename)

# Ensure the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file {json_path} not found.")
    sys.exit(1)

print(f"Processing file: {json_path}")

# Load the JSON data
with open(json_path, "r", encoding="utf-8") as f:
    json_data = json.load(f)

# Ensure json_data is a dictionary
if not isinstance(json_data, dict):
    print("Error: JSON data is not a dictionary.")
    sys.exit(1)

# Load context files
iching_primer_path = os.path.join(source_dir, "../includes/iching_primer.md")
tholonic_primer_path = os.path.join(source_dir, "../includes/tholonic_primer.md")

try:
    with open(iching_primer_path, "r", encoding="utf-8") as f:
        iching_primer_content = f.read()
except FileNotFoundError:
    iching_primer_content = ""
    print("Warning: iching_primer.md not found.")

try:
    with open(tholonic_primer_path, "r", encoding="utf-8") as f:
        tholonic_primer_content = f.read()
except FileNotFoundError:
    tholonic_primer_content = ""
    print("Warning: tholonic_primer.md not found.")

# Always create or update the 'trigram_phrase'
below_quality = json_data['trigrams']['below'].get('Quality', 'N/A')
above_quality = json_data['trigrams']['above'].get('Quality', 'N/A')
trigram_phrase = f"The result of {below_quality} expressed through {above_quality}."

# Prepare the prompt for rewording
reword_prompt = (
    f"{iching_primer_content}\n\n"
    f"{tholonic_primer_content}\n\n"
    f"JSON Data: {json.dumps(json_data, indent=2)}\n\n"
    f"Reword this phrase to best express the dynamics of the trigrams for this hexagram: {trigram_phrase}"
)

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY environment variable is required")
    sys.exit(1)

# Make API request to reword the phrase
try:
    reword_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"You are an expert in I Ching analysis and the tholonic model. Reword the given phrase into a conceptual sentence."},
            {"role": "user", "content": reword_prompt}
        ]
    )

    # Extract and parse the reworded response
    reworded_phrase = reword_response.choices[0].message.content.strip()
    # print(Fore.RED + f"Reworded phrase: {reworded_phrase}" + Style.RESET_ALL)

    # Submit the reworded phrase to OpenAI to rephrase it as a quote from {style}
    style_prompt = f"Rephrase this conceptual sentence to sound like a quote from {style}: {reworded_phrase}"
    style_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"You are an expert in philosophical writing. Rephrase the given sentence as if it were a {style} quote."},
            {"role": "user", "content": style_prompt}
        ]
    )

    # Extract and parse the {style}-styled response
    style_phrase = style_response.choices[0].message.content.strip()
    # print(Fore.GREEN + f"Styled phrase: {style_phrase}" + Style.RESET_ALL)
    # exit()
    # Ensure 'trigram_phrase' is a dictionary in json_data
    if "trigram_phrase" not in json_data or not isinstance(json_data["trigram_phrase"], dict):
        json_data["trigram_phrase"] = {}


    # Assign the styled phrase
    json_data["trigram_phrase"][style] = style_phrase.lstrip('"').rstrip('"')

    # Save the updated JSON file if --save is specified
    if args.save:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)
        print(Fore.RED + style_phrase + Style.RESET_ALL + f" --{style}")
        print(Fore.GREEN + f"Successfully updated the JSON file with trigram phrase: {json_path}" + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + style_phrase + Style.RESET_ALL)

except Exception as e:
    print(Fore.RED + f"Error calling OpenAI API for rewording: {e}" + Style.RESET_ALL)
