#!/bin/env python
import re
import sys

def capitalize_quoted_words_in_file(filename):
    try:
        # Read the content of the file
        with open(filename, 'r') as file:
            content = file.read()

        # Find all words enclosed in double quotes and update them
        def capitalize_match(match):
            word = match.group(1)
            return f'"{word.capitalize()}"'

        modified_content = re.sub(r'"(\w+)"', capitalize_match, content)

        # Write the modified content back to the original file
        with open(filename, 'w') as file:
            file.write(modified_content)

        print(f"The file '{filename}' has been updated successfully.")
    except FileNotFoundError:
        print(f"The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Usage example
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
    else:
        filename = sys.argv[1]
        capitalize_quoted_words_in_file(filename)
