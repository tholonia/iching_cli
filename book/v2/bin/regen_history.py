#!/bin/env python
"""
=============================================================================
regen_history.py - I Ching Historical Context Generator
=============================================================================

Description:
  Generates historical context and interpretations for I Ching hexagrams using
  various AI APIs. Takes a hexagram JSON file as input and generates new
  historical perspectives and line interpretations.

Usage:
  ./regen_history.py -f <input_json_file> -p <provider> [-s]

Arguments:
  -f, --filename : Path to hexagram JSON file (e.g., ../regen/01.json)
  -p, --provider : AI provider to use (openai, grok, anthropic, google)
  -s, --save     : Save the modified data back to the input file

Environment Variables:
  OPENAI_API_KEY  : For OpenAI API access
  GROK_API_KEY    : For Grok API access
  ANTHROPIC_KEY   : For Anthropic API access
  GOOGLE_API_KEY  : For Google API access

Process:
  1. Reads hexagram data from JSON file
  2. Generates new historical context using specified AI provider
  3. Updates:
     - Title and subtitle
     - Historical source reference
     - Historical context and interpretation
     - Line-by-line historical meanings and changes

Output:
  - Prints formatted historical context
  - Outputs complete JSON if not saving
  - Updates input file if --save specified

Dependencies:
  - requests
  - jsonschema
  - colorama
  - funcs_lib.py

Author: Assistant
Last Updated: 2024-03
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
from funcs_lib import call_ai_api
import traceback

# Initialize colorama
init()

# Initialize OpenAI client
client = OpenAI()

def parse_args():
    parser = argparse.ArgumentParser(description='Generate new history for I Ching hexagrams.')
    parser.add_argument('-f', '--filename', required=True,
                      help='Path to JSON file containing history data')
    parser.add_argument('-p', '--provider', required=True,
                      help='API provider to use (e.g., openai, grok)')
    parser.add_argument('-s', '--save', action='store_true',
                      help='Save the modified data back to the input file')
    return parser.parse_args()

# def get_model_for_provider(provider):
    # """Return the appropriate model name for the given provider."""
    # provider_models = {
    #     'openai': 'gpt-4o',
    #     'grok': 'grok-beta',
    #     'anthropic': 'claude-3-opus-20240229',
    #     'google': 'gemini-pro'
    # }
    # return provider_models.get(provider, 'gpt-4')  # default to gpt-4 if provider not found

def ai_query(hexagram_number, args):
    """Make API request for new hisstory content."""
    if not os.getenv("OPENAI_API_KEY"):
        print(Fore.RED + "Error: OPENAI_API_KEY environment variable is required" + Style.RESET_ALL)
        print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
        sys.exit(1)

    try:
        system_message = "You are an expert in I Ching analysis and the Tholonic Model and are a brilliant historian. Respond only with valid JSON."
        prompt = slib.make_history_prompt(hexagram_number)

        # Make single API call based on provider
        try:
            response_text = call_ai_api(
                prompt=prompt,
                system_message=system_message,
                provider=args.provider  # Use provider from command line args
            )
        except Exception as e:
            print(Fore.RED + f"Error calling {args.provider} API: {str(e)}" + Style.RESET_ALL)
            print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
            raise

        if not response_text:
            raise ValueError("Empty response from API")

        # Ensure the response is valid JSON
        try:
            new_story = json.loads(response_text)
            if not new_story:  # Check if empty
                raise ValueError("Empty JSON response")
            return new_story
        except json.JSONDecodeError as e:
            print(Fore.RED + "Error: The API response is not valid JSON." + Style.RESET_ALL)
            print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
            print("Response received:")
            print(response_text)
            sys.exit(1)
    except Exception as e:
        print(Fore.RED + f"Error with AI API: {e}" + Style.RESET_ALL)
        print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
        sys.exit(1)

def make_new_story(history_data, hexagram_number, args):
    """Create a new story entry by replacing title, theme, and short_story with their key names."""
    new_story = ai_query(hexagram_number, args)
    # Replace the fields in the specified entry
    history_data['title'] = new_story['title']
    history_data['subtitle'] = new_story['subtitle']
    history_data['source'] = new_story['source']
    history_data['short_story'] = new_story['short_story']

    """Replace line values in lines_in_history with 'line'."""
    # Get the lines_in_history for the specified entry
    lines_in_history = history_data['lines_in_history']

    # For each line position (1-6)
    for line_num in ['1', '2', '3', '4', '5', '6']:
        # Replace name, meaning, and changing with 'line'
        lines_in_history[line_num]['name'] = new_story['lines_in_history'][line_num]['name']
        lines_in_history[line_num]['meaning'] = new_story['lines_in_history'][line_num]['meaning']
        lines_in_history[line_num]['changing'] = new_story['lines_in_history'][line_num]['changing']

    return history_data

def print_story(story,*args):
    """Print a single story entry in a formatted way."""
    print("\n" + "="*80)
    print(Fore.CYAN + f"Title:{Fore.YELLOW} {story['title']}" + Style.RESET_ALL)
    print(Fore.CYAN + f"Subtitle:{Fore.YELLOW} {story['subtitle']}" + Style.RESET_ALL)
    print(Fore.CYAN + f"Source:{Fore.YELLOW} {story['source']}" + Style.RESET_ALL)
    print(Fore.CYAN + f"short_story:{Fore.GREEN} {story['short_story']}" + Style.RESET_ALL)
    print("\nLines in Context:")
    for line_num, line_data in story['lines_in_history'].items():
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
        if "history" not in data:
            print("Error: No 'history' section found in input file")
            sys.exit(1)

        history_data = data["history"]

        # Validate against schema from the library
        jsonschema.validate(instance=history_data, schema=slib.history_schema)

        # # Validate entry_index
        # if args.index < 0 or args.index >= len(stories_data['entries']):
        #     print(f"Error: entry_index must be between 0 and {len(stories_data['entries']) - 1}")
        #     sys.exit(1)

        # Print title of the collection
        # print(f"\nStory Collection: {stories_data['title']}\n")

        # Update stories with new_story function
        history_data = make_new_story(history_data, hexagram_number, args)

        # Print only the specified entry
        # print(f"Story #{args.index}")
        # print_story(stories_data['entries'][args.index], args.index)

        # Update the stories section in the original data
        data["history"] = history_data

        # Save the modified data if --save flag is used
        if args.save:
            try:
                with open(args.filename, 'w') as f:
                    json.dump(data, f, indent=4)
                print(Fore.GREEN + f"\nSuccessfully saved changes to hisstory in {args.filename}" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"\nError saving file: {e}" + Style.RESET_ALL)
                sys.exit(1)
        else:
            print(Fore.RED + json.dumps(history_data, indent=4) + Style.RESET_ALL)

        # Return the modified data
        return history_data

    except FileNotFoundError:
        print(f"Error: File '{args.filename}' not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: '{args.filename}' is not a valid JSON file")
        sys.exit(1)
    except jsonschema.exceptions.ValidationError as e:
        print(f"Error: history data does not match schema: {e.message}")
        sys.exit(1)
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}" + Style.RESET_ALL)
        print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
        sys.exit(1)

if __name__ == "__main__":
    main()