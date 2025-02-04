#!/bin/env python3
"""
A script that generates descriptive paragraphs for I Ching hexagrams using AI.

This script takes a hexagram number (1-64) as input and generates two narrative paragraphs:
1. A general description of the hexagram's archetypal meaning
2. A description relating to tholonic concepts specific to the hexagram

The script uses context from local files (tholonic_primer.md and hexagram-specific JSON)
to inform the AI's response. The resulting description is printed to stdout and optionally
saved to a text file when using the --save flag.

Requires an API key set in the OPENAI_API_KEY environment variable, though this can be
any string when using the local server.

Usage:
    python get_new_hex_desc.py [-s] <hexagram_number>
Options:
    -s, --save    Save the output to a text file
Example:
    python get_new_hex_desc.py 20         # Display output only
    python get_new_hex_desc.py -s 20      # Display and save output
"""

import os
import sys
import base64
from openai import OpenAI
from colorama import Fore, Style
import argparse

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
    request_client = None
    try:
        # Add text content to context, but be more selective
        context = ""
        for filepath in context_files:
            if not filepath.lower().endswith('.png'):
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

        # Create a new client for each request
        request_client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url="http://127.0.0.1:1234/v1"
        )

        # Send a reset command first (if your server supports it)
        try:
            request_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "reset"}],
                temperature=0.1,
                max_tokens=10
            )
        except:
            pass  # Ignore if reset command isn't supported

        # Print debug information
        print(f"Context length: {len(context)} chars")
        print(f"Prompt length: {len(prompt)} chars")

        # Break the request into smaller chunks if needed
        messages = [
            {"role": "system", "content": "You are providing hexagram descriptions."},
            {"role": "user", "content": context[:4000]},  # Limit context size
            {"role": "user", "content": prompt}
        ]

        # Add memory management hints
        messages.insert(0, {"role": "system", "content": "clear previous conversation"})

        response = request_client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
            # Add any supported parameters for memory management
            presence_penalty=0.0,
            frequency_penalty=0.0
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {e}")
        print(f"Full error details: {str(e)}")
        return None
    finally:
        if request_client:
            try:
                # Send a cleanup request before closing
                request_client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "system", "content": "clear context"}],
                    temperature=0.1,
                    max_tokens=10
                )
            except:
                pass

            try:
                request_client.close()
            except:
                pass

def main():
    parser = argparse.ArgumentParser(description='Generate descriptive paragraphs for I Ching hexagrams')
    parser.add_argument('hexagram', type=int, help='Hexagram number (1-64)')
    parser.add_argument('-s', '--save', action='store_true', help='Save output to file')
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
