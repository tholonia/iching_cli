#!/bin/env python3
"""
=============================================================================
get_new_image_desc_OPENAI.py - I Ching Hexagram Image Description Generator
=============================================================================

Description:
  This script generates AI-powered descriptions of I Ching hexagram images using
  OpenAI's GPT-4 Vision API. For each hexagram image, it generates a narrative
  paragraph explaining why specific visual elements and styles were chosen to
  represent that hexagram.

Usage:
  python get_new_image_desc_OPENAI.py [-s] <hexagram_number>

Arguments:
  hexagram_number: Number of the hexagram (1-64)
  -s, --save: Save the output to a text file

Examples:
  python get_new_image_desc_OPENAI.py 20         # Display output only
  python get_new_image_desc_OPENAI.py -s 20      # Display and save output

Process:
  1. Reads hexagram image and context files
  2. Converts image to base64 for API submission
  3. Sends image and context to OpenAI's Vision API
  4. Generates a formatted description paragraph
  5. Optionally saves output to text file

Dependencies:
  - OpenAI Python package (v1.0.0 or later)
  - Valid OpenAI API key set in OPENAI_API_KEY environment variable
  - Access to GPT-4 Vision model in your OpenAI account
  - Required Python packages: openai, colorama

File Structure:
  - Input: /book/tholonic_primer.md
  - Input: /book/v2/<hexagram_number>.json
  - Input: /book/v2/<hexagram_number>.png
  - Output: /book/v2/<hexagram_number>_img.txt (when using --save)

Environment Variables:
  OPENAI_API_KEY: Your OpenAI API key (required)

Note:
  Vision API calls may have higher costs than standard GPT-4 calls.
  Ensure proper rate limiting and cost monitoring when using this script.

Author: JW
Last Updated: 2024
=============================================================================
"""
import os
import sys
import base64
from openai import OpenAI
import argparse
from colorama import Fore, Style


# Initialize OpenAI client with API key from environment variable
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_file_content(filepath):
    """Read file content as string or base64 for images."""
    if filepath.lower().endswith('.png'):
        try:
            with open(filepath, 'rb') as file:
                image_data = base64.b64encode(file.read()).decode('utf-8')
                return f"data:image/png;base64,{image_data}"
        except Exception as e:
            print(f"Failed to read image {filepath}: {e}")
            return None
    else:
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Failed to read {filepath}: {e}")
            return None

def get_contextual_response(context_files, hex_num_str):
    """Sends a request to the OpenAI API with the context files content."""

    # Add text content to context
    context = ""
    for filepath in context_files:
        if not filepath.lower().endswith('.png'):  # Skip image files
            content = get_file_content(filepath)
            if content:
                context += f"\nContent from {os.path.basename(filepath)}:\n{content}\n"

    # Create the prompt
    prompt = f"""
"Compose a concise narrative paragraph, approximately 100 words, explaining why the elements and styles of this image were selected to represent the hexagram '{hex_num_str}'. Begin the paragraph with the hexagram's name in quotation marks, for example:

'Contemplation' is vividly depicted...

Use the hexagram's name from the JSON file, not its traditional name."
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are providing a detailed response to a prompt about hexagrams."},
                {"role": "user", "content": f"Context:\n{context}\n\nPrompt:\n{prompt}"}
            ],
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Generate AI-powered descriptions of I Ching hexagram images')
    parser.add_argument('-s', '--save', action='store_true', help='Save output to file')
    parser.add_argument('hexagram', type=int, help='Hexagram number (1-64)')
    args = parser.parse_args()

    try:
        if args.hexagram < 1 or args.hexagram > 64:
            raise ValueError("Hexagram number must be between 1 and 64")
        hex_num_str = f"{args.hexagram:02d}"  # Zero-pad to 2 digits
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Files to use as context
    context_files = [
        "/home/jw/src/iching_cli/book/tholonic_primer.md",
#        "/home/jw/src/iching_cli/book/final/Thee_tholonic_iching.md",
        f"/home/jw/src/iching_cli/book/v2/{hex_num_str}.json",
        f"/home/jw/src/iching_cli/book/v2/{hex_num_str}.png",
    ]

    # Get response using file contents as context
    response = get_contextual_response(context_files, hex_num_str)
    if response:
        print("\nResponse:")
        print(Fore.GREEN + response + Style.RESET_ALL)

        # Save response to file only if --save flag is used
        if args.save:
            output_file = f"/home/jw/src/iching_cli/book/v2/{hex_num_str}_img.txt"
            try:
                with open(output_file, 'w') as f:
                    f.write(response)
                print(Fore.YELLOW + f"\nSaved description to: {output_file}" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Error saving to file: {e}" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
