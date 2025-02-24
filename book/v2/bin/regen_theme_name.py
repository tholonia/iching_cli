#!/usr/bin/env python
"""
=============================================================================
regen_theme_name.py - Story Theme Author Extractor
=============================================================================

Description:
  Extracts author names from story themes in I Ching JSON files using NLP
  Named Entity Recognition and pattern matching. Handles various formats like:
  - "Style of {Author}"
  - "In the style of {Author}"
  - "Inspired by {Author}"
  - "{Author}'s Style"
  - "{Author} Style"
  etc.

Usage:
  ./regen_theme_name.py [--save]

Arguments:
  --save : Update the files with extracted author names instead of printing

Dependencies:
  - spacy (with en_core_web_sm model)
  - colorama

Setup:
  pip install spacy colorama
  python -m spacy download en_core_web_sm

Output:
  Without --save: Prints filename and transformations in color
    - Filename in green
    - Original theme in yellow
    - Extracted name in cyan
  With --save: Updates files with extracted names

Author: Assistant
Last Updated: 2024-03
=============================================================================
"""

import json
import sys
import os
from pathlib import Path
import argparse
from colorama import Fore, Style, init
import spacy

# Initialize spacy model
nlp = spacy.load("en_core_web_sm")

def extract_author(theme_text):
    """Extract author name using NLP Named Entity Recognition"""
    doc = nlp(theme_text)

    # Look for PERSON entities
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            # Clean up common suffixes
            name = ent.text
            name = name.replace("'s Style", "")
            name = name.replace("'s", "")
            name = name.strip()
            return name

    # If no PERSON entity found, try cleaning up common patterns
    text = theme_text
    patterns_to_remove = [
        "In the style of ",
        "Style of ",
        "Inspired by ",
        "Following ",
        "After ",
        "Channeling ",
        "the prose of ",
        "Written In the Style of ",
        "Written In the ",
        "By the Clockwork of ",
        "Inspired by the Style of ",
        "the ",
        "'s Style",
        "'s",
        " Style"
    ]

    for pattern in patterns_to_remove:
        text = text.replace(pattern, "")
        text = text.replace(pattern.lower(), "")  # Try lowercase version too
        text = text.replace(pattern.title(), "")  # Try title case version too

    return text.strip()

def process_files(save_changes=False):
    """Process all JSON files in ../regen directory"""
    regen_path = Path('../regen')

    # Get all JSON files and sort them
    json_files = sorted(list(regen_path.glob('*.json')))

    for json_file in json_files:
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)

            if 'stories' in data and 'entries' in data['stories']:
                modified = False
                for entry in data['stories']['entries']:
                    if 'theme' in entry:
                        original_theme = entry['theme']
                        author_name = extract_author(original_theme)

                        if save_changes:
                            entry['theme'] = author_name
                            modified = True
                        else:
                            print(f"{Fore.GREEN}{json_file.name}:{Style.RESET_ALL} "
                                  f"{Fore.YELLOW}{original_theme}{Style.RESET_ALL} -> "
                                  f"{Fore.CYAN}{author_name}{Style.RESET_ALL}")

                # Save changes if requested and modifications were made
                if save_changes and modified:
                    with open(json_file, 'w') as f:
                        json.dump(data, f, indent=2)
                        print(f"Updated {json_file.name}")

        except Exception as e:
            print(f"Error processing {json_file}: {e}")

def main():
    init()  # Initialize colorama
    parser = argparse.ArgumentParser(description='Extract author names from story themes')
    parser.add_argument('--save', action='store_true', help='Save changes to files')
    args = parser.parse_args()

    process_files(args.save)

if __name__ == "__main__":
    main()