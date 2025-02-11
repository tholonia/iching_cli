#!/bin/env python

"""
This script creates a trigram phrase for a specific hexagram JSON file and updates the file with the new phrase.

Usage:
    ./regen_trigram_phrase.py <source_dir> <hexagram_number>

Required Arguments:
    source_dir: The directory containing the source JSON files
    hexagram_number: The number of the hexagram to process (1-64)

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
    print("Usage: regen_trigram_phrase.py <source_dir> <hexagram_number>")
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

# Load context files
iching_primer_path = os.path.join(source_dir, "../includes/iching_primer.md")
tholonic_primer_path = os.path.join(source_dir, "../includes/tholonic_primer.md")

try:
    with open(iching_primer_path, "r", encoding="utf-8") as f:
        iching_primer_content = f.read()
except FileNotFoundError:
    iching_primer_content = ""

try:
    with open(tholonic_primer_path, "r", encoding="utf-8") as f:
        tholonic_primer_content = f.read()
except FileNotFoundError:
    tholonic_primer_content = ""

# Check if 'trigram_phrase' exists, if not, create it
if "trigram_phrase" not in json_data:
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
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in I Ching analysis and the tholonic model.  You are also a brilliant and creative writer.  You are given a phrase that expresses the dynamics of the trigrams for a specific hexagram.  Your job is to reword the phrase in a way that is more poetic and insightful.  The phrase should be a single sentence that captures the essence of the hexagram.  The phrase should be written in the style of a shaman or mystic giving sage advice to a young acolyte.  Use lower case excedpt for the start of the sentence.  IMPORTANT: only reply with the phrase itself, no other words.  CREATE A GRAMATICALLY PROPER SENTENCE WITH PROPER CASING AND PUNCTUATION. Capitalize the first character of the first word and put a period at the end of the sentence."},
                {"role": "user", "content": reword_prompt}
            ]
        )

        # Extract and parse the reworded response
        reworded_phrase = reword_response.choices[0].message.content.strip()
        json_data["trigram_phrase"] = reworded_phrase

        # Save the updated JSON file back to the original input file
        # print(reworded_phrase)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)
        print(Fore.GREEN + f"Successfully updated the JSON file with trigram phrase: {json_path}" + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"Error calling OpenAI API for rewording: {e}" + Style.RESET_ALL)
