#!/bin/env python3
"""
=============================================================================
get_new_hex_desc_OPENAI.py - I Ching Hexagram Description Generator
=============================================================================

Description:
  This script generates descriptive paragraphs for I Ching hexagrams using
  OpenAI's GPT-4 API. For each hexagram, it generates two narrative paragraphs:
  1. A general description of the hexagram's archetypal meaning
  2. A description relating to tholonic concepts specific to the hexagram

Usage:
  python get_new_hex_desc_OPENAI.py [-s] <hexagram_number>

Arguments:
  hexagram_number: Number of the hexagram (1-64)
  -s, --save: Save the output to a text file

Examples:
  python get_new_hex_desc_OPENAI.py 20         # Display output only
  python get_new_hex_desc_OPENAI.py -s 20      # Display and save output

Process:
  1. Reads context from local files (tholonic_primer.md and hexagram JSON)
  2. Sends context to OpenAI's GPT-4 API for processing
  3. Generates two formatted paragraphs
  4. Optionally saves output to text file

Dependencies:
  - OpenAI Python package (v1.0.0 or later)
  - Valid OpenAI API key set in OPENAI_API_KEY environment variable
  - Access to GPT-4 model in your OpenAI account
  - Required Python packages: openai, colorama

File Structure:
  - Input: /book/tholonic_primer.md
  - Input: /book/v2/<hexagram_number>.json
  - Output: /book/v2/<hexagram_number>_hex.txt (when using --save)

Environment Variables:
  OPENAI_API_KEY: Your OpenAI API key (required)

Author: JW
Last Updated: 2024
=============================================================================
"""
import os
import sys
import base64
from openai import OpenAI
from colorama import Fore, Style
import argparse

# Initialize OpenAI client with API key from environment variable
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_file_content(filepath):
    """Read file content as string or base64 for images."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Failed to read {filepath}: {e}")
        return None

def get_contextual_response(context_files, hex_num_str):
    """Sends a request to the OpenAI API with the context files content."""
    try:
        # Add text content to context, but be more selective
        context = ""
        for filepath in context_files:
            content = get_file_content(filepath)
            if content:
                # Only include relevant sections to reduce context size
                if filepath.endswith('.json'):
                    # For JSON files, we might only need specific fields
                    context += f"\nEssential content from {os.path.basename(filepath)}:\n{content[:1000]}\n"
                else:
                    # For other files, take first portion
                    context += f"\nContent from {os.path.basename(filepath)}:\n{content[:2000]}\n"

        # Create a more concise prompt
        prompt = f"""
OUTPUT FORMAT: Write EXACTLY two paragraphs with ONE blank line between them. NO titles, NO numbers, NO headers, NO indentation, NO introduction, NO extra text.

CONTENT:
Paragraph 1: Write about the archetypal meaning (avoid all tholonic references). Include how we see this in the universe, world, and ourselves.

Paragraph 2: Write about the archetypal meaning, but using tholonic concepts

EXAMPLE OF EXACT FORMAT TO FOLLOW:
This is the first paragraph with no indentation. It goes on to make its complete point in a single paragraph format. This shows exactly how the first paragraph should look with no special formatting.

This is the second paragraph, also with no indentation. Notice there is exactly one blank line above this paragraph and no extra spaces or formatting. This is exactly how your response should look.

RULES:
- Always use the hexagram name when referring to the hexagram.
- Put hexagram names in quotes (e.g. "Initiation")
- Italicize these tholonic terms: *negotiation*, *limitation*, *contribution*
- No Chinese names or words. Replace with english translations.
- No technical terms (tetrahedral, hypergraph, holon, holons, parton, partons, tholon, tholons, holarchy, holarchies, etc.)

YOUR RESPONSE MUST FOLLOW THE EXACT FORMAT SHOWN ABOVE - TWO PLAIN PARAGRAPHS WITH ONE BLANK LINE BETWEEN THEM. NOTHING ELSE.
"""

        # Print debug information
        print(f"Context length: {len(context)} chars")
        print(f"Prompt length: {len(prompt)} chars")

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are providing hexagram descriptions."},
                {"role": "user", "content": context[:4000]},  # Limit context size
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        print(Fore.RED + f"OpenAI API error: {e}" + Style.RESET_ALL)
        print(Fore.RED + f"Full error details: {str(e)}" + Style.RESET_ALL)
        return None

def main():
    parser = argparse.ArgumentParser(description='Generate descriptive paragraphs for I Ching hexagrams using OpenAI')
    parser.add_argument('hexagram', type=int, help='Hexagram number (1-64)')
    parser.add_argument('-s', '--save', action='store_true', help='Save output to file')
    args = parser.parse_args()

    try:
        if args.hexagram < 1 or args.hexagram > 64:
            raise ValueError("Hexagram number must be between 1 and 64")
        hex_num_str = f"{args.hexagram:02d}"  # Zero-pad to 2 digits
    except ValueError as e:
        print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
        sys.exit(1)

    # Files to use as context
    context_files = [
        "/home/jw/src/iching_cli/book/tholonic_primer.md",
        f"/home/jw/src/iching_cli/book/v2/{hex_num_str}.json",
    ]

    # Get response using file contents as context
    response = get_contextual_response(context_files, hex_num_str)
    if response:
        print("\nResponse:")
        print(Fore.GREEN + response + Style.RESET_ALL)

        # Save response to file only if --save flag is used
        if args.save:
            output_file = f"/home/jw/src/iching_cli/book/v2/{hex_num_str}_hex.txt"
            try:
                with open(output_file, 'w') as f:
                    f.write(response)
                print(Fore.YELLOW + f"\nSaved description to: {output_file}" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Error saving to file: {e}" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
