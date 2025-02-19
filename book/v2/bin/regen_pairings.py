#!/usr/bin/env python3

"""
=============================================================================
regen_pairings.py - I Ching Pair-Path Analysis Generator
=============================================================================

Description:
    This script analyzes pairs of I Ching hexagrams that are inversions of
    each other, representing ascending and descending aspects of a pair-path.
    It processes hexagram data and uses AI to generate pair-path analysis.

Usage:
    ./regen_pairings.py <hex1> <hex2> <pair_number>
    Example: ./regen_pairings.py 1 2 1

Process:
    1. Loads data for both hexagrams from JSON files
    2. Analyzes their relationship as a pair-path
    3. Generates analysis using AI:
       - Title for the pair-path
       - Description of relationship
       - Image prompt for visualization
    4. Updates both hexagram JSON files with pair-path data
    5. Determines path stability (dynamic/stable)
    6. Assigns pair-path number (1-32)

Arguments:
    hex1: First hexagram number (1-64)
    hex2: Second hexagram number (1-64)
    pair_number: Pair-path number (1-32)
    --save: Save changes back to JSON files

Output:
    - Updates to hexagram JSON files with pair-path analysis
    - Console output of generated analysis
    - Status messages for process steps

Pair-Path Features:
    - Identifies ascending/descending relationships
    - Generates meaningful titles
    - Creates descriptive analysis
    - Provides image generation prompts
    - Determines path stability
    - Assigns canonical path numbers

Dependencies:
    - Python 3.x
    - openai
    - json
    - colorama

Author: Assistant
Last Updated: 2024-03-21
=============================================================================
"""


pathnum = [
    [11,12,1],
    [54,53,2],
    [55,59,3],
    [32,42,4],
    [60,56,5],
    [63,64,6],
    [48,21,7],
    [17,18,8],
    [47,22,9],
    [31,41,10],
    [49,4,11],
    [34,20,12],
    [28,27,13],
    [43,23,14],
    [8,14,15],
    [3,50,16],
    [29,30,17],
    [16,9,18],
    [51,57,19],
    [39,38,20],
    [40,37,21],
    [15,10,22],
    [36,6,23],
    [7,13,24],
    [5,35,25],
    [24,44,26],
    [2,1,27],
    [45,26,28],
    [62,61,29],
    [46,25,30],
    [19,33,31],
    [58,52,32],
]


import os
import json
import sys
import argparse
from openai import OpenAI
from colorama import Fore, Style





hexagram_values = {
    1: [63, "111111", 6],
    2: [0, "000000", 0],
    3: [17, "010001", 2],
    4: [34, "100010", 2],
    5: [23, "010111", 4],
    6: [58, "111010", 4],
    7: [10, "001010", 2],
    8: [16, "010000", 1],
    9: [55, "110111", 5],
    10: [59, "111011", 5],
    11: [7, "000111", 3],
    12: [56, "111000", 3],
    13: [61, "111101", 5],
    14: [47, "101111", 5],
    15: [4, "000100", 1],
    16: [8, "001000", 1],
    17: [25, "011001", 3],
    18: [38, "100110", 3],
    19: [3, "000011", 2],
    20: [48, "110000", 2],
    21: [41, "101001", 3],
    22: [37, "100101", 3],
    23: [32, "100000", 1],
    24: [1, "000001", 1],
    25: [57, "111001", 4],
    26: [39, "100111", 4],
    27: [33, "100001", 2],
    28: [30, "011110", 4],
    29: [18, "010010", 2],
    30: [45, "101101", 4],
    31: [28, "011100", 3],
    32: [14, "001110", 3],
    33: [60, "111100", 4],
    34: [15, "001111", 4],
    35: [40, "101000", 2],
    36: [5, "000101", 2],
    37: [53, "110101", 4],
    38: [43, "101011", 4],
    39: [20, "010100", 2],
    40: [10, "001010", 2],
    41: [35, "100011", 3],
    42: [49, "110001", 3],
    43: [31, "011111", 5],
    44: [62, "111110", 5],
    45: [24, "011000", 2],
    46: [6, "000110", 2],
    47: [26, "011010", 3],
    48: [22, "010110", 3],
    49: [29, "011101", 4],
    50: [46, "101110", 4],
    51: [9, "001001", 2],
    52: [36, "100100", 2],
    53: [52, "110100", 3],
    54: [11, "001011", 3],
    55: [13, "001101", 3],
    56: [44, "101100", 3],
    57: [54, "110110", 4],
    58: [27, "011011", 4],
    59: [50, "110010", 3],
    60: [19, "010011", 3],
    61: [51, "110011", 4],
    62: [12, "001100", 2],
    63: [21, "010101", 3],
    64: [42, "101010", 3]
}




Group_0 = [2]
Group_1 = [8, 15, 16, 23, 24, 32]
Group_2 = [3, 4, 7, 19, 20, 27, 29, 35, 36, 39, 40, 45, 46, 51, 62]
Group_3 = [11, 12, 17, 18, 21, 22, 31, 32, 41, 42, 47, 48, 53, 54, 55, 56, 59, 60, 63, 64]
Group_4 = [5, 6, 25, 26, 28, 30, 33, 34, 37, 38, 49, 50, 57, 58, 61]
Group_5 = [9, 10, 13, 14, 43, 44]
Group_6 = [1]


def load_hexagram_json(hex_num):
    """Load hexagram data from JSON file in ../regen directory."""
    hex_str = f"{int(hex_num):02d}"  # Zero-pad to 2 digits
    filepath = f"../regen/{hex_str}.json"

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Make a copy of the data to avoid modifying the original
            datacopy = data.copy()

            return data, datacopy, filepath  # Return the filepath too

    except FileNotFoundError:
        print(f"Error: File {filepath} not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {filepath}")
        sys.exit(1)

def get_pair_analysis(hex1_data, hex2_data, hex1_num, hex2_num):
    """Generate pair-path analysis using OpenAI API."""

    # Remove specified elements if they exist
    hex1_data.pop('stories', None)
    hex1_data.pop('history', None)
    hex2_data.pop('stories', None)
    hex2_data.pop('history', None)

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is required")
        sys.exit(1)

    prompt = f"""
Hexagram {hex1_num} and Hexagram {hex2_num} are exact inverses of each other. As a pair, they represent the two aspects (one ascending, one descending) of one of the 32 possible pair-paths. Analyze the provided JSON data for both hexagrams to determine the nature of this pair-path, its meaning, and assign a suitable **SHORT** title to it. Focus only on the **pair-path** as a whole, not on individual hexagrams.

Describe an image suitable as an AI promt for image generation.

- When referencing a hexagram by number, **always include both its name and number**.
- If a hexagram has **equal numbers of yin and yang lines** (i.e., **3 yin and 3 yang**), set `"kstate": "sephiroth"`, otherwise set `"kstate": "path"`.
- Return the response **only in JSON format** with no additional text, explanations, or formatting.

### **Expected JSON Format:**
{{
    "pairpath": {{
        "title": "{{Pair-Path title 1 or 2 words}}",
        "ascending_hex_num": {hex1_num},
        "ascending_hex_name": "{{Ascending hexagram name}}",
        "descending_hex_num": {hex2_num},
        "descending_hex_name": "{{Descending hexagram name}}",
        "description": "{{Pair-Path description}}",
        "kstate": "{{Pair-Path kstate}}",
        "image_prompt": "{{Image prompt for AI image generation}}"
    }}
}}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            temperature=0.5,
            messages=[
                {"role": "system", "content": "You are an expert in I Ching analysis and interpretation, and the Tholonic Model, and you are a brilliant writer of philosophy."},
                {"role": "user", "content": prompt}
            ]
        )
        return extract_valid_json(response.choices[0].message.content.strip())
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        sys.exit(1)

def extract_valid_json(text):
    """
    Attempt to extract and parse valid JSON from a string or dict.
    Returns parsed JSON object or exits with error.
    """
    # If already a dict, return it
    if isinstance(text, dict):
        return text

    # If it's a string, try to parse it
    if isinstance(text, str):
        # First try the original string
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Try removing markdown code blocks
        if "```json" in text or "```" in text:
            try:
                # Remove ```json and ``` markers
                cleaned = text.replace("```json", "").replace("```", "").strip()
                return json.loads(cleaned)
            except json.JSONDecodeError:
                pass

        # Try to find JSON-like content between curly braces
        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                potential_json = text[start:end]
                return json.loads(potential_json)
        except json.JSONDecodeError:
            pass

    # If all attempts fail, print error and exit
    print(Fore.RED + "Error: Could not extract valid JSON from response" + Style.RESET_ALL)
    print(Fore.YELLOW + "Raw response:" + Style.RESET_ALL)
    print(text)
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Generate I Ching pair-path analysis')
    parser.add_argument('hex1', type=int, help='First hexagram number (1-64)')
    parser.add_argument('hex2', type=int, help='Second hexagram number (1-64)')
    parser.add_argument('pair_number', type=int, help='Pair-path number (1-32)')
    parser.add_argument('--save', action='store_true', help='Save modified JSON back to original files')
    args = parser.parse_args()

    # Validate input ranges
    if not (1 <= args.hex1 <= 64 and 1 <= args.hex2 <= 64):
        print("Error: Hexagram numbers must be between 1 and 64")
        sys.exit(1)
    if not (1 <= args.pair_number <= 32):
        print("Error: Pair number must be between 1 and 32")
        sys.exit(1)

    # Load hexagram data
    hex1_data, hex1_data_copy, hex1_path = load_hexagram_json(args.hex1)  # Get filepath
    hex2_data, hex2_data_copy, hex2_path = load_hexagram_json(args.hex2)  # Get filepath

    # Get analysis
    analysis = get_pair_analysis(hex1_data_copy, hex2_data_copy, args.hex1, args.hex2)

    try:
        # Parse and validate JSON
        analysis_data = extract_valid_json(analysis)

        # Add the analysis to both hexagrams' data
        pair_path_key = f"pairpath"
        hex1_data[pair_path_key] = analysis_data['pairpath']
        hex2_data[pair_path_key] = analysis_data['pairpath']


        # manualy update the path type

        if args.hex1 in Group_3:
            hex1_data['pairpath']['kstate'] = 'stable'
            hex2_data['pairpath']['kstate'] = 'stable'
        else:
            hex1_data['pairpath']['kstate'] = 'dynamic'
            hex2_data['pairpath']['kstate'] = 'dynamic'

        # Find matching path number from pathnum list
        for path in pathnum:
            if args.hex1 in [path[0], path[1]]:
                hex1_data['pairpath']['path_num'] = path[2]
                hex2_data['pairpath']['path_num'] = path[2]
                break

        if args.save:
            # Save back to original files
            with open(hex1_path, 'w', encoding='utf-8') as f:
                json.dump(hex1_data, f, indent=2)
            with open(hex2_path, 'w', encoding='utf-8') as f:
                json.dump(hex2_data, f, indent=2)
            print(f"Updated files saved: {hex1_path}, {hex2_path}")
        else:
            # Print the analysis
            print(json.dumps(analysis_data, indent=2))

    except KeyError as e:
        print(Fore.RED + f"Error: Missing expected key in analysis: {e}" + Style.RESET_ALL)
        print(Fore.YELLOW + "Raw response:" + Style.RESET_ALL)
        print(json.dumps(analysis_data, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()
