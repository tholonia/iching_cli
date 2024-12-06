#!/bin/env python3

import json
import sys
import os

def update_json_file(file_number, setnum):
    # Ensure the file number is zero-padded
    padded_number = str(file_number).zfill(2)

    # Define file paths with setnum
    json_file = f"/home/jw/store/src/iching_cli/defs/final/{padded_number}.json"
    txt_file = f"/home/jw/store/src/iching_cli/defs/s{setnum}/{padded_number}.txt"

    # Check if files exist
    if not os.path.exists(json_file):
        print(f"Error: JSON file {json_file} not found")
        return

    if not os.path.exists(txt_file):
        print(f"Error: Text file {txt_file} not found")
        return

    try:
        # Read the text file content
        with open(txt_file, 'r', encoding='utf-8') as f:
            image_description = f.read().strip()

        # Read and parse the JSON file
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Update the core section with new values
        if 'hx' in data and 'core' in data['hx']:
            data['hx']['core']['image_description'] = image_description
            data['hx']['core']['image_file'] = f"{padded_number}.png"
        else:
            print("Error: Expected JSON structure not found (missing 'hx.core')")
            return

        # Write the updated JSON back to file
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"Successfully updated {json_file}")

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {json_file}: {e}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <file_number> <set_number>")
        print("Example: python script.py 20 1")
        sys.exit(1)

    try:
        file_number = int(sys.argv[1])
        setnum = int(sys.argv[2])

        if not 0 <= file_number <= 99:
            raise ValueError("File number must be between 0 and 99")
        if not 1 <= setnum <= 9:
            raise ValueError("Set number must be between 1 and 9")

        update_json_file(file_number, setnum)
    except ValueError as e:
        print(f"Error: Invalid input - {str(e)}")
