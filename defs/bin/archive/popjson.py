#!/bin/env python

import sys
import openai
import os
import re
import json
from openai import OpenAI
from colorama import Fore, Style

client = OpenAI()

def markdown_to_json(markdown_file):
    with open(markdown_file, 'r') as file:
        markdown_data = file.read()

    # Split the markdown data into chunks to avoid truncation
    chunks = [markdown_data[i:i + 6719] for i in range(0, len(markdown_data), 6719)]

    json_data = []
    openai.api_key = os.getenv("OPENAI_API_KEY")

    for chunk in chunks:
        prompt = (
            "You are an assistant that helps convert Markdown data into a JSON array. "
            "Here is a Markdown file content representing hexagram data. Convert this data to a JSON array format: \n\n"
            f"{chunk}"
        )

        chat_completion = client.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": prompt}], temperature=0.3, max_tokens=6719)

        # Extract JSON from the response
        json_chunk = chat_completion.choices[0].message.content.strip()
        try:
            json_data.extend(json.loads(json_chunk))
        except json.JSONDecodeError as e:
            print(Fore.RED + f"An error occurred while decoding JSON ({markdown_file}): {e}" + Style.RESET_ALL)
            print(Fore.GREEN + f"{json_chunk}" + Style.RESET_ALL)

    return json_data

def save_to_json(json_data, output_file):
    with open(output_file, 'w') as file:
        json.dump(json_data, file, indent=4)
    print(f"Data saved to {output_file} successfully.")

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <markdown_file> <output_json_file>")
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_json_file = sys.argv[2]

    print(f"\nProcessing {markdown_file}...")

    json_data = markdown_to_json(markdown_file)
    save_to_json(json_data, output_json_file)

if __name__ == "__main__":
    main()
