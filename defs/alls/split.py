#!/bin/env python

import sys
import os


def split_markdown(markdown_file):
    # Read the contents of the markdown file
    with open(markdown_file, 'r') as file:
        markdown_data = file.read()

    # Split the markdown data into two parts: before and after "# Three Tales"
    split_marker = "# Three Tales"
    split_index = markdown_data.find(split_marker)

    if split_index == -1:
        print(f"The marker '{split_marker}' was not found in the file.")
        sys.exit(1)

    # Extract the core and remaining parts
    core_text = markdown_data[:split_index]
    remaining_text = markdown_data[split_index:]

    # Create new filenames for the core and remaining parts
    base_filename, file_extension = os.path.splitext(markdown_file)
    core_filename = f"{base_filename}-core{file_extension}"
    rem_filename = f"{base_filename}-rem{file_extension}"

    # Save the core part to the new file
    with open(core_filename, 'w') as core_file:
        core_file.write(core_text)
    print(f"Core content saved to {core_filename}")

    # Save the remaining part to the new file
    with open(rem_filename, 'w') as rem_file:
        rem_file.write(remaining_text)
    print(f"Remaining content saved to {rem_filename}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <markdown_file>")
        sys.exit(1)

    markdown_file = sys.argv[1]
    split_markdown(markdown_file)


if __name__ == "__main__":
    main()
