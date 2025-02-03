#!/bin/env python3

import os
import sys
import base64
from openai import OpenAI

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
        Explain briefly as possible why this image its elements and its styles were chosen
        to represent this hexagram {hex_num_str}. Respond in a narrative paragraph. If you refer to the
        hexagram, do so by name, not by number. Start vthe paragramg with teh name of the hexagram in quotations, for example:

        "Contemplation" is vividly depicted...

        Use the name of the hexagram from the JSON file, not the traditional name.
        Keep the response to ~100 words.
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
    if len(sys.argv) != 2:
        print("Usage: python get_new_image_desc.py <hexagram_number>")
        print("Example: python get_new_image_desc.py 20")
        sys.exit(1)

    try:
        hex_num = int(sys.argv[1])
        if hex_num < 1 or hex_num > 64:
            raise ValueError("Hexagram number must be between 1 and 64")
        hex_num_str = f"{hex_num:02d}"  # Zero-pad to 2 digits
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Files to use as context
    context_files = [
        "/home/jw/src/iching_cli/defs/tholonic_primer.md",
#        "/home/jw/src/iching_cli/defs/final/Thee_tholonic_iching.md",
        f"/home/jw/src/iching_cli/defs/v2/{hex_num_str}.json",
        f"/home/jw/src/iching_cli/defs/v2/{hex_num_str}.png",
    ]

    # Get response using file contents as context
    response = get_contextual_response(context_files, hex_num_str)
    if response:
        print("\nResponse:")
        print(response)

        # Save response to file
        output_file = f"/home/jw/src/iching_cli/defs/v2/{hex_num_str}_img.txt"
        try:
            with open(output_file, 'w') as f:
                f.write(response)
            print(f"\nSaved description to: {output_file}")
        except Exception as e:
            print(f"Error saving to file: {e}")

if __name__ == "__main__":
    main()
