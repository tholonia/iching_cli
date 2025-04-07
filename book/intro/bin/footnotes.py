#!/bin/env python3
import re
import sys


def extract_footnote_numbers(markdown_text):
    # Regular expression to find footnote references in the format [^nn]
    # This will match [^1], [^42], [^123], etc.
    footnote_pattern = r"\[\^(\d+)\]"

    # Find all matches in the text
    matches = re.findall(footnote_pattern, markdown_text)

    # Convert the matched strings to integers for proper numerical sorting
    footnote_numbers = [int(num) for num in matches]

    # Remove duplicates (a footnote might be referenced multiple times)
    unique_footnotes = sorted(set(footnote_numbers))

    return unique_footnotes


def main():
    # Check if a filename was provided as command line argument
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            with open(filename, "r", encoding="utf-8") as file:
                markdown_text = file.read()
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return
        except Exception as e:
            print(f"Error reading file: {e}")
            return
    else:
        # If no filename provided, read from stdin
        print("Please enter or paste your Markdown text (press Ctrl+D when finished):")
        markdown_text = sys.stdin.read()

    # Extract and sort footnote numbers
    footnote_numbers = extract_footnote_numbers(markdown_text)

    # Print the results
    if footnote_numbers:
        print("Footnote numbers found (in numerical order):")
        for num in footnote_numbers:
            print(num)
    else:
        print("No footnotes found in the document.")


if __name__ == "__main__":
    main()
