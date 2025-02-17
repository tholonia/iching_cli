#!/bin/env python

"""
=============================================================================
regen_trigrams_phrase_general.py - I Ching Trigram Phrase Generator
=============================================================================

Description:
  This script generates a general trigram phrase for an I Ching hexagram by
  combining multiple philosophical perspectives (Jungian, Platonic, Taoist,
  Tholonic, and Thermodynamic) into a single comprehensive description.
  It processes a single JSON file containing hexagram data and can either
  display or save the generated phrase.

Usage:
  ./regen_trigrams_phrase_general.py <filename> [--save]
  Example: ./regen_trigrams_phrase_general.py 01.json --save

Arguments:
  filename: JSON file to process (e.g., 01.json)
  --save: Optional flag to save updates to the JSON file

Process:
  1. Loads specified hexagram JSON file
  2. Extracts existing trigram phrases from different perspectives
  3. Uses OpenAI API to generate a combined general phrase
  4. Either displays the result or saves it back to the file
  5. Updates JSON with new 'general' field under 'trigram_phrase'

Dependencies:
  - Python 3.x
  - Required packages: openai, colorama
  - OpenAI API key in environment

File Structure:
  Input JSON format:
    {
      "trigram_phrase": {
        "Jungian": "...",
        "Platonic": "...",
        "Taoist": "...",
        "Tholonic": "...",
        "Thermodynamics": "..."
      }
    }

Environment:
  OPENAI_API_KEY: OpenAI API authentication key

Error Handling:
  - Validates file existence
  - Ensures valid JSON formatting
  - Handles API errors gracefully
  - Reports errors in color-coded output

Author: JW
Last Updated: 2024
=============================================================================
"""

import os
import json
import sys
import argparse
from openai import OpenAI
from colorama import Fore, Style, init

# Initialize colorama
init()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY environment variable is required")
    sys.exit(1)

def get_json_response(hexagram_data):
    """Generate a general trigram phrase from multiple perspectives."""

    # Extract all trigram phrases and hexagram info
    trigram_phrases = hexagram_data.get('trigram_phrase', {})
    trigrams = hexagram_data.get('trigrams', {})

    hex_name = hexagram_data.get('name', '')
    hex_id = hexagram_data.get('id', '')

    # Create the prompt with context
    prompt = f"""
    For hexagram {hex_id} ({hex_name}), combine all of the following philosophical perspectives into one sentence that explains how the trigrams of this hexagram can generally be described:

    {json.dumps(trigram_phrases, indent=4)}

    First, provide a single sentence that synthesizes these perspectives into a general phrase.

    Then, IN LESS THAT 100 WORDS, explain how the upper lower trigram of "{trigrams['below']['Meaning']}" representing {trigrams['below']['Quality']} and the upper trigram of "{trigrams['above']['Meaning']}" representing {trigrams['above']['Quality']} can produce the general phrase.


    IMPORTANT INSTRUCTIONS:
    - Use simple and easy to understand terms when creating this new phrase
    - Do NOT include any other text or commentary.  Just the sentence.
    - Do not refer to hexagrams by number.  Only refer to them by their name.

    The output MUST be in the following JSON format:

    {{
        "general_phrase": "<general phrase>",
        "explanation": "<explanation>"
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            temperature=0.4,
            messages=[
                {"role": "system", "content": "You are an expert in combining philosophical perspectives and analyzing trigram relationships. Provide both synthesis and detailed justification."},
                {"role": "user", "content": prompt}
            ]
        )

        # Get just the response text
        response_text = response.choices[0].message.content.strip()
        # Remove JSON code block markers if they exist
        response_text = response_text.replace('```json', '').replace('```', '').strip()

        # Parse the JSON response
        try:
            json_response = json.loads(response_text)
            print(f"{Fore.GREEN}{json.dumps(json_response, indent=4)}{Style.RESET_ALL}")
            return json_response
        except json.JSONDecodeError:
            print(f"{Fore.RED}Error: Invalid JSON response{Style.RESET_ALL}")
            return None

    except Exception as e:
        print(f"{Fore.RED}Error calling OpenAI API: {e}{Style.RESET_ALL}")
        return None

def process_json(file_path, save=False):
    """Process JSON file and update with general trigram phrase."""
    print(f"{Fore.CYAN}Processing file: {file_path}{Style.RESET_ALL}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"{Fore.RED}Error loading JSON file: {e}{Style.RESET_ALL}")
        return

    # Generate the general trigram phrase
    response = get_json_response(data)

    if response:
        try:
            # Parse the response to get the general phrase and explanation
            # response_lines = response['general_phrase'])
            general_phrase = response['general_phrase']
            explanation = response['explanation']

            # Update the JSON structure
            if 'trigram_phrase' not in data:
                data['trigram_phrase'] = {}
            data['trigram_phrase']['general'] = general_phrase
            data['trigram_phrase']['explanation'] = explanation

            if save:
                # Save updated JSON back to file
                print(f"{Fore.YELLOW}{general_phrase}{Style.RESET_ALL}")
                print(f"\n{Fore.CYAN}{explanation}{Style.RESET_ALL}")
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)
                    print(f"{Fore.GREEN}Successfully updated {file_path}: {file_path}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}Error saving file {file_path}: {e}{Style.RESET_ALL}")
            else:
                # Print the result to screen
                print(f"{Fore.YELLOW}{general_phrase}{Style.RESET_ALL}")
                print(f"\n{Fore.CYAN}{explanation}{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}Error processing response: {e}{Style.RESET_ALL}")
            return

def main():
    parser = argparse.ArgumentParser(description='Generate general trigram phrase for a specific I Ching hexagram')
    parser.add_argument('filename', help='JSON file to process (e.g., 01.json)')
    parser.add_argument('--save', action='store_true', help='Save updates to JSON file')
    args = parser.parse_args()

    # Process the specified JSON file
    if os.path.exists(args.filename):
        process_json(args.filename, args.save)
    else:
        print(f"{Fore.RED}Error: File {args.filename} not found{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
