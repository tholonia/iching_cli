#!/bin/env python
"""
=============================================================================
regen_story.py - I Ching Story Generator
=============================================================================

Description:
  This script generates new stories for I Ching hexagrams using OpenAI's GPT API.
  It takes a JSON file containing story data and an entry index as input, then
  updates the specified story with new AI-generated content.

Usage:
  ./regen_story.py --filename <input_json_file> --index <entry_index>
  ./regen_story.py -f <input_json_file> -i <entry_index>

Arguments:
  -f, --filename : Path to JSON file containing stories data
  -i, --index    : Integer specifying which story entry to update (0-based index)
  -s, --save     : Save the modified data back to the input file

Example:
  ./regen_story.py --filename ../regen/01.json --index 0
  ./regen_story.py -f ../regen/01.json -i 0

Environment Variables:
  OPENAI_API_KEY: Required OpenAI API key for making requests

Process:
  1. Reads and validates input JSON file against schema
  2. Makes API request to OpenAI for new story content
  3. Updates specified story entry with new content:
     - title
     - theme
     - short_story
     - lines_in_context (name, meaning, changing for each line)
  4. Prints updated story and returns modified data structure

Dependencies:
  - OpenAI Python package
  - jsonschema
  - colorama
  - regen_story_lib.py (local library)

Output:
  - Prints formatted story to stdout
  - Returns updated stories data structure
  - Prints complete JSON output in red

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
    return parser.parse_args()

def ai_query(hexagram_number, args):
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is required")
        sys.exit(1)

    # Make API request using the new ChatCompletion method
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert in I Ching analysis and the Tholonic Model and are a brilliant story writer. Respond only with valid JSON."},
                {"role": "user", "content": slib.make_prompt(hexagram_number, args.index)}
            ]
        )

        # Extract and parse the response
        response_text = response.choices[0].message.content.strip()

        # Remove JSON code block markers if they exist
        response_text = response_text.replace('```json', '').replace('```', '').strip()

        # Ensure the response is valid JSON
        try:
            new_story = json.loads(response_text)
            if not new_story:  # Check if empty
                raise ValueError("Empty JSON response")
            return new_story
        except json.JSONDecodeError:
            print(Fore.RED + "Error: The API response is not valid JSON." + Style.RESET_ALL)
            print("Response received:")
            print(response_text)
            sys.exit(1)
    except Exception as e:
        print(Fore.RED + f"Error calling OpenAI API: {e}" + Style.RESET_ALL)
        sys.exit(1)

def make_new_story(stories_data, entry_index, hexagram_number, args):
    """Create a new story entry by replacing title, theme, and short_story with their key names."""
    new_story = ai_query(hexagram_number, args)
    # Replace the fields in the specified entry
    stories_data['entries'][entry_index]['title'] = new_story['entries'][0]['title'] + " (" + slib.story_type[args.index] + ")"
    stories_data['entries'][entry_index]['theme'] = new_story['entries'][0]['theme']
    stories_data['entries'][entry_index]['short_story'] = new_story['entries'][0]['short_story']

    """Replace line values in lines_in_context with 'line'."""
    # Get the lines_in_context for the specified entry
    lines_in_context = stories_data['entries'][entry_index]['lines_in_context']

    # For each line position (1-6)
    for line_num in ['1', '2', '3', '4', '5', '6']:
        # Replace name, meaning, and changing with 'line'
        lines_in_context[line_num]['name'] = new_story['entries'][0]['lines_in_context'][line_num]['name']
        lines_in_context[line_num]['meaning'] = new_story['entries'][0]['lines_in_context'][line_num]['meaning']
        lines_in_context[line_num]['changing'] = new_story['entries'][0]['lines_in_context'][line_num]['changing']

    return stories_data

def print_story(story,*args):
    """Print a single story entry in a formatted way."""
    print("\n" + "="*80)
    print(Fore.CYAN + f"Title:{Fore.YELLOW} {story['title']} ({slib.story_type[args.index]})" + Style.RESET_ALL)
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

    # Extract hexagram number from filename
    try:
        base_name = os.path.basename(args.filename)
        file_number = base_name.split('.')[0]
        hexagram_number = int(file_number)
        if hexagram_number < 1 or hexagram_number > 64:
            print("Error: Hexagram number must be between 1 and 64")
            sys.exit(1)
        # Convert to zero-padded 2-digit string
        hexagram_number = f"{hexagram_number:02d}"
    except (ValueError, IndexError) as e:
        print(f"Error: Could not extract valid hexagram number from filename: {e}")
        sys.exit(1)

    try:
        # Read input JSON file
        with open(args.filename, 'r') as f:
            data = json.load(f)

        # Extract stories section
        if "stories" not in data:
            print("Error: No 'stories' section found in input file")
            sys.exit(1)

        stories_data = data["stories"]

        # Validate against schema from the library
        jsonschema.validate(instance=stories_data, schema=slib.stories_schema)

        # Validate entry_index
        if args.index < 0 or args.index >= len(stories_data['entries']):
            print(f"Error: entry_index must be between 0 and {len(stories_data['entries']) - 1}")
            sys.exit(1)

        # Print title of the collection
        # print(f"\nStory Collection: {stories_data['title']}\n")

        # Update stories with new_story function
        stories_data = make_new_story(stories_data, args.index, hexagram_number, args)

        # Print only the specified entry
        # print(f"Story #{args.index}")
        # print_story(stories_data['entries'][args.index], args.index)

        # Update the stories section in the original data
        data["stories"] = stories_data

        # Save the modified data if --save flag is used
        if args.save:
            try:
                with open(args.filename, 'w') as f:
                    json.dump(data, f, indent=4)
                print(Fore.GREEN + f"\nSuccessfully saved changes to story[{args.index}] in {args.filename}" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"\nError saving file: {e}" + Style.RESET_ALL)
                sys.exit(1)
        else:
            print(Fore.RED + json.dumps(stories_data, indent=4) + Style.RESET_ALL)

        # Return the modified data
        return stories_data

    except FileNotFoundError:
        print(f"Error: File '{args.filename}' not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: '{args.filename}' is not a valid JSON file")
        sys.exit(1)
    except jsonschema.exceptions.ValidationError as e:
        print(f"Error: Stories data does not match schema: {e.message}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()