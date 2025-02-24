#!/bin/env python
"""
Unicode Hexagram Character Converter

This script processes JSON files containing I Ching hexagram data and updates their
hexagram codes with the corresponding Unicode characters. It uses a mapping of
hexagram IDs (1-64) to their respective Unicode characters (U+4DC0 to U+4DFF).

The script:
1. Reads all JSON files in the ../regen directory
2. For each file, extracts the 'id' field
3. Looks up the corresponding Unicode hexagram character
4. Updates the 'hexagram_code' field with the Unicode character
5. Saves the modified JSON file

Each hexagram entry contains:
- bin: Binary representation (e.g., "111111")
- hex: Unicode hexagram character (e.g., "䷀")
- unicode: Unicode code point (e.g., "\u4DC0")

Usage:
    python unicode2char.py

Requirements:
    - Python 3.x
    - JSON files must contain 'id' and 'hexagram_code' fields
"""

import os
import json

# Dictionary mapping hexagram codes to their properties
hexagrams = {
    1: {"bin": "111111", "hex": "䷀", "unicode": "\u4DC0"},
    2: {"bin": "000000", "hex": "䷁", "unicode": "\u4DC1"},
    3: {"bin": "010001", "hex": "䷂", "unicode": "\u4DC2"},
    4: {"bin": "100010", "hex": "䷃", "unicode": "\u4DC3"},
    5: {"bin": "010111", "hex": "䷄", "unicode": "\u4DC4"},
    6: {"bin": "111010", "hex": "䷅", "unicode": "\u4DC5"},
    7: {"bin": "000010", "hex": "䷆", "unicode": "\u4DC6"},
    8: {"bin": "010000", "hex": "䷇", "unicode": "\u4DC7"},
    9: {"bin": "011111", "hex": "䷈", "unicode": "\u4DC8"},
    10: {"bin": "111110", "hex": "䷉", "unicode": "\u4DC9"},
    11: {"bin": "000111", "hex": "䷊", "unicode": "\u4DCA"},
    12: {"bin": "111000", "hex": "䷋", "unicode": "\u4DCB"},
    13: {"bin": "111101", "hex": "䷌", "unicode": "\u4DCC"},
    14: {"bin": "101111", "hex": "䷍", "unicode": "\u4DCD"},
    15: {"bin": "000100", "hex": "䷎", "unicode": "\u4DCE"},
    16: {"bin": "001000", "hex": "䷏", "unicode": "\u4DCF"},
    17: {"bin": "011001", "hex": "䷐", "unicode": "\u4DD0"},
    18: {"bin": "100110", "hex": "䷑", "unicode": "\u4DD1"},
    19: {"bin": "000011", "hex": "䷒", "unicode": "\u4DD2"},
    20: {"bin": "110000", "hex": "䷓", "unicode": "\u4DD3"},
    21: {"bin": "101001", "hex": "䷔", "unicode": "\u4DD4"},
    22: {"bin": "100101", "hex": "䷕", "unicode": "\u4DD5"},
    23: {"bin": "100000", "hex": "䷖", "unicode": "\u4DD6"},
    24: {"bin": "000001", "hex": "䷗", "unicode": "\u4DD7"},
    25: {"bin": "111001", "hex": "䷘", "unicode": "\u4DD8"},
    26: {"bin": "100111", "hex": "䷙", "unicode": "\u4DD9"},
    27: {"bin": "100001", "hex": "䷚", "unicode": "\u4DDA"},
    28: {"bin": "011110", "hex": "䷛", "unicode": "\u4DDB"},
    29: {"bin": "010010", "hex": "䷜", "unicode": "\u4DDC"},
    30: {"bin": "101101", "hex": "䷝", "unicode": "\u4DDD"},
    31: {"bin": "011100", "hex": "䷞", "unicode": "\u4DDE"},
    32: {"bin": "001110", "hex": "䷟", "unicode": "\u4DDF"},
    33: {"bin": "111100", "hex": "䷠", "unicode": "\u4DE0"},
    34: {"bin": "001111", "hex": "䷡", "unicode": "\u4DE1"},
    35: {"bin": "101000", "hex": "䷢", "unicode": "\u4DE2"},
    36: {"bin": "000101", "hex": "䷣", "unicode": "\u4DE3"},
    37: {"bin": "110101", "hex": "䷤", "unicode": "\u4DE4"},
    38: {"bin": "101011", "hex": "䷥", "unicode": "\u4DE5"},
    39: {"bin": "010100", "hex": "䷦", "unicode": "\u4DE6"},
    40: {"bin": "001010", "hex": "䷧", "unicode": "\u4DE7"},
    41: {"bin": "100011", "hex": "䷨", "unicode": "\u4DE8"},
    42: {"bin": "110001", "hex": "䷩", "unicode": "\u4DE9"},
    43: {"bin": "011111", "hex": "䷪", "unicode": "\u4DEA"},
    44: {"bin": "111110", "hex": "䷫", "unicode": "\u4DEB"},
    45: {"bin": "011000", "hex": "䷬", "unicode": "\u4DEC"},
    46: {"bin": "000110", "hex": "䷭", "unicode": "\u4DED"},
    47: {"bin": "011010", "hex": "䷮", "unicode": "\u4DEE"},
    48: {"bin": "010110", "hex": "䷯", "unicode": "\u4DEF"},
    49: {"bin": "011101", "hex": "䷰", "unicode": "\u4DF0"},
    50: {"bin": "101110", "hex": "䷱", "unicode": "\u4DF1"},
    51: {"bin": "001001", "hex": "䷲", "unicode": "\u4DF2"},
    52: {"bin": "100100", "hex": "䷳", "unicode": "\u4DF3"},
    53: {"bin": "110100", "hex": "䷴", "unicode": "\u4DF4"},
    54: {"bin": "001011", "hex": "䷵", "unicode": "\u4DF5"},
    55: {"bin": "001101", "hex": "䷶", "unicode": "\u4DF6"},
    56: {"bin": "101100", "hex": "䷷", "unicode": "\u4DF7"},
    57: {"bin": "011011", "hex": "䷸", "unicode": "\u4DF8"},
    58: {"bin": "110110", "hex": "䷹", "unicode": "\u4DF9"},
    59: {"bin": "010011", "hex": "䷺", "unicode": "\u4DFA"},
    60: {"bin": "110010", "hex": "䷻", "unicode": "\u4DFB"},
    61: {"bin": "110011", "hex": "䷼", "unicode": "\u4DFC"},
    62: {"bin": "001100", "hex": "䷽", "unicode": "\u4DFD"},
    63: {"bin": "101010", "hex": "䷾", "unicode": "\u4DFE"},
    64: {"bin": "010101", "hex": "䷿", "unicode": "\u4DFF"}
}

def process_json_files():
    # Get directory path
    regen_dir = "../regen"

    # Get all JSON files in the directory
    json_files = [f for f in os.listdir(regen_dir) if f.endswith('.json')]

    for json_file in sorted(json_files):
        file_path = os.path.join(regen_dir, json_file)

        try:
            # Read the JSON file
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Get the id value and check if hexagram_code exists
            if 'id' in data and 'hexagram_code' in data:
                hex_id = int(data['id'])

                if hex_id in hexagrams:
                    # Replace hexagram_code with the corresponding hex character
                    data['hexagram_code'] = hexagrams[hex_id]['hex']

                    # Write the updated data back to the file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)

                    print(f"Updated {json_file}: id {hex_id} → {hexagrams[hex_id]['hex']}")
                else:
                    print(f"Warning: No hexagram found for id {hex_id} in {json_file}")
            else:
                print(f"Warning: Missing 'id' or 'hexagram_code' in {json_file}")

        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {json_file}")
        except Exception as e:
            print(f"Error processing {json_file}: {str(e)}")

if __name__ == "__main__":
    process_json_files()
