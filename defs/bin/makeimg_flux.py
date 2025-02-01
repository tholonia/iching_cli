#!/usr/bin/env python3

"""
I Ching Image Description Generator

This script analyzes existing I Ching hexagram images and generates new descriptions
that incorporate tholonic principles. It compares the new description with any
existing description before saving.

Process:
1. Loads hexagram data from JSON file
2. Loads and preserves any existing image description
3. Uses OpenAI GPT-4 to analyze the image with tholonic principles
4. Shows side-by-side comparison of old and new descriptions
5. Asks for confirmation before saving

Usage:
    python makeimg_desc.py <hexagram_number> <image_path>

Arguments:
    hexagram_number    Two-digit hexagram number (01-64)
    image_path        Path to the existing image to analyze

Required Files:
    - Hexagram JSON files in /home/jw/src/iching_cli/defs/final/
    - Tholonic primer at /home/jw/store/src/iching_cli/defs/tholonic_primer.md

Example:
    python makeimg_desc.py 35 images/hexagram_35.png

Output:
    Creates <image_path>_description.txt if approved by user
"""

import sys
import json
import base64
import os
from openai import OpenAI
from colorama import Fore, Style

MODEL = "gpt-4o"  # OpenAI model to use

def load_json_file(id_num):
    """Load the JSON file based on the ID number."""
    jsonfile = f"/home/jw/src/iching_cli/defs/final/{id_num}.json"
    print(Fore.YELLOW + "\nLoading JSON file: " + jsonfile + Style.RESET_ALL)
    try:
        with open(jsonfile, 'r') as file:
            prejson = json.load(file)
            # Store the old description before clearing
            old_desc = prejson['hx']['core']['image_description']
            #! Clear the image_description field
            prejson['hx']['core']['image_description'] = ""
            prejson['hx']['core']['image'] = ""
            return prejson, old_desc
    except FileNotFoundError:
        print(Fore.RED + f"Error: File {jsonfile} not found." + Style.RESET_ALL)
        sys.exit(1)

def load_tholonic_primer():
    """Load the tholonic primer content."""
    primer_path = "/home/jw/store/src/iching_cli/defs/tholonic_primer.md"
    try:
        with open(primer_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(Fore.RED + f"Warning: Could not load tholonic primer: {e}" + Style.RESET_ALL)
        return None

def get_image_analysis(image_path, json_data):
    """Analyze the image and generate a new description."""
    client = OpenAI()

    # Load tholonic primer
    tholonic_context = load_tholonic_primer()

    # Read the image file
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    try:
        system_message = {
            "role": "system",
            "content": f"""You are an expert in tholonic concepts and I Ching interpretation.
Here is the context about tholonic concepts to consider in your analysis:

{tholonic_context if tholonic_context else 'No additional context available'}

Important: Your analysis MUST incorporate tholonic principles and concepts, even while avoiding
the specific words 'tholon' or 'tholonic'. Focus on describing the universal patterns,
hierarchical relationships, and dynamic equilibrium that tholonic thinking reveals.
Reference concepts like triadic relationships, emergent order, and the interaction
between chaos and structure."""
        }

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                system_message,
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""
Analyze this hexagram data and image:
{json_data}

Explain why the subject, style, and medium were chosen to represent this hexagram.
Your analysis must incorporate tholonic principles while avoiding the words 'tholon' or 'tholonic'.
Focus on:
- The universal patterns and hierarchies present in the image
- The dynamic relationships between elements
- How the image embodies principles of emergence and order
- The triadic relationships visible in the composition
- The balance between structure and chaos

Answer in a concise narrative form and keep the answer as short as possible,
one paragraph, no more than 200 words. Do not use any artists names.
"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        analysis = response.choices[0].message.content
        # print(Fore.WHITE + "\nNew Image Analysis:" + Style.RESET_ALL)
        # print(Fore.YELLOW + analysis + Style.RESET_ALL)
        return analysis
    except Exception as e:
        print(Fore.RED + f"Error getting image analysis from OpenAI: {e}" + Style.RESET_ALL)
        return None

def main():
    if len(sys.argv) != 3:
        print("Usage: python makeimg_desc.py <hexagram_number> <image_path>")
        sys.exit(1)

    id_num = sys.argv[1]
    image_path = sys.argv[2]
    jsonfile = f"/home/jw/src/iching_cli/defs/final/{id_num}.json"

    # Validate ID format
    if not (len(id_num) == 2 and id_num.isdigit()):
        print(Fore.RED + "Error: Please provide a two-digit hexagram number" + Style.RESET_ALL)
        sys.exit(1)

    # Validate image path
    if not os.path.exists(image_path):
        print(Fore.RED + f"Error: Image file not found: {image_path}" + Style.RESET_ALL)
        sys.exit(1)

    # Load JSON data and get old description
    json_data, old_description = load_json_file(id_num)

    # Generate new description
    analysis = get_image_analysis(image_path, json_data)

    if analysis:
        print("\n" + "="*80)
        print(Fore.GREEN + "Old Description:" + Style.RESET_ALL)
        print(Fore.BLUE + (old_description if old_description else "No previous description") + Style.RESET_ALL)
        print("\n" + "-"*80 + "\n")
        print(Fore.GREEN + "New Description:" + Style.RESET_ALL)
        print(Fore.YELLOW + analysis + Style.RESET_ALL)
        print("="*80 + "\n")

        # Ask for confirmation
        while True:
            response = input(Fore.WHITE + "Do you want to save this description? (y/n): " + Style.RESET_ALL).lower()
            if response in ['y', 'n']:
                break
            print("Please answer 'y' or 'n'")

        if response == 'y':
            # Save analysis to text file
            output_file = f"{image_path}_description.txt"
            with open(output_file, 'w') as f:
                f.write(analysis)
            print(Fore.GREEN + f"\nDescription saved to: {output_file}" + Style.RESET_ALL)

            # Update the JSON file with new description
            json_data['hx']['core']['image_description'] = analysis
            with open(jsonfile, 'w') as f:
                json.dump(json_data, f, indent=2)
            print(Fore.GREEN + f"Updated description in: {jsonfile}" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "\nDescription not saved." + Style.RESET_ALL)

if __name__ == "__main__":
    main()