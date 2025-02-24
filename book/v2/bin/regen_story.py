#!/bin/env python
"""
=============================================================================
regen_story.py - I Ching Story Regenerator
=============================================================================

Description:
  This script regenerates stories for I Ching hexagrams using various AI providers.
  It takes a JSON file containing story data and an entry index as input, then
  updates the specified story with new AI-generated content while preserving the
  existing structure.

Usage:
  ./regen_story.py -f <input_json_file> -i <entry_index> -p <provider> [-s]

Arguments:
  -f, --filename : Path to JSON file containing stories data
  -i, --index    : Integer specifying which story entry to update (0-based index)
  -p, --provider : AI provider to use (e.g., openai, grok, anthropic)
  -s, --save     : Save the modified data back to the input file (optional)

Example:
  ./regen_story.py -f ../regen/01.json -i 0 -p openai -s
  ./regen_story.py --filename ../regen/01.json --index 0 --provider grok

Process:
  1. Reads and validates input JSON file against schema
  2. Makes API request to specified AI provider for new story content
  3. Updates specified story entry with new content:
     - title
     - theme
     - short_story
     - lines_in_context (name, meaning, changing for each line)
  4. Optionally saves changes back to input file
  5. Prints complete JSON output in red

Environment Variables:
  OPENAI_API_KEY: Required for OpenAI API access
  Other provider-specific keys as needed

Dependencies:
  - OpenAI Python package
  - jsonschema
  - colorama
  - regen_story_lib.py (local library)
  - funcs_lib.py (local library)

Output:
  - Prints formatted story to stdout
  - Returns updated stories data structure
  - Optionally saves modified JSON back to input file

Author: Assistant
Last Updated: 2024
=============================================================================
"""
import json
import sys
import jsonschema
from openai import OpenAI
from colorama import Fore, Style, init
import regen_story_lib as slib
from pprint import pprint
import os
import argparse
from funcs_lib import call_ai_api, get_model_for_provider  # Add this import
import traceback
from dotenv import load_dotenv

load_dotenv()

# Initialize colorama
init()

# Initialize OpenAI client
client = OpenAI()

def parse_args():
    parser = argparse.ArgumentParser(description='Generate new stories for I Ching hexagrams.')
    parser.add_argument('-f', '--filename', required=True,
                      help='Path to JSON file containing stories data')
    parser.add_argument('-i', '--index', type=int, required=True,
                      help='Story entry index to update (0-based)')
    parser.add_argument('-s', '--save', action='store_true',
                      help='Save the modified data back to the input file')
    parser.add_argument('-p', '--provider', required=True,
                      help='API provider to use (e.g., openai, grok)')
    return parser.parse_args()

def ai_query(hexagram_number, args):
    """Make API request for new story content."""
    if not os.getenv("OPENAI_API_KEY"):
        print(Fore.RED + "Error (r01): OPENAI_API_KEY environment variable is required" + Style.RESET_ALL)
        print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
        sys.exit(1)

    try:
        system_message = "You are an expert in I Ching analysis and the Tholonic Model and are a brilliant story writer. Respond only with valid JSON."
        prompt = slib.make_stories_prompt(hexagram_number, args.index)

        try:
            response_text = call_ai_api(
                prompt=prompt,
                system_message=system_message,
                provider=args.provider
            )
        except Exception as e:
            print(Fore.RED + f"Error (r02): Error calling {args.provider} API: {str(e)}" + Style.RESET_ALL)
            print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
            raise

        if not response_text:
            raise ValueError("Error (r03): Empty response from API")

        try:
            new_story = json.loads(response_text)
            if not new_story:  # Check if empty
                raise ValueError("Error (r04): Empty JSON response")
            return new_story
        except json.JSONDecodeError as e:
            print(Fore.RED + "Error (r05): The API response is not valid JSON." + Style.RESET_ALL)
            print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
            print("Response received:")
            print(response_text)
            sys.exit(1)
    except Exception as e:
        print(Fore.RED + f"Error (r06): Error with AI API: {str(e)}" + Style.RESET_ALL)
        print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
        sys.exit(1)

def make_new_story(stories_data, entry_index, hexagram_number, args):
    """Create a new story entry by replacing title, theme, and short_story with their key names."""
    try:
        new_story = ai_query(hexagram_number, args)
        # Replace the fields in the specified entry
        stories_data['entries'][entry_index]['title'] = new_story['entries'][0]['title'] + " (" + slib.story_type[args.index][0] + ")"
        stories_data['entries'][entry_index]['theme'] = new_story['entries'][0]['theme']
        stories_data['entries'][entry_index]['short_story'] = new_story['entries'][0]['short_story']

        # Get the lines_in_context for the specified entry
        lines_in_context = stories_data['entries'][entry_index]['lines_in_context']

        # For each line position (1-6)
        for line_num in ['1', '2', '3', '4', '5', '6']:
            try:
                lines_in_context[line_num]['name'] = new_story['entries'][0]['lines_in_context'][line_num]['name']
                lines_in_context[line_num]['meaning'] = new_story['entries'][0]['lines_in_context'][line_num]['meaning']
                lines_in_context[line_num]['changing'] = new_story['entries'][0]['lines_in_context'][line_num]['changing']
            except KeyError as e:
                print(Fore.RED + f"Error (r07): Missing key in line {line_num}: {str(e)}" + Style.RESET_ALL)
                raise
            except Exception as e:
                print(Fore.RED + f"Error (r08): Error processing line {line_num}: {str(e)}" + Style.RESET_ALL)
                raise

        return stories_data
    except Exception as e:
        print(Fore.RED + f"Error (r09): Error creating new story: {str(e)}" + Style.RESET_ALL)
        print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
        raise

def print_story(story,*args):
    """Print a single story entry in a formatted way."""
    print("\n" + "="*80)
    print(Fore.CYAN + f"Title:{Fore.YELLOW} {story['title']} ({slib.story_type[args.index][0]})" + Style.RESET_ALL)
    print(Fore.CYAN + f"Theme:{Fore.YELLOW} {story['theme']}" + Style.RESET_ALL)
    print(Fore.CYAN + f"short_story:{Fore.GREEN} {story['short_story']}" + Style.RESET_ALL)
    print("\nLines in Context:")
    for line_num, line_data in story['lines_in_context'].items():
        print(Fore.CYAN + f"\nLine {line_num}:{Fore.GREEN}" + Style.RESET_ALL)
        print(Fore.CYAN + f"  Name:{Fore.GREEN} {line_data['name']}" + Style.RESET_ALL)
        print(Fore.CYAN + f"  Meaning:{Fore.GREEN} {line_data['meaning']}" + Style.RESET_ALL)
        print(Fore.CYAN + f"  Changing:{Fore.GREEN} {line_data['changing']}" + Style.RESET_ALL)
    print("="*80 + "\n")

def main():
    args = parse_args()

    try:
        # Extract hexagram number from filename
        base_name = os.path.basename(args.filename)
        file_number = base_name.split('.')[0]
        hexagram_number = int(file_number)
        if hexagram_number < 1 or hexagram_number > 64:
            print(Fore.RED + "Error (r10): Hexagram number must be between 1 and 64" + Style.RESET_ALL)
            sys.exit(1)
        hexagram_number = f"{hexagram_number:02d}"
    except (ValueError, IndexError) as e:
        print(Fore.RED + f"Error (r11): Could not extract valid hexagram number from filename: {str(e)}" + Style.RESET_ALL)
        sys.exit(1)

    try:
        # Read input JSON file
        with open(args.filename, 'r') as f:
            data = json.load(f)

        # Extract stories section
        if "stories" not in data:
            print(Fore.RED + "Error (r12): No 'stories' section found in input file" + Style.RESET_ALL)
            sys.exit(1)

        stories_data = data["stories"]

        # Validate against schema from the library
        try:
            jsonschema.validate(instance=stories_data, schema=slib.stories_schema)
        except jsonschema.exceptions.ValidationError as e:
            print(Fore.RED + f"Error (r13): Stories data does not match schema: {str(e)}" + Style.RESET_ALL)
            sys.exit(1)

        # Validate entry_index
        if args.index < 0 or args.index >= len(stories_data['entries']):
            print(Fore.RED + f"Error (r14): entry_index must be between 0 and {len(stories_data['entries']) - 1}" + Style.RESET_ALL)
            sys.exit(1)

        # Update stories with new_story function
        stories_data = make_new_story(stories_data, args.index, hexagram_number, args)

        # Update the stories section in the original data
        data["stories"] = stories_data

        # Save the modified data if --save flag is used
        if args.save:

            # Add metadata about the regeneration
            from datetime import datetime
            current_time = datetime.now().strftime("%a %b %d %I:%M:%S %p %z %Y")
            data['api'] = args.provider
            data['model'] = get_model_for_provider(args.provider)
            data['date'] = current_time

            try:
                with open(args.filename, 'w') as f:
                    json.dump(data, f, indent=4)
                print(Fore.GREEN + f"\nSuccessfully saved changes to story[{args.index}] ({slib.story_type[args.index][0]}) in {args.filename}" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Error (r15): Error saving file: {str(e)}" + Style.RESET_ALL)
                sys.exit(1)
        else:
            print(Fore.RED + json.dumps(stories_data["entries"][args.index], indent=4) + Style.RESET_ALL)

        return stories_data

    except FileNotFoundError:
        print(Fore.RED + f"Error (r16): File '{args.filename}' not found" + Style.RESET_ALL)
        sys.exit(1)
    except json.JSONDecodeError:
        print(Fore.RED + f"Error (r17): '{args.filename}' is not a valid JSON file" + Style.RESET_ALL)
        sys.exit(1)
    except Exception as e:
        print(Fore.RED + f"Error (r18): Unexpected error: {str(e)}" + Style.RESET_ALL)
        print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
        sys.exit(1)

if __name__ == "__main__":
    main()